#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
ファイルをアップロードする
'''
html = '''Content-Type: text/html

<html>
<head>
  <meta http-equiv="Content-Type" content="text/html" charset="UTF-8" />
  <title>ファイルをアップロードする</title>
</head>
<body>
<form action="post.py" method="post" enctype="multipart/form-data">
    <p>name:<input id="" name="name" type="text" /></p>
    <p>tag:<input id="" name="tag0" type="text" /></p>
    <p>tag:<input id="" name="tag1" type="text" /></p>
  <p>url:<input type="text" name="url" /></p>
  <p><input type="submit" /></p>
</form>
</body>
</html>
'''

import cgi
import os, sys
import sqlite3;
import datetime
import MySQLdb

user = "root";
password = "26nKZAzS";

result = ''
text = "";
if (os.environ.has_key("REQUEST_METHOD") == True and os.environ["REQUEST_METHOD"] == 'POST'):
    form = cgi.FieldStorage();
    url = form["url"].value;
    name = form["name"].value;
    i = 0;
    tags = [];
    while (form.has_key("tag" + str(i))):
        tags.append(form["tag" + str(i)].value);
        i += 1;
else:
    url = "https://docs.google.com/present/edit?id=0AcRZrHwgNrh1ZGNqNHJ2ZDlfNmRzOXR3ZmRq";
    name = "test";
    tags = ['test'];
connector = MySQLdb.connect(host="localhost", db='twippt', user=user, passwd=password);
cursor = connector.cursor();

cursor.execute("SELECT COUNT(id) FROM slide");
slide_id = cursor.fetchone()[0];
cursor.execute("INSERT INTO slide VALUES (%s, '%s', '%s')"% (slide_id, name, url));

tag_ids = [];

for tag in tags:
    cursor.execute("SELECT id FROM tag WHERE text = '%s'" % (tag,));
    row = cursor.fetchone();
    if (row == None):
        cursor.execute("SELECT COUNT(id) FROM tag");
        temp = cursor.fetchone();
        tag_ids.append(temp[0]);
        cursor.execute("INSERT INTO tag VALUES (%s, '%s')" % (temp[0], tag));
    else:
        tag_ids.append(row[0]);

for tag_id in tag_ids:
    cursor.execute("SELECT COUNT(id) FROM tag_slide_relation;");
    new_id = cursor.fetchone()[0];
    cursor.execute("INSERT INTO tag_slide_relation VALUES (%s, %s, %s)" % (new_id, slide_id, tag_id));

connector.commit();

print html;
