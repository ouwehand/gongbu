#!/usr/bin/python3

import random
import sqlite3
from abc import ABCMeta, abstractmethod
from collections import defaultdict

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
