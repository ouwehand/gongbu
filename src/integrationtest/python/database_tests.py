import unittest
import gongbu
import sqlite3


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

    def test_label_database(self):
        label = gongbu.Label(42, 'ANY_DESCR')

        received = label.get_words(self.cursor)
        expected = [(1000, 'ANY_KOREAN', 'ANY_ENGLISH')]

        self.assertEqual(expected, received)


if __name__ == '__main__':
    unittest.main()
