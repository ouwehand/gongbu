BEGIN TRANSACTION;

.mode csv

CREATE TABLE raw_data (
	kor1 TEXT,
	kor2 TEXT,
	kor3 TEXT,
	eng3 TEXT,
	eng2 TEXT,
	eng1 TEXT
);

.import korean_cards_dump.csv raw_data
.mode column

UPDATE raw_data SET kor1=NULL WHERE kor1="NULL";
UPDATE raw_data SET kor2=NULL WHERE kor2="NULL";
UPDATE raw_data SET kor3=NULL WHERE kor3="NULL";
UPDATE raw_data SET eng1=NULL WHERE eng1="NULL";
UPDATE raw_data SET eng2=NULL WHERE eng2="NULL";
UPDATE raw_data SET eng3=NULL WHERE eng3="NULL";


INSERT into definitions (korean, english)
	SELECT kor1, eng1 from raw_data WHERE kor1 NOT NULL AND eng1 NOT NULL;

INSERT into definitions (korean, english)
	SELECT kor2, eng2 from raw_data WHERE kor2 NOT NULL AND eng2 NOT NULL;

INSERT into definitions (korean, english)
	SELECT kor3, eng3 from raw_data WHERE kor3 NOT NULL AND eng3 NOT NULL;

DROP TABLE raw_data;


--Assign a few labels and properties, only for demonstration purposes
--The labels/properties in the current database are by no means complete

INSERT INTO labels (defnID, lblID) SELECT defnID, 1 FROM definitions WHERE english="to write";
INSERT INTO labels (defnID, lblID) SELECT defnID, 1 FROM definitions WHERE english="to read";
INSERT INTO labels (defnID, lblID) SELECT defnID, 1 FROM definitions WHERE english="to listen";

INSERT INTO properties (defnID, propID, stateID) SELECT defnID, 1, 2 FROM definitions WHERE english="spicy";
INSERT INTO properties (defnID, propID, stateID) SELECT defnID, 1, 2 FROM definitions WHERE english="to listen";

INSERT INTO definitions (korean, english) VALUES ("입다", "to wear");
INSERT INTO properties (defnID, propID, stateID) SELECT defnID, 1, 1 FROM definitions WHERE english="to wear";

--De-couple a few Korean homonyms

DELETE FROM definitions WHERE korean="밤";
INSERT INTO definitions (korean, english) VALUES ("밤", "night"),
                                                 ("밤", "chestnut");

DELETE FROM definitions WHERE korean="병";
INSERT INTO definitions (korean, english) VALUES ("병", "bottle"),
                                                 ("병", "illness");

--Not a true homonym, but an abbreviation

DELETE FROM definitions WHERE korean="차";
INSERT INTO definitions (korean, english) VALUES ("차", "tea"),
                                                 ("차 / 자동차", "car");

--Add a few more Korean homonyms

INSERT INTO definitions (korean, english) VALUES ("쓰다", "to wear something on the head (hat or glasses)"),
                                                 ("쓰다", "bitter");

COMMIT;
