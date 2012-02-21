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
    <p><input id="" name="name" type="text" /></p>
    <p><input id="" name="tag" type="text" /></p>
  <p><input type="text" name="url" /></p>
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
if (os.environ.has_key("REQUEST_METHOD") == False or os.environ["REQUEST_METHOD"] == 'POST'):
    form = cgi.FieldStorage();
    url = form["url"].value;
    name = form["name"].value;
    i = 0;
    while (form.has_key("tag" + str(i))):
        tags.append(form["tag" + str(i)].value);
        i += 1;

    connector = MySQLdb.connect(host="localhost", db='twippt', user=user, passwd=password);
    cursor = connector.cursor();
    
    cursor.execute("SELECT COUNT(id) FORM slide;");
    slide_id = cursor.fetchone()[0];
    cursor.execute("INSERT INTO slide VALUES (%s, '%s', '%s')"% (slide_id, name, url));
    
    tag_ids = [];

    for tag in tags:
        cursor.execute("SELECT id FROM tag WHERE text = '%s'" % (tag,));
        row = cursor.fetchone();
        if (row == None):
            cursor.execute("SELECT COUNT(id) FROM tag");
            tag_ids.append(row[0]);
            cursor.execute("INSERT INTO tag VALUES (%s, '%s')" % (row[0], tag));
        else:
            tag_ids.append(row[0]);
    
    for tag_id in tag_ids:
        cursor.execute("SELECT COUNT(id) FORM tag_slide_relation;");
        new_id = cursor.fetchone()[0];
        cursor.execute("INSERT INTO tag_slide_relation VALUES (%s, %s, %s)" % (new_id, slide_id, tag_id));

    connector.commit();

print html % result;
