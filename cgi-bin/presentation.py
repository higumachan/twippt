#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import cgi
import json
import urllib
import datetime

html = '''Content-Type: text/html; charset=utf-8

<!DOCTYPE HTML>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<link rel="stylesheet" href="jslib/deck/core/deck.core.css">
	<link rel="stylesheet" href="jslib/deck/extensions/goto/deck.goto.css">
	<link rel="stylesheet" href="jslib/deck/extensions/menu/deck.menu.css">
	<link rel="stylesheet" href="jslib/deck/extensions/navigation/deck.navigation.css">
	<link rel="stylesheet" href="jslib/deck/extensions/status/deck.status.css">
	<link rel="stylesheet" href="jslib/deck/extensions/hash/deck.hash.css">
	<link rel="stylesheet" id="style-theme-link" href="jslib/deck/themes/style/web-2.0.css">
	<link rel="stylesheet" id="transition-theme-link" href="jslib/deck/themes/transition/horizontal-slide.css">
	<link rel="stylesheet"  href="css/main.css">
	<link rel="stylesheet"  href="css/present.css">
	<script src="js/jquery-1.6.4.min.js" type="text/javascript"></script>
	<script src="js/main2.js" type="text/javascript"></script>


	<script src="jslib/deck/modernizr.custom.js"></script>
</head>
<body class="present">
	
	<article class="deck-container" style="width: 100%; height: 100%"> 
	%s
	</article>
	<canvas id="layer2"  style="position: absolute; left: 0; top: 0; z-index: 10; width: 100%; height: 100%;"></canvas>
	<input type="button" id="draw_ctrl" value="on" onclick="toggle();" style="position: absolute; left: 0; bottom: 0; z-index: 101;"/>

	<!-- Grab CDN jQuery, with a protocol relative URL; fall back to local if offline -->
	<script srcjslib/deck//ajax.aspnetcdn.com/ajax/jQuery/jquery-1.7.min.js"></script>
	<script>window.jQuery || document.write('<script src="jslib/deck/jquery-1.7.min.js"><\/script>')</script>

	<!-- Deck Core and extensions -->
	<script src="jslib/deck/core/deck.core.js"></script>
	<script src="jslib/deck/extensions/hash/deck.hash.js"></script>
	<script src="jslib/deck/extensions/menu/deck.menu.js"></script>
	<script src="jslib/deck/extensions/goto/deck.goto.js"></script>
	<script src="jslib/deck/extensions/status/deck.status.js"></script>
	<script src="jslib/deck/extensions/navigation/deck.navigation.js"></script>

	<script type="text/javascript">
		$.deck(".slide");
	</script>
</body>
</html>
''';

form = cgi.FieldStorage();
try:
    name = form["name"];
except:
    name = 'tekito';

connector = sqlite3.connect("test.db");
cursor = connector.cursor();

cursor.execute("SELECT text FROM slide WHERE name = '%s';" % (name,));
text = cursor.fetchone()[0];

print html % (text,);

