import sqlite3 as sq
import tkinter as tk
import hashlib as hash


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
            class VARCHAR(20),
            path VARCHAR(100)
        )""")
        self.conn.commit()

    def register_user(self, first_name, last_name, age, class_, path):
        self.curs.execute("""INSERT INTO users(first_name, last_name, age, class, path) VALUES(?, ?, ?, ?, ?)""",
                          (first_name, last_name, age, class_, path))
        self.conn.commit()

    def delete_table(self, table):
        self.curs.execute("DROP TABLE " + table)
        self.conn.commit()

    def check_admin_password(self):
        self.curs.execute("""SELECT first_name, last_name FROM users WHERE first_name=?""", ("admin",))
        rep = self.curs.fetchone()
        if rep is None:
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
                passwd = pwd_entry.get()
                hash_passwd = hash.sha256(passwd.encode())
                self.curs.execute("""INSERT INTO users(first_name, last_name, age) VALUES(?, ?, ?)""",
                                  ("admin", str(hash_passwd), 1))
                self.conn.commit()
                win_set_pass.destroy()

            tk.Label(win_set_pass, text="Aucun mot de passe administrateur n'est défini, veuillze en entrer un:").pack()
            pwd_entry.pack(side="top")
            pwd_entry.bind('<Return>', lambda self: on_ok())
            tk.Button(win_set_pass, command=lambda self: on_ok(), text="OK").pack(side="top")
            win_set_pass.mainloop()
            return False
        else:
            return True

    def close_db(self):
        self.conn.close()
