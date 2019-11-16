#! /usr/bin/env python3
#! -*- coding: utf-8 -*-

import os, struct, argparse
from PIL import Image
import fsutils
from unicodeutils import UnicodeUtils


DEF_YAML_PATH = './etl_data_def.yml'
DATA_DIR_ROOT = './etl_data'
OUTPUT_ROOT = '{}/images'.format(DATA_DIR_ROOT)


def _read_record(f, data_format):
    s = f.read(data_format['record_size'])
    r = struct.unpack(data_format['record_format'], s)

    charcode_idx = data_format['char_code_index']
    img_data_idx = data_format['image_data_index']
    reso      = data_format['resolution']
    bit_depth = data_format['bit_depth']
    char_code = r[charcode_idx]
    img = Image.frombytes('F', reso, r[img_data_idx], 'bit', bit_depth)
    img = img.convert('L')
    return char_code, img


def _convert_charcode(char_code, char_set):
    if char_set == 'JIS_X_0201' or char_set == 'JIS_X_0208':
        ret = hex(char_code)
    elif char_set == 'CO-59':
        ''' 2 codes have 6 bits and are stored packed in CO-59 data '''
        code1 = char_code[0] >> 2
        code2 = ((char_code[0] & 0b11) << 4) + (char_code[1] >> 4)
        ret = (code1, code2)
    return ret


def _convert_img(img):
    ret = Image.eval(img, lambda x: 255 - x * 16)
    return ret


def extract_info(data_name, data_format, is_hiragana = False, save_same_dir = False):

    '''
        data_foramt['char_set'] should be either 'JIS_X_0208', 'JIS_X_0201' or 'CO-59'
    '''

    print('extraction of data set "{}" start.'.format(data_name))

    if save_same_dir:
        output_dir = '{}/{}'.format(OUTPUT_ROOT, 'all')
        file_prefix = '{}_'.format(data_name)
    else:
        output_dir = '{}/{}'.format(OUTPUT_ROOT, data_name)
        file_prefix = ''
    record_idx = 0
    unicode_utils = UnicodeUtils()
    data_dir = '{}/{}'.format(DATA_DIR_ROOT, data_name)
    if not os.path.exists(data_dir):
        print('Dataset {} does not exist, so skip extracting this dataset'.format(data_name))
        return
    files = fsutils.list_files(data_dir)
    files = [f for f in files if not f.endswith('INFO')]
    char_set = data_format['char_set']
    rec_size = data_format['record_size']

    for filepath in files:
        filesize = os.path.getsize(filepath)
        if filesize % rec_size > 0:
            message = 'File size "{}" or record size "{}" is invalid in {}'.format(
                    filesize, rec_size, filepath)
            raise Exception(message)

        with open(filepath, 'rb') as f:
            num_records = filesize // rec_size
            for _ in range(num_records):
                char_code, img = _read_record(f, data_format)
                char_code = _convert_charcode(char_code, char_set)
                img = _convert_img(img)

                unicode_hex = unicode_utils.convert_to_unicode(char_code, char_set)
                char_str = chr(int(unicode_hex, 16))

                ''' nomalization and kata -> hira conversion '''
                if char_str != UnicodeUtils.normalize(char_str):
                    char_str = UnicodeUtils.normalize(char_str)
                    if is_hiragana:
                        char_str = UnicodeUtils.kata2hira(char_str)
                    unicode_hex = '0x{:04x}'.format(ord(char_str), 16)

                ## for debug
                #print(char_str, unicode_hex, record_idx)

                save_dir = '{}/{}'.format(output_dir, unicode_hex)
                img_filepath = '{}/{}{:06d}.png'.format(save_dir, file_prefix, record_idx)
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                    fsutils.write_file(char_str, '{}/.char.txt'.format(save_dir))
                img.save(img_filepath)

                record_idx += 1

                ## for debug
                #print(char_str, unicode_hex, record_idx)

            print('extracted {} images from file {}.'.format(record_idx, filepath))

        print('completed! extracted {} images.'.format(record_idx))
        print('******************************* \n')


def main(data_sets, save_same_dir=False):
    etl_def = fsutils.read_yaml(DEF_YAML_PATH)
    for data_set_idx in data_sets:
        idx = data_set_idx - 1
        data_set_def = etl_def['data_set_def'][idx]
        data_name    = data_set_def['data_name']
        format_name  = data_set_def['data_format']
        is_hiragana  = ('is_hiragana' in data_set_def and data_set_def['is_hiragana'])
        data_format  = etl_def['data_format_def'][format_name]
        extract_info(data_name, data_format, is_hiragana, save_same_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data extractor of ETL Character Database')
    parser.add_argument('--data_sets', nargs='*', type=int, dest='data_sets',
                        required=False, default=range(1, 10),
                        choices=range(1, 10), help='dataset number.')
    parser.add_argument('--save_same_dir', dest='save_same_dir', action='store_true',
                        help=('save images in one directory, ' +
                              'or divide it to each data set directory. ("False" in default)'))

    args = parser.parse_args()
    main(args.data_sets, args.save_same_dir)
