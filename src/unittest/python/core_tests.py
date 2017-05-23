import unittest
import unittest.mock as mock
import gongbu
from collections import namedtuple
import sqlite3


class TestGenWordlist(unittest.TestCase):

    def test_collect_homonyms(self):
        """Test for auxiliary function collect_homonyms"""
        defn_dict = {
                1: ('ANY_KOREAN_WORD_1', 'ANY_ENGLISH_WORD_1'),
                2: ('ANY_KOREAN_WORD_2', 'ANY_ENGLISH_WORD_2'),
                3: ('ANY_KOREAN_WORD_1', 'ANY_ENGLISH_WORD_3')}
        expected = [
                ('ANY_KOREAN_WORD_1',
                    ['ANY_ENGLISH_WORD_1', 'ANY_ENGLISH_WORD_3']),
                ('ANY_KOREAN_WORD_2',
                    ['ANY_ENGLISH_WORD_2'])]
        received = gongbu.collect_homonyms(defn_dict)
        self.assertEqual(received, expected)

    def test_active_categories_empty_e2k_true(self):
        mock_cursor = mock.Mock()
        mock_cursor.fetchall.return_value = [
                (1, 'ANY_KOREAN_WORD_1', 'ANY_ENGLISH_WORD_1'),
                (2, 'ANY_KOREAN_WORD_2', 'ANY_ENGLISH_WORD_2')]

        expected = [('ANY_ENGLISH_WORD_1', ['ANY_KOREAN_WORD_1']),
                    ('ANY_ENGLISH_WORD_2', ['ANY_KOREAN_WORD_2'])]

        received = gongbu.generate_wordlist(mock_cursor, set(), True)
        self.assertEqual(received, expected)
