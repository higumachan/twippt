import sqlite3
# OUT: Traceback (most recent call last):
# OUT:   File "<input>", line 1, in <module>
# OUT: TypeError: Required argument 'database' (pos 1) not found
connector = sqlite3.connect("test.db")
cursor = connector.cursor();

cursor.execute("SELECT * FROM tweet")
print cursor.fetchall();
