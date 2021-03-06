import unittest
import gongbu
import sqlite3


class TestDatabaseRules(unittest.TestCase):

    def setUp(self):
        self.connection = sqlite3.connect('./src/sql/gongbu.db')
        self.connection.isolation_level = None
        self.cursor = self.connection.cursor()

        self.cursor.execute('PRAGMA foreign_keys=1')

        self.cursor.execute('BEGIN TRANSACTION')

        self.cursor.execute('INSERT INTO state_descriptions '
                            '(stateID, state_description) VALUES '
                            '(42, "ANY_STATE_1"), '
                            '(43, "ANY_STATE_2")')

        self.cursor.execute('INSERT INTO property_descriptions '
                            '(propID, prop_description) VALUES '
                            '(110, "PROPERTY_1"), '
                            '(111, "PROPERTY_2")')

        self.cursor.execute('INSERT INTO property_definitions '
                            '(propID, stateID) VALUES '
                            '(110, 42), '
                            '(110, 43), '
                            '(111, 42)')

        self.cursor.execute('INSERT INTO definitions '
                            '(defnID, korean, english) VALUES '
                            '(1000, "ANY_KOREAN_1", "ANY_ENGLISH_1"), '
                            '(1001, "ANY_KOREAN_2", "ANY_ENGLISH_2")')

        self.cursor.execute('INSERT INTO properties '
                            '(defnID, propID, stateID) VALUES '
                            '(1000, 110, 42), '
                            '(1000, 111, 42)')

    def tearDown(self):
        self.cursor.execute('ROLLBACK')
        self.cursor.close()
        self.connection.close()

    def test_state_must_be_assigned_to_property(self):
        with self.assertRaises(sqlite3.IntegrityError) as cm:

            self.cursor.execute('INSERT INTO properties '
                                '(defnID, propID, stateID) VALUES '
                                '(1001, 111, 43)')

        self.assertEqual(str(cm.exception), 'FOREIGN KEY constraint failed')

    def test_property_must_have_unique_state(self):
        with self.assertRaises(sqlite3.IntegrityError) as cm:

            self.cursor.execute('INSERT INTO properties '
                                '(defnID, propID, stateID) VALUES '
                                '(1000, 110, 43)')

        self.assertEqual(str(cm.exception), 'UNIQUE constraint failed: '
                                            'properties.defnID, '
                                            'properties.propID')


class TestLabelDatabaseInteraction(unittest.TestCase):

    def setUp(self):
        self.connection = sqlite3.connect('./src/sql/gongbu.db')
        self.connection.isolation_level = None
        self.cursor = self.connection.cursor()

        self.cursor.execute('BEGIN TRANSACTION')

        self.cursor.execute('INSERT INTO label_descriptions '
                            '(lblID, description) VALUES '
                            '(42, "ANY_LABEL")')

        self.cursor.execute('INSERT INTO definitions '
                            '(defnID, korean, english) VALUES '
                            '(1000, "ANY_KOREAN", "ANY_ENGLISH")')

        self.cursor.execute('INSERT INTO labels '
                            '(defnID, lblID) VALUES '
                            '(1000, 42)')

    def tearDown(self):
        self.cursor.execute('ROLLBACK')
        self.cursor.close()
        self.connection.close()

    def test_label_database_interaction(self):
        label = gongbu.Label(42, 'ANY_LABEL')

        received = label.get_words(self.cursor)
        expected = [(1000, 'ANY_KOREAN', 'ANY_ENGLISH')]

        self.assertEqual(expected, received)


class TestStatelDatabaseInteraction(unittest.TestCase):

    def setUp(self):
        self.connection = sqlite3.connect('./src/sql/gongbu.db')
        self.connection.isolation_level = None
        self.cursor = self.connection.cursor()

        self.cursor.execute('BEGIN TRANSACTION')

        self.cursor.execute('INSERT INTO state_descriptions '
                            '(stateID, state_description) VALUES '
                            '(42, "ANY_STATE")')

        self.cursor.execute('INSERT INTO property_descriptions '
                            '(propID, prop_description) VALUES '
                            '(110, "PROPERTY_1"), '
                            '(111, "PROPERTY_2")')

        self.cursor.execute('INSERT INTO property_definitions '
                            '(propID, stateID) VALUES '
                            '(110, 42), '
                            '(111, 42)')

        self.cursor.execute('INSERT INTO definitions '
                            '(defnID, korean, english) VALUES '
                            '(1000, "ANY_KOREAN", "ANY_ENGLISH")')

        self.cursor.execute('INSERT INTO properties '
                            '(defnID, propID, stateID) VALUES '
                            '(1000, 110, 42), '
                            '(1000, 111, 42)')

    def tearDown(self):
        self.cursor.execute('ROLLBACK')
        self.cursor.close()
        self.connection.close()

    def test_state_database_interaction(self):
        state = gongbu.State(42, 'ANY_STATE')

        received = state.get_words(self.cursor)
        expected = [(1000, 'ANY_KOREAN', 'ANY_ENGLISH')]

        self.assertEqual(expected, received)


if __name__ == '__main__':
    unittest.main()
