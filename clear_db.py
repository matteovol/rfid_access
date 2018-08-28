import sqlite3 as sq

conn = sq.connect("rfid_access.db")
curs = conn.cursor()
curs.execute("DROP TABLE users")
conn.commit()

conn.close()
