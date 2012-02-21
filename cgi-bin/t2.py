import sqlite3

con = sqlite3.connect("../test.db");

con.execute("""
CREATE TABLE slide (
	id INTEGER,
	name CHAR(255),
	tag CHAR(255),
	text NTEXT,
    time DATETIME
)""");


con.commit();

