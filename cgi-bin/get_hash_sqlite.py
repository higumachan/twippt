import sqlite3
import json
import sys
import cgi


connector = sqlite3.connect();
cursor = sqlite3.cursor();

cursor.execute("SELECT text FROM twitter_tag WHERE flag = 'false'");
connector.execute("UPDATE twitter_tag SET flag = 'true' WHERE flag = 'false'");

