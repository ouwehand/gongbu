#!/bin/sh

if [ ! -f "./gongbu.db" ]; then
	sqlite3 -batch gongbu.db < database_setup.sql
	sqlite3 -batch gongbu.db < import_cards.sql
fi
