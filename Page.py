import tkinter as tk
import Database as db

BIG_FONT = "arial 17"


class Page(tk.Frame):

    """Page class, all the page class inherit this one"""

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        # Init the database and call the function to create them
        self.bdd = db.Database()
        self.bdd.create_user_table()
        self.bdd.create_daily_table()

    def get_bdd(self):

        """Return the bdd variable to use all the Database method"""

        return self.bdd

    def show(self):

        """Show the page, can be replaced by another function in children object"""

        self.lift()
