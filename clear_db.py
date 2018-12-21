#!/usr/bin/env python3

import sqlite3 as sq
import os

# Connect to database
conn = sq.connect(os.getenv("HOME") + "/.rfid_access/rfid_access.db")
curs = conn.cursor()

# Ask for permisison to delete user table
ans = input("Delete users table? (y)").lower()
if ans == "y":
    try:
        curs.execute("DROP TABLE users")
    except sq.OperationalError:
        pass

# Delete other tables
table = ["daily", "annual", "log"]
for t in table:
    try:
        curs.execute("DROP TABLE " + t)
    except sq.OperationalError:
        pass
conn.commit()

conn.close()
