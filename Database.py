import sqlite3 as sq
import time
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
            town VARCHAR(30),
            path VARCHAR(256)
        )""")
        self.conn.commit()

    def get_user_table(self):

        """Get all the 'user' database"""

        self.curs.execute("""SELECT * FROM users WHERE id is not 1""")
        users = self.curs.fetchall()
        return users

    def check_existing_user(self, name):

        """Return the number of occurence in the 'users' table"""

        self.curs.execute("""SELECT name FROM users WHERE name=?""", (name,))
        ret = self.curs.fetchall()
        return len(ret)

    def register_user(self, name, age, class_, path, id_card, town):

        """Register a user"""

        self.curs.execute("""INSERT INTO users(id, name, age, class, town, path) VALUES(?, ?, ?, ?, ?, ?)""",
                          (id_card, name, age, class_, town, path))
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

    def get_number_user(self):

        """Get the number of registered users"""

        self.curs.execute("""SELECT COUNT(*) FROM users""")
        nb_users = self.curs.fetchall()
        return nb_users[0][0]

    def get_name_by_id(self, id_card):

        """Get user by index"""

        self.curs.execute("""SELECT name FROM users WHERE id=?""", (id_card,))
        name = self.curs.fetchone()
        try:
            return name[0]
        except TypeError:
            return None

    def get_id_by_name(self, name):

        """Get user id by its name"""

        self.curs.execute("""SELECT id FROM users WHERE name=?""", (name,))
        id_card = self.curs.fetchone()
        return id_card[0]

    def get_age_by_id(self, id_card):

        """Get the user's age by its id"""

        self.curs.execute("""SELECT age FROM users WHERE id=?""", (id_card,))
        age = self.curs.fetchone()
        return age[0]

    def get_class_by_id(self, id_card):

        """Get the usser's class by its id"""

        self.curs.execute("""SELECT class FROM users WHERE id=?""", (id_card,))
        class_ = self.curs.fetchone()
        return class_[0]

    def create_daily_table(self):

        """Create if not exist the daily stat table"""

        self.curs.execute("""
        CREATE TABLE IF NOT EXISTS daily(
            id INTEGER,
            name VARCHAR(100),
            date_enter TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            date_leave TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            age INT NOT NULL,
            class VARCHAR(20)
        )""")
        self.conn.commit()
        self.create_log_table()

    def get_daily_stats(self):

        """Get all the data in the daily table"""

        self.curs.execute("""SELECT * FROM daily""")
        table = self.curs.fetchall()
        return table

    def store_hour_enter_by_id(self, id_card):

        """Store in the daily table the time when an user enter or leave using the id"""

        date = time.time()
        age = self.get_age_by_id(id_card)
        class_ = self.get_class_by_id(id_card)
        name = self.get_name_by_id(id_card)
        self.curs.execute("INSERT INTO daily(id, name, date_enter, date_leave, age, class) VALUES(?, ?, ?, ?, ?, ?)",
                          (id_card, name, date, None, age, class_))
        self.conn.commit()
        self.store_enter_log(id_card, name, date, age, class_)

    def store_hour_leave_by_id(self, id_card):

        """Store the leaving value in the table"""

        date = time.time()
        self.curs.execute("""SELECT * FROM daily WHERE id=?""", (id_card,))
        tab = self.curs.fetchall()
        tab_time = []
        for t in tab:
            tab_time.append(t[2])
        max_time = max(tab_time)
        self.curs.execute("UPDATE daily SET date_leave=? WHERE id=" + str(id_card) + " AND date_enter=" + str(max_time),
                          (date,))
        self.conn.commit()
        self.store_leave_log(id_card, max_time, date)

    def store_hour_enter_by_name(self, name):

        """Store the enter timestamp in the daily table using the name"""

        id_card = self.get_id_by_name(name)
        self.store_hour_enter_by_id(id_card)

    def store_hour_leave_by_name(self, name):

        """Store the leave timestamp in the daily table using the name"""

        id_card = self.get_id_by_name(name)
        self.store_hour_leave_by_id(id_card)

    def clear_daily_table(self):

        """Clear the daily table"""

        self.curs.execute("""DELETE FROM daily""")
        self.conn.commit()

    def create_annual_table(self):

        """Create the annual table"""

        self.curs.execute("""
        CREATE TABLE IF NOT EXISTS annual (
            date VARCHAR(20),
            nb_user INT NOT NULL,
            average_age INT NOT NULL,
            average_time REAL,
            town VARCHAR(30)
        )""")
        self.conn.commit()

    def set_daily_stats(self, date, nb_user, average_age, average_time, town):

        """Insert daily stats into the annual table"""

        self.curs.execute("INSERT INTO annual(date, nb_user, average_age, average_time, town) VALUES(?, ?, ?, ?, ?)",
                          (date, nb_user, average_age, average_time, town))
        self.conn.commit()

    def get_annual_table(self):

        """Get all the annual table"""

        self.curs.execute("""SELECT * FROM annual""")
        stats = self.curs.fetchall()
        return stats

    def clear_annual_table(self):

        """Clear the annual table"""

        self.curs.execute("""DELETE FROM annual""")
        self.conn.commit()

    def create_log_table(self):

        """Create if not exist the log table"""

        self.curs.execute("""
        CREATE TABLE IF NOT EXISTS log(
            id INTEGER,
            name VARCHAR(100),
            date_enter TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            date_leave TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            age INT NOT NULL,
            class VARCHAR(20)
        )""")
        self.conn.commit()

    def store_enter_log(self, id_card, name, date, age, class_):
        self.curs.execute("""INSERT INTO log(id, name, date_enter, date_leave, age, class) VALUES(?, ?, ?, ?, ?, ?)""",
                          (id_card, name, date, None, age, class_))
        self.conn.commit()

    def store_leave_log(self, id_card, max_time, date):
        self.curs.execute("UPDATE log SET date_leave=? WHERE id=" + str(id_card) + " AND date_enter=" + str(max_time),
                          (date,))
        self.conn.commit()

    def close_db(self):

        """Close the database"""

        self.conn.close()
