import sqlite3 as sq

conn = sq.connect("rfid_access.db")
curs = conn.cursor()
curs.execute("DROP TABLE users")
curs.execute("DROP TABLE daily")
curs.execute("DROP TABLE annual")
curs.execute("DROP TABLE log")
conn.commit()

conn.close()
