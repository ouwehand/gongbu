import random
import sqlite3
from abc import ABCMeta, abstractmethod
from collections import defaultdict


class Category(metaclass=ABCMeta):
    """A category is either a label or a state of a property"""

    @property
    @abstractmethod
    def description(self):
        pass

    @abstractmethod
    def get_words(self, cursor):
        pass


class Label(Category):

    def __init__(self, label_ID, description):
        self.__label_ID = (label_ID,)
        self.__description = description
        self.__instruction = ('SELECT definitions.defnID, korean, english'
                              ' FROM definitions INNER JOIN labels'
                              ' ON labels.defnID = definitions.defnID'
                              ' WHERE lblID = ?')

    @property
    def description(self):
        return self.__description

    def get_words(self, cursor):
        cursor.execute(self.__instruction, self.__label_ID)
        return cursor.fetchall()


class State(Category):

    def __init__(self, state_ID, description):
        self.__state_ID = (state_ID,)
        self.__description = description
        self.__instruction = ('SELECT DISTINCT definitions.defnID, korean, english'
                              ' FROM definitions INNER JOIN properties'
                              ' ON properties.defnID = definitions.defnID'
                              ' WHERE StateID = ?')

    @property
    def description(self):
        return self.__description

    def get_words(self, cursor):
        cursor.execute(self.__instruction, self.__state_ID)
        return cursor.fetchall()


def generate_wordlist(cursor, active_categories, english_to_korean=False):
    """Generating a wordlist corresponding to selected categories"""

    defn_dict = {}

    # Empty set of active categories means that we get *all* the words

    if len(active_categories) == 0:
        cursor.execute('SELECT * FROM definitions')
        for v in cursor.fetchall():
            defn_dict[v[0]] = (v[1], v[2])
    else:
        for s in active_categories:
            for v in s.get_words(cursor):
                defn_dict[v[0]] = (v[1], v[2])

    if english_to_korean:
        return [(defn_dict[word][1], [defn_dict[word][0]])
                for word in defn_dict]
    else:
        return collect_homonyms(defn_dict)


def collect_homonyms(defn_dict):
    """Deal with homonyms: concatenate the English translations."""

    korean_dict = defaultdict(list)

    for key in defn_dict:
        korean_word = defn_dict[key][0]
        english_translation = defn_dict[key][1]
        korean_dict[korean_word].append(english_translation)

    return [(korean_word, korean_dict[korean_word])
            for korean_word in korean_dict]


class DatabaseConnection():

    def __init__(self, db_name):
        self.__db_name = db_name
        self.__cursor = None

    @property
    def cursor(self):
        return self.__cursor

    def __enter__(self):
        self.__connection = sqlite3.connect(self.__db_name)
        self.__cursor = self.__connection.cursor()
        return self

    def __exit__(self, type, value, traceback):
        self.cursor.close()
        self.__connection.commit()
        self.__connection.close()


class WordData():

    def __init__(self, database_connection):
        self.__categories = []
        self.__active_categories = set()
        self.__english_to_korean = False
        self.__cursor = database_connection.cursor
        self.__regenerate_wordlist = True

        random.seed()

        # Fetch all available categories (which is constant for the duration of the program)
        self.__cursor.execute('SELECT * FROM label_descriptions')

        for l in self.__cursor.fetchall():
            self.__categories.append(Label(l[0], l[1]))

        self.__cursor.execute('SELECT * FROM state_descriptions')

        for s in self.__cursor.fetchall():
            self.__categories.append(State(s[0], s[1]))

    @property
    def categories(self):
        return self.__categories.copy()

    @property
    def active_categories(self):
        return self.__active_categories.copy()

    @active_categories.setter
    def active_categories(self, new_active_categories):

        if new_active_categories != self.__active_categories:
            self.__active_categories = new_active_categories
            self.__regenerate_wordlist = True

    @property
    def english_to_korean(self):
        return self.__english_to_korean

    @english_to_korean.setter
    def english_to_korean(self, new_english_to_korean):

        if new_english_to_korean != self.english_to_korean:
            self.__english_to_korean = new_english_to_korean
            self.__regenerate_wordlist = True

    def get_definition(self):

        if self.__regenerate_wordlist:
            self.__regenerate_wordlist = False
            self.__wordlist = generate_wordlist(self.__cursor,
                                                self.__active_categories,
                                                self.__english_to_korean)

        i = random.randrange(0, len(self.__wordlist))
        word, definitions = self.__wordlist[i]
        return word, "; ".join(definitions)


def gongbu_cli():

    import argparse

    # Parse command-line arguments
    parser = argparse.ArgumentParser()

    parser.add_argument('db_file',
                        type=str,
                        help='database file',
                        metavar='FILENAME')

    parser.add_argument('-f',
                        '--filter',
                        dest='filter_by_category',
                        action='store_true',
                        help=('start with a menu that lets you '
                              'filter words by category'))

    parser.add_argument('-e2k',
                        '--english_to_korean',
                        action='store_true',
                        help=('translate from English to Korean, '
                              'rather than the other way around'))

    args = parser.parse_args()

    with DatabaseConnection(args.db_file) as db_connection:

        word_data = WordData(db_connection)
        categories = word_data.categories
        active_categories = set()

        # Define the active categories
        if args.filter_by_category:
            for i, category in enumerate(categories):
                print("{}: {}".format(i+1, category.description))

            while True:
                input_str = input(('\nPlease enter a category number, '
                                   'or zero to finish '))

                if input_str.isdigit():
                    num = int(input_str)

                    if num > 0 and num <= len(categories):
                        active_categories.add(categories[num-1])
                    if num == 0:
                        break

        # Pass settings to word_data object
        word_data.active_categories = active_categories
        word_data.english_to_korean = args.english_to_korean

        # Main loop
        while True:
            word, definition = word_data.get_definition()
            print(word)
            key = input("Press enter to see answer, 'x' to quit ")
            print(definition)
            print("--------------------")

            if key == 'x':
                break
