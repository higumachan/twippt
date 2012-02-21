import sqlite3
import sys

connector = sqlite3.connect("test.db");

args = sys.argv;
file_name = args[1];

f = open(file_name);

sql = "";
for row in f:
    sql += row;

connector.execute(sql);
connector.commit();

connector.close();
