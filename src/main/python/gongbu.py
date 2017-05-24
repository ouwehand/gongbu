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

    @description.setter
    @abstractmethod
    def description(self, value):
        pass

    @abstractmethod
    def get_words(self, cursor):
        pass


class Label(Category):

    def __init__(self, label_ID, description):
        self.label_ID = (label_ID,)
        self.description = description
        self.instruction = ('SELECT definitions.defnID, korean, english'
                            ' FROM definitions INNER JOIN labels'
                            ' ON labels.defnID = definitions.defnID'
                            ' WHERE lblID = ?')

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        self.__description = value

    def get_words(self, cursor):
        cursor.execute(self.instruction, self.label_ID)
        return cursor.fetchall()


class State(Category):

    def __init__(self, state_ID, description):
        self.state_ID = (state_ID,)
        self.description = description
        self.instruction = ('SELECT DISTINCT definitions.defnID, korean, english'
                            ' FROM definitions INNER JOIN properties'
                            ' ON properties.defnID = definitions.defnID'
                            ' WHERE StateID = ?')

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        self.__description = value

    def get_words(self, cursor):
        cursor.execute(self.instruction, self.state_ID)
        return cursor.fetchall()


def generate_wordlist(cursor, active_categories, english_to_korean=False):
    """Generating a wordlist corresponding to selected categories"""

    defn_dict = {}

    # Empty set of active categories means that we get *all* the words

    if len(active_categories) == 0:
        cursor.execute('select * from Definitions')
        for v in cursor.fetchall():
            defn_dict[v[0]] = (v[1], v[2])
    else:
        for s in active_categories:
            for v in s.getWords(cursor):
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
