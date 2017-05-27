# About

This is a little flashcard program, meant to help with learning Korean vocabulary. It is built around an SQLite database.

Coded by David Ouwehand. This program is released under the terms of the GNU General Public License.

Despite the existence of many flashcard programs, there are two reasons why this one exists:

Firstly, the Korean language has many homonyms. For homonyms I want all the known definitions to be displayed.

Secondly, I already had a wordlist. This was a spreadsheet 6 columns wide, designed to be printed with 3 columns per sheet. Then, by gluing the sheets back-to-back, you get actual paper flashcards. Of course I wanted to re-use this list. This can be done by first exporting to CSV, then importing into a database.

# Features

Comes with a built-in wordset, see `./src/sql/korean_cards_dump.csv`. This wordlist corresponds more or less to the lowest-level language course of the [King Sejong Institute](https://en.wikipedia.org/wiki/King_Sejong_Institute). There may be mistakes.

Alternatively, you can use your own wordlist. The program and database are entirely based on Unicode, so everything should work for other homonym-rich languages. You just need to somehow get the definitions inside the database.

Every definition in the database can be given a label or assigned a property. Contraty to labels, a property can have several mutually exclusive states. When reviewing words, you have the option to draw cards having only certain labels or certain properties.

The currently built-in labels and properties are:

* The label `Language test vocabulary`. I have seen homework and tests where even the assignments are written in Korean. Then it is important to know the typical vocabulary for language test assignments.

* The property `Regularity of verb / adjective`. This is meant for verbs / adjectives with stem ending in ㅂ or ㄷ. When conjugated, the ㅂ may or may not turn into 우. Similarly, the ㄷ may or may not turn into ㄹ.

# Installation

Get pybuilder first, if it's not installed already:

`pip install pybuilder`

Then to install the script called 'gongbu':

`pyb -X`

`pip install target/dist/gongbu-<version>/dist/gongbu-<version>.tar.gz`

Create a database file (need to have sqlite3 installed):

`./src/sql/database-setup.sh`

If you want a minimal database setup, without any words, then use the script `./src/sql/database-setup.sql`.

# Usage

You need to pass the 'gongbu' script a local database file as argument, e.g.:

`TODO`

For other command-line options, type: `gongbu -h`.

A fresh copy of the database can be generated with the shell script in `./src/sql`.

# TODO

* A GUI.

* A way to add more definitions.

* A way to edit the labels and properties of existing definitions.

* Display properties along with definitions. The idea is that properties contain useful meta-information, whereas labels are just used to group words.
