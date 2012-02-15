#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import cgi
import json
import urllib
import datetime

form = cgi.FieldStorage();
try:
    max_id = long(form["max_id"].value);
    tag = form["tag"].value;
except:
    #ago_time = datetime.datetime(2012, 2, 11);
    max_id = 168517232924700673;
    tag = "test";
#ago_time -= datetime.timedelta(seconds=20);
s = urllib.urlopen("http://search.twitter.com/search.json?q=\#%s" % (tag,)).read();
d = json.loads(s);
results = d["results"]

print "Content-Type: text/html; charset=utf-8"
print "";

res = {"texts": [], "max_id": 0};
for result in results:
#    print max_id, result["id"];
#    print max_id == result["id"];
    if (max_id == result["id"]):
        break;
    res["texts"].append(result["text"]);

res["max_id"] = d["max_id_str"];
print json.dumps(res);

