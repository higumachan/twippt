#!/usr/bin/python

import sqlite3
import json
import sys
import cgi


connector = sqlite3.connect("test.db");
cursor = connector.cursor();

form = cgi.FieldStorage();
try:
    tag = form["tag"].value;
    slide = form["slide"].value;
except:
    tag = "tekito";
    slide = "0";
cursor.execute("SELECT text FROM tweet WHERE flag = 'false' AND tag = '%s';" % (tag,));
rows = cursor.fetchall();
connector.execute("UPDATE tweet SET flag = 'true', slide = %s WHERE flag = 'false' AND tag = '%s';" % (slide, tag));

connector.commit();

cursor.close();
connector.close();

result = {"texts": []};
for row in rows:
    result["texts"].append(row[0]);

print "Content-Type: text/html; charset=utf-8"
print "";
print json.dumps(result);

