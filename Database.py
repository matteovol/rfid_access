import sqlite3 as sq
import tkinter as tk
from hashlib import sha256


class Database:

    """Class for database navigation"""

    def __init__(self):
        self.conn = sq.connect("rfid_access.db")
        self.curs = self.conn.cursor()

    def create_user_table(self):

        """Create the 'users' table if it doesn't exist"""

        self.curs.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY UNIQUE,
            name VARCHAR(100),
            age INT NOT NULL,
            class VARCHAR(20),
            path VARCHAR(256)
        )""")
        self.conn.commit()

    def check_existing_user(self, name):

        """Return the number of occurence in the 'users' table"""

        self.curs.execute("""SELECT name FROM users WHERE name=?""", (name,))
        ret = self.curs.fetchall()
        return len(ret)

    def register_user(self, name, age, class_, path):

        """Register a user"""

        self.curs.execute("""INSERT INTO users(name, age, class, path) VALUES(?, ?, ?, ?)""",
                          (name, age, class_, path))
        self.conn.commit()

    def delete_user(self, name):

        """Delete the user 'name'"""

        self.curs.execute("""DELETE FROM users WHERE name=?""", (name,))
        self.conn.commit()

    def delete_table(self, table):

        """Delete all the user from the 'users' table (except the admin password)"""

        self.curs.execute("DELETE FROM " + table + " WHERE name!='admin'")
        self.conn.commit()

    def check_admin_password(self):

        """Check the admin password"""

        self.curs.execute("""SELECT name, path FROM users WHERE name=?""", ("admin",))
        rep = self.curs.fetchone()
        if rep is None:

            # Setup the window to set admin password
            win_set_pass = tk.Tk()
            win_set_pass.title("")
            width = 400
            height = 100
            ws = win_set_pass.winfo_screenwidth()
            hs = win_set_pass.winfo_screenheight()
            x = (ws / 2) - (width / 2)
            y = (hs / 2) - (height / 2)
            win_set_pass.geometry("{}x{}+{}+{}".format(width, height, int(x), int(y)))
            win_set_pass.resizable(height=False, width=False)
            win_set_pass.iconbitmap("ressources/icon.ico")
            pwd_entry = tk.Entry(win_set_pass, show='*')

            def on_ok():

                """Hash password and store it in the table"""

                passwd = pwd_entry.get()
                hash_passwd = sha256(passwd.encode()).hexdigest()
                self.curs.execute("""INSERT INTO users(name, age, path) VALUES(?, ?, ?)""",
                                  ("admin", 1, str(hash_passwd)))
                self.conn.commit()
                win_set_pass.destroy()

            tk.Label(win_set_pass, text="Aucun mot de passe administrateur n'est défini, veuillez en entrer un:").pack()
            pwd_entry.pack(side="top")
            pwd_entry.bind('<Return>', lambda ok: on_ok())
            tk.Button(win_set_pass, command=lambda ok: on_ok(), text="OK").pack(side="top")
            win_set_pass.mainloop()
            return False
        else:
            return True

    def get_admin_hash(self):

        """Get the admin hash"""

        self.curs.execute("""SELECT path FROM users WHERE name=?""", ("admin",))
        admin_hash = self.curs.fetchone()
        return admin_hash[0]

    def change_admin_password(self, passwd):

        """Update the admin password"""

        self.curs.execute("""UPDATE users SET path=? WHERE name='admin'""", (passwd,))
        self.conn.commit()

    def get_names(self):

        """Get name from all the users"""

        self.curs.execute("""SELECT name FROM users""")
        tab_name = self.curs.fetchall()
        return tab_name

    def create_daily_table(self):

        """Create if not exist the daily stat table"""

        self.curs.execute("""
        CREATE TABLE IF NOT EXISTS daily(
            id INTEGER PRIMARY KEY UNIQUE,
            date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            age INT NOT NULL,
            class VARCHAR(20)
        )""")
        self.conn.commit()

    def close_db(self):

        """Close the database"""

        self.conn.close()
