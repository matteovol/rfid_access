#!/usr/bin/env python3

import time
import datetime
import tkinter.filedialog as fd
from tkinter import ttk
import tkinter as tk
import tkinter.messagebox as ms
from dateutil import tz
import Database as db

FONT = "arial 15"


class App(tk.Frame):

    """class for main frame"""

    def __init__(self, *args, **kwargs):
        global var_combo, var_entry, bdd
        tk.Frame.__init__(self, *args, **kwargs)

        bdd = db.Database()

        # Setup browser
        var_combo = tk.StringVar()
        var_entry = tk.StringVar()
        label_title = tk.Label(self, text="Chercher par date ou par nom :", font=FONT)
        label_entry = tk.Label(self, text="Date (JJ-MM-AAAA) ou Nom (Prénom Nom):", font=FONT)
        combo = ttk.Combobox(self, textvariable=var_combo, font=FONT, state="readonly", values=("Date", "Nom"),
                             width=24)
        entry_browse = tk.Entry(self, textvariable=var_entry, font=FONT, width=24)
        button_validate = tk.Button(self, text="Chercher et exporter", font=FONT, command=self.validate)

        # Place elements on screen
        label_title.place(in_=self, x=50, y=10)
        combo.place(in_=self, x=50, y=40)
        label_entry.place(in_=self, x=50, y=100)
        entry_browse.place(in_=self, x=50, y=130)
        button_validate.place(in_=self, x=50, y=200)

    @staticmethod
    def export_by_date(search):

        """Export log information searched by date in a csv file"""

        # Set timezones values
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        fmt_time = "%H:%M:%S"

        search = search.split('-')
        if len(search) == 3 and search[0].isdigit() and int(search[0]) <= 31 and search[1].isdigit() and int(search[1]) <= 12 and search[2].isdigit():
            stamp = time.mktime(datetime.datetime.strptime('-'.join(search), "%d-%m-%Y").timetuple())
            table = bdd.get_log_by_date(stamp)
            if len(table) < 1:
                ms.showerror("Erreur", "La date saisie ne possède pas d'occurence")
                return
            file_name = fd.asksaveasfilename(title="Enregistrer les données",
                                             filetypes=[("csv files", "*.csv"), ("text files", "*.txt"),
                                                        ("all files", "*.*")])
            fstream = open(file_name, "w")
            fstream.write("nom,date_enter,date_leave\n")
            for t in table:
                fstream.write(t[1] + ',' + datetime.datetime.utcfromtimestamp(t[2]).replace(tzinfo=from_zone).astimezone(to_zone).strftime(fmt_time) + ',' +
                              datetime.datetime.utcfromtimestamp(t[3]).replace(tzinfo=from_zone).astimezone(to_zone).strftime(fmt_time) + '\n')
        else:
            ms.showerror("Error", "La date est erronée")
            return

    @staticmethod
    def export_by_name(search):

        """Export log information searched by name in a csv file"""

        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        fmt_time = "%H:%M:%S"
        fmt_date = "%d-%m-%Y"
        search = search.split(' ')
        if len(search) >= 2 and search[0].isalpha() and search[1].isalpha():
            tab = bdd.get_log_by_name(' '.join(search))
            if len(tab) < 1:
                ms.showerror("Erreur", "Le nom saisi n'est pas présent")
                return
            file_name = fd.asksaveasfilename(title="Enregistrer les données",
                                             filetypes=[("csv files", "*.csv"), ("text files", "*.txt"),
                                                        ("all files", "*.*")])
            fstream = open(file_name, "w")
            fstream.write("date,time_enter,time_leave\n")
            for t in tab:
                fstream.write(datetime.datetime.utcfromtimestamp(t[2]).replace(tzinfo=from_zone).astimezone(to_zone).strftime(fmt_date) + ',' +
                           datetime.datetime.utcfromtimestamp(t[2]).replace(tzinfo=from_zone).astimezone(to_zone).strftime(fmt_time) + ',' +
                           datetime.datetime.utcfromtimestamp(t[3]).replace(tzinfo=from_zone).astimezone(to_zone).strftime(fmt_time) + '\n')
        else:
            ms.showerror("Erreur", "Le nom saisi est erroné")
            return

    def validate(self):

        """Choose an export method depending on searched information"""

        mode = var_combo.get()
        search = var_entry.get()
        if mode == "Date":
            self.export_by_date(search)
        elif mode == "Nom":
            self.export_by_name(search)


def delete_window():

    """Destroy window and quit application on close"""

    root.destroy()


if __name__ == '__main__':
    # Setup the main window
    root = tk.Tk()

    # Setup windows size and position
    root.title("Trouver un utilisateur")
    width = 500
    height = 300
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws / 2) - (width / 2)
    y = (hs / 2) - (height / 2)
    root.geometry("{}x{}+{}+{}".format(width, height, int(x), int(y)))
    root.resizable(width=False, height=False)

    # Handle windows close events
    root.protocol("WM_DELETE_WINDOW", delete_window)

    main = App(root)
    main.pack(side="top", fill="both", expand=True)

    root.mainloop()
