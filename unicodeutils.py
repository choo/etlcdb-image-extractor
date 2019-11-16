#! /usr/bin/env python3
#! -*- coding: utf-8 -*-

import fsutils
import unicodedata


class UnicodeUtils(object):

    comment_prefix = '#'
    jis_x_0201_conf = {
        'mapping_file': './charset_data/JIS0201.TXT',
        'jis_code_col_idx': 0,
        'unicode_col_idx':  1
    }
    jis_x_0208_conf = {
        'mapping_file': './charset_data/JIS0208.TXT',
        'jis_code_col_idx': 1,
        'unicode_col_idx':  2
    }
    co59_mapping_file = './charset_data/co59-utf8.txt'

    uni_hira_start = 'ぁ' # 0x3041
    uni_hira_end   = 'ゖ' # 0x3096
    uni_kata_start = 'ァ' # 0x30a1
    uni_kata_end   = 'ヺ' # 0x30fa
    uni_hira_kata_diff = ord(uni_kata_start) - ord(uni_hira_start)

    def __init__(self):
        self.jis0201_to_uni = self._load_jis_mapping_info(
                self.jis_x_0201_conf['mapping_file'],
                self.jis_x_0201_conf['jis_code_col_idx'],
                self.jis_x_0201_conf['unicode_col_idx']
        )
        self.jis0208_to_uni = self._load_jis_mapping_info(
                self.jis_x_0208_conf['mapping_file'],
                self.jis_x_0208_conf['jis_code_col_idx'],
                self.jis_x_0208_conf['unicode_col_idx']
        )
        self.co59_to_uni = self._load_co59_info(self.co59_mapping_file)

    def convert_to_unicode(self, char_code, char_set = 'JIS_X_0208'):
        '''
            returns unicode hex string.
            char_set is either JIS_X_0201, JIS_X_0208, CO-59.

            if char_set is JIS, char_code is given as hex string.
            if char_set is CO-59, char_code is given as tuple with 2 int elements.
        '''
        ret = char_code
        if char_set == 'JIS_X_0208' and char_code in self.jis0208_to_uni:
            ret = self.jis0208_to_uni[char_code]
        if char_set == 'JIS_X_0201' and char_code in self.jis0201_to_uni:
            ret = self.jis0201_to_uni[char_code]
        if char_set == 'CO-59':
            ret = self.co59_to_uni[char_code]
        ret = '0x{:04x}'.format(int(ret, 16))
        return ret


    def _load_jis_mapping_info(self, filepath, jis_code_col_idx, unicode_col_idx):
        lines = fsutils.read_csv(
                filepath, has_header = False, comment_prefix = self.comment_prefix)
        ret = {}
        for line in lines:
            jis_code      = line[jis_code_col_idx].lower()
            unicode_code  = line[unicode_col_idx].lower()
            ret[jis_code] = unicode_code
        return ret


    def _load_co59_info(self, filepath):
        '''
            '▲' means the character cannot be read,
            so replace it with null char (0x00)
        '''
        lines = fsutils.read_lines(filepath)
        ret = {}
        for line in lines:
            elms = line.split(':')
            s = elms[0]
            if s == '▲':
                s = '\x00'
            codes = elms[1].split(',') # 2 elms
            codes = (int(codes[0]), int(codes[1]))
            ret[codes] = hex(ord(s))
        return ret


    @classmethod
    def hira2kata(cls, s):
        ret = []
        for c in s:
            if cls.is_hiragana(c):
                ret.append(chr(ord(c) + cls.uni_hira_kata_diff))
            else:
                ret.append(c)
        return ''.join(ret)

    @classmethod
    def kata2hira(cls, s):
        ret = []
        for c in s:
            if (cls.is_katakana(c) and 
                    cls.is_hiragana(chr(ord(c) - cls.uni_hira_kata_diff))):
                ret.append(chr(ord(c) - cls.uni_hira_kata_diff))
            else:
                ret.append(c)
        return ''.join(ret)


    @classmethod
    def is_hiragana(cls, char):
        return cls.uni_hira_start <= char <= cls.uni_hira_end

    @classmethod
    def is_katakana(cls, char):
        '''Judge if given char is katakana or not

        NOTE: halfwidth katakana is not be considered as true in thie method
        '''
        return cls.uni_kata_start <= char <= cls.uni_kata_end

    @staticmethod
    def normalize(s):
        '''
            wrapper method of unicodedata.noramlize
        '''
        return unicodedata.normalize('NFKC', s)

