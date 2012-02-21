import sqlite3

con = sqlite3.connect("../test.db");

con.execute("""
CREATE TABLE tweet (
	tag CHAR(255),
    flag BOOLEAN,
	text CHAR (300),
	slide INTEGER,
	id INTEGER,
	name CHAR(255),
    time DATETIME
)""");


con.commit();

