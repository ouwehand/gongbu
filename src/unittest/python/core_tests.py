import unittest
import unittest.mock as mock
import gongbu
import sqlite3


class TestLabel(unittest.TestCase):

    def setUp(self):
        self.label = gongbu.Label('ANY_ID', 'ANY_DESC')

    def test_property_description(self):
        self.assertEqual(self.label.description, 'ANY_DESC')

    @mock.patch('sqlite3.connect')
    def test_get_words_database_execution(self, mock_conn):
        self.label._Label__instruction = 'ANY_INST'
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

    def test_property_description(self):
        self.assertEqual(self.state.description, 'ANY_DESC')

    @mock.patch('sqlite3.connect')
    def test_get_words_database_execution(self, mock_conn):
        self.state._State__instruction = 'ANY_INST'
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

    @mock.patch('sqlite3.connect')
    def setUp(self, mock_conn):
        conn = sqlite3.connect('ANY_DB')
        self.mock_cursor = conn.cursor.return_value

    def test_active_categories_empty_e2k_true(self):
        self.mock_cursor.fetchall.return_value = [
                (1, 'ANY_KOREAN_WORD_1', 'ANY_ENGLISH_WORD_1'),
                (2, 'ANY_KOREAN_WORD_2', 'ANY_ENGLISH_WORD_2')]

        expected = [('ANY_ENGLISH_WORD_1', ['ANY_KOREAN_WORD_1']),
                    ('ANY_ENGLISH_WORD_2', ['ANY_KOREAN_WORD_2'])].sort()

        received = gongbu.generate_wordlist(self.mock_cursor,
                                            set(), True).sort()
        self.assertEqual(received, expected)

    @mock.patch('gongbu.collect_homonyms')
    def test_active_categories_empty_e2k_false(self, mock_homonyms):
        self.mock_cursor.fetchall.return_value = [
                (1, 'ANY_KOREAN_WORD_1', 'ANY_ENGLISH_WORD_1'),
                (2, 'ANY_KOREAN_WORD_2', 'ANY_ENGLISH_WORD_2')]

        intermediate = {
                        1: ('ANY_KOREAN_WORD_1', 'ANY_ENGLISH_WORD_1'),
                        2: ('ANY_KOREAN_WORD_2', 'ANY_ENGLISH_WORD_2')}

        gongbu.generate_wordlist(self.mock_cursor, set(), False)
        mock_homonyms.assert_called_once_with(intermediate)

    @mock.patch('gongbu.State.get_words')
    @mock.patch('gongbu.Label.get_words')
    def test_active_categories_nonempty_e2k_true(self, mock_label, mock_state):
        active_category_1 = gongbu.Label('ANY_STATE_1', 'ANY_DESCR_1')
        active_category_1.get_words.return_value = [
                (1, 'ANY_KOREAN_WORD_1', 'ANY_ENGLISH_WORD_1'),
                (2, 'ANY_KOREAN_WORD_2', 'ANY_ENGLISH_WORD_2')]

        active_category_2 = gongbu.State('ANY_STATE_2', 'ANY_DESCR_2')
        active_category_2.get_words.return_value = [
                (1, 'ANY_KOREAN_WORD_1', 'ANY_ENGLISH_WORD_1'),
                (3, 'ANY_KOREAN_WORD_3', 'ANY_ENGLISH_WORD_3')]

        active_categories = set()
        active_categories.add(active_category_1)
        active_categories.add(active_category_2)

        expected = [('ANY_ENGLISH_WORD_1', ['ANY_KOREAN_WORD_1']),
                    ('ANY_ENGLISH_WORD_2', ['ANY_KOREAN_WORD_2']),
                    ('ANY_ENGLISH_WORD_3', ['ANY_KOREAN_WORD_3'])].sort()

        received = gongbu.generate_wordlist(self.mock_cursor,
                                            active_categories, True).sort()
        self.assertEqual(received, expected)

    @mock.patch('gongbu.collect_homonyms')
    @mock.patch('gongbu.State.get_words')
    @mock.patch('gongbu.Label.get_words')
    def test_active_categories_nonempty_e2k_false(self, mock_label, mock_state, mock_homonyms):
        active_category_1 = gongbu.Label('ANY_STATE_1', 'ANY_DESCR_1')
        active_category_1.get_words.return_value = [
                (1, 'ANY_KOREAN_WORD_1', 'ANY_ENGLISH_WORD_1'),
                (2, 'ANY_KOREAN_WORD_2', 'ANY_ENGLISH_WORD_2')]

        active_category_2 = gongbu.State('ANY_STATE_2', 'ANY_DESCR_2')
        active_category_2.get_words.return_value = [
                (1, 'ANY_KOREAN_WORD_1', 'ANY_ENGLISH_WORD_1'),
                (3, 'ANY_KOREAN_WORD_3', 'ANY_ENGLISH_WORD_3')]

        active_categories = set()
        active_categories.add(active_category_1)
        active_categories.add(active_category_2)

        intermediate = {
                        1: ('ANY_KOREAN_WORD_1', 'ANY_ENGLISH_WORD_1'),
                        2: ('ANY_KOREAN_WORD_2', 'ANY_ENGLISH_WORD_2'),
                        3: ('ANY_KOREAN_WORD_3', 'ANY_ENGLISH_WORD_3')}
        gongbu.generate_wordlist(self.mock_cursor, active_categories, False)
        mock_homonyms.assert_called_once_with(intermediate)


