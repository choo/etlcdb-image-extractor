#! /usr/bin/env python3
#! -*- coding: utf-8 -*-

from unittest import TestCase
from unicodeutils import UnicodeUtils


class TestUnicodeUtils(TestCase):

    mappings = {

            # JIS_X_0201 doesn't have full width char
            'あ': {
                'JIS_X_0208': '0x2422',
                'CO-59': (5, 12),
            },
            'ア': {
                'JIS_X_0208': '0x2522',
                'CO-59': (37, 12),
            },
            '宙': {
                'JIS_X_0208': '0x5b99',
                'CO-59': (56, 14),
            },

            # JIS_X_0208, CO-59 doesn't have half width char
            'ｱ': {
                'JIS_X_0201': '0xb1',
            },
            'ｧ': {
                'JIS_X_0201': '0xa7',
            },
            '｢': {
                'JIS_X_0201': '0xa2',
            },
            'ﾞ': {
                'JIS_X_0201': '0xde',
            },
    }

    def test_is_hiragana(self):
        self.assertTrue(UnicodeUtils.is_hiragana('あ'))
        self.assertTrue(UnicodeUtils.is_hiragana('ぁ'))
        self.assertTrue(UnicodeUtils.is_hiragana('ゔ'))
        self.assertTrue(UnicodeUtils.is_hiragana('ゑ'))
        self.assertTrue(UnicodeUtils.is_hiragana('ゖ'))

        self.assertFalse(UnicodeUtils.is_hiragana('ア'))
        self.assertFalse(UnicodeUtils.is_hiragana('A'))
        self.assertFalse(UnicodeUtils.is_hiragana('。'))

    def test_is_katakana(self):
        self.assertTrue(UnicodeUtils.is_katakana('ア'))
        self.assertTrue(UnicodeUtils.is_katakana('ァ'))
        self.assertTrue(UnicodeUtils.is_katakana('ヴ'))
        self.assertTrue(UnicodeUtils.is_katakana('ヱ'))
        self.assertTrue(UnicodeUtils.is_katakana('ヶ'))

        self.assertFalse(UnicodeUtils.is_katakana('あ'))
        self.assertFalse(UnicodeUtils.is_katakana('ぁ'))
        self.assertFalse(UnicodeUtils.is_katakana('ゔ'))
        self.assertFalse(UnicodeUtils.is_katakana('ゑ'))
        self.assertFalse(UnicodeUtils.is_katakana('ゖ'))
        self.assertFalse(UnicodeUtils.is_katakana('ｳ'))

        self.assertFalse(UnicodeUtils.is_katakana('A'))
        self.assertFalse(UnicodeUtils.is_katakana('。'))


    def test_hira2kata(self):
        self.assertEqual(UnicodeUtils.hira2kata('あ'), 'ア')
        self.assertEqual(UnicodeUtils.hira2kata('ゖ'), 'ヶ')
        self.assertEqual(UnicodeUtils.hira2kata('ゑ'), 'ヱ')
        self.assertEqual(UnicodeUtils.hira2kata('ゔ'), 'ヴ')
        self.assertEqual(UnicodeUtils.hira2kata('あいうぇお'), 'アイウェオ')


    def test_kata2hira(self):
        self.assertEqual(UnicodeUtils.kata2hira('ア'), 'あ')
        self.assertEqual(UnicodeUtils.kata2hira('ヶ'), 'ゖ')
        self.assertEqual(UnicodeUtils.kata2hira('ヱ'), 'ゑ')
        self.assertEqual(UnicodeUtils.kata2hira('ヷ'), 'ヷ') # does not exit in hiragana


    def test_convert_to_uni(self):

        unicode_utils = UnicodeUtils()

        for c, conf in self.mappings.items():
            for char_set, char_code in conf.items():
                converted = unicode_utils.convert_to_unicode(char_code, char_set)
                expected  = hex(ord(c))
                self.assertEqual(converted, expected)
