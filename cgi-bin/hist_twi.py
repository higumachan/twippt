#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
import sys
import os
import cgi
import datetime
import json

try:
    start = form['start'].value;
    end = form['end'].value;
    name = form["name"].value;
except:
    start = '2011-12-06T00:00:00';
    end = '2011-12-06T1:00:00';
    name = 'tekito';
connector = sqlite3.connect("test.db");
cursor = connector.cursor();
cursor.execute("SELECT COUNT(time), time FROM tweet WHERE time > '%s' AND time < '%s' AND name = '%s' GROUP BY time;" % (start, end, name));
rows = cursor.fetchall();
s = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S");
e = datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S");

result = {"chart_data":[]};
dic = {};
for row in rows:
    delta = datetime.datetime.strptime(row[1], "%Y-%m-%dT%H:%M:%S") - s; 
    dic[delta.seconds] = row[0];
for i in range((e - s).seconds):
    if (dic.has_key(i) == True):
        result["chart_data"].append((i, dic[i]));
    else:
        result["chart_data"].append((i, 0));
    
print "Content-Type: text/html; charset=utf-8"
print "";
print json.dumps(result);
