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
<h1>ファイルをアップロードする</h1>
<p>%s</p>
<form action="post.py" method="post" enctype="multipart/form-data">
    <p><input id="" name="name" type="text" /></p>
    <p><input id="" name="tag" type="text" /></p>
  <p><input type="file" name="file" /></p>
  <p><input type="submit" /></p>
</form>
</body>
</html>
'''

import cgi
import os, sys
import sqlite3;
import datetime

result = ''
text = "";
if (os.environ.has_key("REQUEST_METHOD") == False or os.environ["REQUEST_METHOD"] == 'POST'):
    form = cgi.FieldStorage();
    item = form["file"];
    tag = form["tag"].value;
    name = form["name"].value;

    for row in item.file:
        text += row;
    connector = sqlite3.connect("test.db");
    cursor = connector.cursor();

    cursor.execute("SELECT COUNT(id) FROM slide");
    new_id = cursor.fetchone()[0] + 1;
    now = datetime.datetime.now();
    now = now.replace(microsecond=0);
    connector.execute("INSERT INTO slide VALUES(%s, '%s', '%s', '%s', '%s')" % (new_id, name, tag, text, now.isoformat()));
    connector.commit();

print html % result
