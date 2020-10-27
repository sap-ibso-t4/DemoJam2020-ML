import sqlite3

conn = sqlite3.connect('material.db')
c = conn.cursor()

cursor = c.execute('SELECT * FROM ENGINE')
for row in cursor:
    print(row)

conn.close()