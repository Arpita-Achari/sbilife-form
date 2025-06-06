import sqlite3

conn = sqlite3.connect('sbilife.db')
c = conn.cursor()
c.execute("SELECT * FROM customers")
rows = c.fetchall()
for row in rows:
    print(row)
conn.close()
