import unittest
import unittest.mock as mock
import gongbu
from collections import namedtuple
import sqlite3


class TestLabel(unittest.TestCase):

    def setUp(self):
        self.label = gongbu.Label('ANY_ID', 'ANY_DESC')

    def test_should_initialize_label_and_decr(self):
        self.assertEqual(self.label.label_ID, ('ANY_ID',))
        self.assertEqual(self.label.description, 'ANY_DESC')

    @mock.patch('sqlite3.connect')
    def test_should_execute_instruction_and_return_fetchall(self, mock_conn):

        self.label.instruction = 'ANY_INST'
        conn = sqlite3.connect('ANY_DB')
        cursor = conn.cursor()
        cursor.fetchall.return_value = 'ANY_FETCH'

        received = self.label.get_words(cursor)

        cursor.execute.assert_called_once_with('ANY_INST', ('ANY_ID',))
        cursor.fetchall.assert_called_once_with()
        self.assertEqual(received, 'ANY_FETCH')


class TestState(unittest.TestCase):

    def setUp(self):
        self.state = gongbu.State('ANY_ID', 'ANY_DESC')

    def test_should_initialize_label_and_decr(self):
        self.assertEqual(self.state.state_ID, ('ANY_ID',))
        self.assertEqual(self.state.description, 'ANY_DESC')

    @mock.patch('sqlite3.connect')
    def test_should_execute_instruction_and_return_fetchall(self, mock_conn):

        self.state.instruction = 'ANY_INST'
        conn = sqlite3.connect('ANY_DB')
        cursor = conn.cursor()
        cursor.fetchall.return_value = 'ANY_FETCH'

        received = self.state.get_words(cursor)

        cursor.execute.assert_called_once_with('ANY_INST', ('ANY_ID',))
        cursor.fetchall.assert_called_once_with()
        self.assertEqual(received, 'ANY_FETCH')


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
                    ['ANY_ENGLISH_WORD_2'])].sort()
        received = gongbu.collect_homonyms(defn_dict).sort()
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
