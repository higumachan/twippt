#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import cgi
import json
import urllib
import datetime
import MySQLdb

html = '''Content-Type: text/html; charset=utf-8

<!DOCTYPE HTML>
<html lang="jp">
<head>
	<meta charset="UTF-8">
	<title></title>
	<script src="/js/jquery-1.6.4.min.js" type="text/javascript"></script>
	<script src="/js/main2.js" type="text/javascript"></script>
</head>
<body style="background-color: black">
	<iframe src="%s" name="test" height="100\%" width="100\%" style="position: absolute; left: 0; top: 0; z-index: 0;"></iframe>
	<canvas id="layer2" onclick="top.test.focus()" style="position: absolute; left: 0; top: 0; z-index: 1; width: 100\%; height: 100\%;"></canvas>
	<input type="button" id="draw_ctrl" value="on" onclick="toggle(); top.test.focus()" style="position: absolute; left: 0; bottom: 0; z-index: 2;"/>
</body>
</html>
''';

form = cgi.FieldStorage();
try:
    name = form["name"].value;
except:
    name = 'nadeko';

connector = MySQLdb.connect(host="localhost", db='twippt', user="root", passwd="26nKZAzS", charset="utf8");
cursor = connector.cursor();

cursor.execute("SELECT url FROM slide WHERE name = '%s'" % (name,));
row =  cursor.fetchone();
if (row != None):
    url = row[0];
else:
    url = "http://Notfound"

print '''Content-Type: text/html; charset=utf-8

<!DOCTYPE HTML>
<html lang="jp">
<head>
	<meta charset="UTF-8">
	<title></title>
	<script src="/js/jquery-1.6.4.min.js" type="text/javascript"></script>
    <script src="/jslib/lib.js" type="text/javascript"></script>
	<script src="/js/main2.js" type="text/javascript"></script>
</head>
<body style="background-color: black">
	<iframe src=" ''' + url + '''" name="test" height="100%" width="100%" style="position: absolute; left: 0; top: 0; z-index: 0;"></iframe>
	<canvas id="layer2" onclick="top.test.focus()" style="position: absolute; left: 0; top: 0; z-index: 1; width: 100%; height: 100%;"></canvas>
	<input type="button" id="draw_ctrl" value="on" onclick="toggle(); top.test.focus()" style="position: absolute; left: 0; bottom: 0; z-index: 2;"/>
</body>
</html>
''';