class TestDatabaseConnection(unittest.TestCase):

    @mock.patch('sqlite3.connect')
    def test_databse_setup_release(self, mock_conn):
        data_init = gongbu.DatabaseConnection('ANY_NAME')

        mock_connection = sqlite3.connect.return_value
        mock_cursor = mock_connection.cursor.return_value
        mock_cursor.fetchall.return_value = [(2, 'ANY_DESCR')]

        with data_init:
            sqlite3.connect.assert_called_once_witch('ANY_NAME')
            mock_connection.cursor.assert_called_once_with()

        mock_cursor.close.assert_called_once_with()
        mock_connection.commit.assert_called_once_with()
        mock_connection.close.assert_called_once_with()


class TestWordData(unittest.TestCase):

        @mock.patch('sqlite3.connect')
        def setUp(self, mock_conn):
            with gongbu.DatabaseConnection('ANY_DB') as db_connection:
                cursor = db_connection.cursor
                cursor.fetchall.return_value = [['ANY_ID', 'ANY_DESCRIPTION']]
                self.word_data = gongbu.WordData(db_connection)

        @mock.patch('gongbu.generate_wordlist')
        def test_get_definition(self, mock_genword):
            mock_genword.return_value = [('ANY_WORD', ['ANY_DEFN_1', 'ANY_DEFN_2'])]
            expected = 'ANY_WORD', 'ANY_DEFN_1; ANY_DEFN_2'
            self.assertEqual(self.word_data.get_definition(), expected)
            mock_genword.assert_called_once()

        def test_property_categories(self):
            description_list = [c.description for c in self.word_data.categories]
            self.assertEqual(description_list, ['ANY_DESCRIPTION', 'ANY_DESCRIPTION'])

        @mock.patch('gongbu.generate_wordlist')
        def test_active_categories_setter(self, mock_genword):
            mock_genword.return_value = [('ANY_WORD', ['ANY_DEFN_1', 'ANY_DEFN_2'])]
            new_active = set()
            cat = self.word_data.categories[0]
            new_active.add(cat)
            self.word_data.active_categories = new_active
            self.assertEqual(self.word_data.active_categories, new_active)
            self.word_data.get_definition()
            mock_genword.assert_called_once()

        @mock.patch('gongbu.generate_wordlist')
        def test_english_to_korean_setter(self, mock_genword):
            mock_genword.return_value = [('ANY_WORD', ['ANY_DEFN_1', 'ANY_DEFN_2'])]
            self.word_data.english_to_korean = True
            self.assertEqual(self.word_data.english_to_korean, True)
            self.word_data.get_definition()
            mock_genword.assert_called_once() 
