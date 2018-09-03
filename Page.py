import tkinter as tk
import Database as db

BIG_FONT = "arial 20"


class Page(tk.Frame):

    """Page class, all the page class inherit this one"""

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        self.bdd = db.Database()
        self.bdd.create_user_table()

    def get_bdd(self):

        """Return the bdd variable to use all the Database method"""

        return self.bdd

    def show(self):
        self.lift()
