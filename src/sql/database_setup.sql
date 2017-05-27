/*   Copyright (C) 2017  David Ouwehand

     This program is free software: you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation, either version 3 of the License, or
     (at your option) any later version.

     This program is distributed in the hope that it will be useful,
     but WITHOUT ANY WARRANTY; without even the implied warranty of
     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
     GNU General Public License for more details.

     You should have received a copy of the GNU General Public License
     along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/


.mode column
PRAGMA foreign_keys = 1;

--Contains Korean words and English translations

CREATE TABLE definitions(
	defnID INTEGER PRIMARY KEY,
	korean TEXT NOT NULL,
	english TEXT NOT NULL
);

--Assign numeric identifiers to all the available labels

CREATE TABLE label_descriptions(
	lblID INTEGER PRIMARY KEY,
	description TEXT
);

INSERT INTO label_descriptions (description) VALUES ("Language test vocabulary");

--Assign one or more labels to a word

CREATE TABLE labels(
	defnID INTEGER NOT NULL,
	lblID INTEGER NOT NULL,

	PRIMARY KEY (defnID, lblID),
	FOREIGN KEY (defnID) REFERENCES definitions (defnID),
	FOREIGN KEY (lblID) REFERENCES label_descriptions (lblID)
);

--Assign numeric identifiers to all the available properties

CREATE TABLE property_descriptions(
	propID INTEGER PRIMARY KEY,
	prop_description TEXT
);

INSERT INTO property_descriptions (propID, prop_description) VALUES (1, "Regularity of verbs/adjectives");

--Assign numeric identifiers to all the states that a property may have

CREATE TABLE state_descriptions(
	stateID INTEGER PRIMARY KEY,
	state_description TEXT
);

INSERT INTO state_descriptions (stateID, state_description) VALUES (1, "Regular verb/adjective");
INSERT INTO state_descriptions (stateID, state_description) VALUES (2, "Irregular verb/adjective");

--This table defines the available properties (i.e. their valid states)

CREATE TABLE property_definitions(
	propID INTEGER NOT NULL,
	stateID INTEGER NOT NULL,

	PRIMARY KEY (propID, stateID),
	FOREIGN KEY (propID) REFERENCES property_descriptions (propID),
	FOREIGN KEY (stateID) REFERENCES state_descriptions (stateID)
);

INSERT INTO property_definitions (propID, stateID) VALUES (1,1);
INSERT INTO property_definitions (propID, stateID) VALUES (1,2);

--Assign one or more properties (each property with its state) to a word

CREATE TABLE properties(
	defnID INTEGER NOT NULL,
	propID INTEGER NOT NULL,
	stateID INTEGER NOT NULL,

	PRIMARY KEY (defnID, propID),
	FOREIGN KEY (defnID) REFERENCES definitions (defnID),
	FOREIGN KEY (propID, stateID) REFERENCES property_definitions (propID, stateID)
);
