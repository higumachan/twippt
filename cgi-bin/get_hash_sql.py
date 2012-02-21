#!/usr/bin/python

import json
import sys
import cgi
import MySQLdb

connector = MySQLdb.connect(host="localhost", db='twippt', user="root", passwd="26nKZAzS");
cursor = connector.cursor();

form = cgi.FieldStorage();

try:
    name = form["name"].value;
    slide = form["slide"].value;
except:
    name = "tekito";
    slide = "0";

cursor.execute("SELECT id FROM slide WHERE name = '%s'" % (name,));
slide_id = cursor.fetchone[0];
#cursor.execute("SELECT id FROM tag WHERE IN (SELECT tag_id FROM tag_slide_relation WHERE slide_id = '%s')" % (slide_id,));
#temp = cursor.fetchall();
#tag_ids = [t[0] for t in temp];
#tag_ids = tuple(tag_ids);
#cursor.execute("SELECT tweet_id FROM tag_slide_relation WHERE IN (%s)" % (str(tag_ids),));
#tweet_ids = tuple([t[0] for t in cursor.fetchall()]);
#cursor.execute("SELECT text FROM tweet WHERE flag = 'false' AND IN (%s)" % (str(tweet_ids,)));
cursor.execute("SELECT text FROM tweet WHERE flag = 'false' AND slide_id = %s" % (slide_id,));

rows = cursor.fetchall();

cursor.execute("UPDATE tweet SET flag = 'true' WHERE flag = 'false' AND slide_id = %s" % (slide_id,));

connector.commit();

cursor.close();
connector.close();

result = {"texts": []};
for row in rows:
    result["texts"].append(row[0]);

print "Content-Type: text/html; charset=utf-8"
print "";
print json.dumps(result);
