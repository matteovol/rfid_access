import sqlite3 as sq

conn = sq.connect("rfid_access.db")
curs = conn.cursor()
ans = input("Delete users table? (y)").lower()
if ans == "y":
    try:
        curs.execute("DROP TABLE users")
    except sq.OperationalError:
        pass

table = ["daily", "annual", "log"]
for t in table:
    try:
        curs.execute("DROP TABLE " + t)
    except sq.OperationalError:
        pass
conn.commit()

conn.close()
