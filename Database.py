import sqlite3 as sq


class Database:

    """Class for database navigation"""

    def __init__(self):
        self.conn = sq.connect("rfid_access.db")
        self.curs = self.conn.cursor()

    def create_user_table(self):
        self.curs.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY UNIQUE,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            age INT NOT NULL,
            class VARCHAR(20)
        )""")
        self.conn.commit()

    def delete_table(self, table):
        self.curs.execute("DROP TABLE " + table)
        self.conn.commit()

    def close_db(self):
        self.conn.close()
