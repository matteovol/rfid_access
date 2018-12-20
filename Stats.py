import datetime
import tkinter.messagebox as ms
from Page import *
from tkinter import ttk


class Stats(Page):

    """Page where all the stats collected are listed"""

    def __init__(self, *args, **kwargs):

        """Init method for Stats class"""

        global var_nb_user, bdd, var_combo, var_val_d1, var_val_d2, var_val_d3, var_val_d4, var_val_d5, var_d1, var_d2, var_d3, var_d4, var_d5
        Page.__init__(self, *args, **kwargs)

        bdd = Page.get_bdd(self)

        # Init var for label
        var_nb_user = tk.StringVar()
        var_nb_user.set(str(bdd.get_number_user() - 1))
        var_title = tk.StringVar()
        var_title.set("Statistique des 5 derniers jours d'ouverture")
        var_val_d1 = tk.StringVar()
        var_val_d2 = tk.StringVar()
        var_val_d3 = tk.StringVar()
        var_val_d4 = tk.StringVar()
        var_val_d5 = tk.StringVar()
        var_d1 = tk.StringVar()
        var_d2 = tk.StringVar()
        var_d3 = tk.StringVar()
        var_d4 = tk.StringVar()
        var_d5 = tk.StringVar()
        var_combo = tk.StringVar()

        # Init label
        label_nb_user = tk.Label(self, text="Nombre d'inscrits :", font=BIG_FONT)
        label_user_var = tk.Label(self, textvariable=var_nb_user, font=BIG_FONT)
        label_title = tk.Label(self, textvariable=var_title, font=BIG_FONT)
        label_mon = tk.Label(self, textvariable=var_d1, font=BIG_FONT)
        label_tue = tk.Label(self, textvariable=var_d2, font=BIG_FONT)
        label_wen = tk.Label(self, textvariable=var_d3, font=BIG_FONT)
        label_thi = tk.Label(self, textvariable=var_d4, font=BIG_FONT)
        label_fri = tk.Label(self, textvariable=var_d5, font=BIG_FONT)
        label_val_mon = tk.Label(self, textvariable=var_val_d1, font=BIG_FONT)
        label_val_tue = tk.Label(self, textvariable=var_val_d2, font=BIG_FONT)
        label_val_wen = tk.Label(self, textvariable=var_val_d3, font=BIG_FONT)
        label_val_thi = tk.Label(self, textvariable=var_val_d4, font=BIG_FONT)
        label_val_fri = tk.Label(self, textvariable=var_val_d5, font=BIG_FONT)

        # Init combobox
        values = ("Age moyen", "Commune", "Nombre d'utilisateur", "Temps moyen")
        combo_stat = ttk.Combobox(self, font=BIG_FONT, textvariable=var_combo, state="readonly", values=values)

        # Init buttons
        button_validate = tk.Button(self, text="Visualiser", command=self.validate, font=BIG_FONT)

        # Place elem on screen
        label_nb_user.place(in_=self, x=50, y=50)
        label_user_var.place(in_=self, x=300, y=50)
        label_title.place(in_=self, x=700, y=50)
        label_mon.place(in_=self, x=500, y=150)
        label_tue.place(in_=self, x=500, y=250)
        label_wen.place(in_=self, x=500, y=350)
        label_thi.place(in_=self, x=500, y=450)
        label_fri.place(in_=self, x=500, y=550)
        label_val_mon.place(in_=self, x=850, y=150)
        label_val_tue.place(in_=self, x=850, y=250)
        label_val_wen.place(in_=self, x=850, y=350)
        label_val_thi.place(in_=self, x=850, y=450)
        label_val_fri.place(in_=self, x=850, y=550)
        combo_stat.place(in_=self, x=50, y=150)
        button_validate.place(in_=self, x=134, y=220)

    @staticmethod
    def validate():

        """Display stats when validate button is pressed"""

        to_see = var_combo.get()
        if len(to_see) < 1:
            return
        tab_first = bdd.sort_annual_table()
        tab_day = [var_val_d1, var_val_d2, var_val_d3, var_val_d4, var_val_d5]
        j = 0
        if to_see == "Age moyen":
            j = 3
        elif to_see == "Commune":
            j = 5
        elif to_see == "Nombre d'utilisateur":
            j = 2
        elif to_see == "Temps moyen":
            j = 4
        i = 4
        for d in tab_day:
            try:
                if j == 4:
                    d.set('{0:02.0f}h{1:02.0f}'.format(*divmod(tab_first[i][j] * 60, 60)))
                else:
                    d.set(tab_first[i][j])
            except IndexError:
                ms.showerror("Error", "Pas asser de donnees pour les 5 derniers jours")
                return
            i -= 1

    @staticmethod
    def set_days(tab_first):

        """Select last five dates and weekday to display in stat frame"""

        global var_d1, var_d2, var_d3, var_d4, var_d5
        tab_day = [var_d1, var_d2, var_d3, var_d4, var_d5]
        weekday = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
        i = 4
        j = 1
        for d in tab_day:
            split = tab_first[i][j].split('-')
            curr_day = datetime.datetime(int(split[2]), int(split[1]), int(split[0]))
            try:
                temp = weekday[curr_day.weekday()] + "\t" + tab_first[i][j] + ":"
            except IndexError:
                ms.showerror("Error", "Pas asser de donnees pour les 5 derniers jours")
            d.set(temp)
            i -= 1

    def lift_stats(self):

        """Update stats frame and display it"""

        var_nb_user.set(str(bdd.get_number_user() - 1))
        tab_days = bdd.sort_annual_table()
        self.set_days(tab_days)
        self.lift()
