#!/usr/bin/python3

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


class InitializeData():

    def __init__(self):
        self.wordlist = []
        self.categories = []
        self.activeCategories = set()
        self.english_to_korean = False
        self.db_name = 'gongbu.db'

    def __enter__(self):
        random.seed()
       
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        # Fetch all available categories (which is constant for the duration of the program)
        self.cursor.execute("SELECT * FROM label_descriptions")

        for l in self.cursor.fetchall():
            self.categories.append(Label(l[0], l[1]))

        self.cursor.execute("SELECT * FROM state_descriptions")

        for s in self.cursor.fetchall():
            self.categories.append(State(s[0], s[1]))

        return self

    def __exit__(self, type, value, traceback):
        self.cursor.close()
        self.conn.commit()
        self.conn.close()
