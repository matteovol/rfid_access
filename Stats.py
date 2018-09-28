from Page import *
from tkinter import ttk
import calendar


class Stats(Page):

    """Page where all the stats collected are listed"""

    def __init__(self, *args, **kwargs):
        global var_nb_user, bdd, var_combo, var_mon, var_tue, var_wen, var_thi, var_fri
        Page.__init__(self, *args, **kwargs)

        bdd = Page.get_bdd(self)

        # Init var for label
        var_nb_user = tk.StringVar()
        var_nb_user.set(str(bdd.get_number_user() - 1))
        var_title = tk.StringVar()
        var_title.set("Statistique sur la semaine passée")
        var_mon = tk.StringVar()
        var_tue = tk.StringVar()
        var_wen = tk.StringVar()
        var_thi = tk.StringVar()
        var_fri = tk.StringVar()
        var_combo = tk.StringVar()

        # Init label
        label_nb_user = tk.Label(self, text="Nombre d'inscrits :", font=BIG_FONT)
        label_user_var = tk.Label(self, textvariable=var_nb_user, font=BIG_FONT)
        label_title = tk.Label(self, textvariable=var_title, font=BIG_FONT)
        label_mon = tk.Label(self, text="Lundi :", font=BIG_FONT)
        label_tue = tk.Label(self, text="Mardi :", font=BIG_FONT)
        label_wen = tk.Label(self, text="Mercredi :", font=BIG_FONT)
        label_thi = tk.Label(self, text="Jeudi :", font=BIG_FONT)
        label_fri = tk.Label(self, text="Vendredi :", font=BIG_FONT)
        label_val_mon = tk.Label(self, textvariable=var_mon, font=BIG_FONT)
        label_val_tue = tk.Label(self, textvariable=var_tue, font=BIG_FONT)
        label_val_wen = tk.Label(self, textvariable=var_wen, font=BIG_FONT)
        label_val_thi = tk.Label(self, textvariable=var_thi, font=BIG_FONT)
        label_val_fri = tk.Label(self, textvariable=var_fri, font=BIG_FONT)

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
        label_val_mon.place(in_=self, x=650, y=150)
        label_val_tue.place(in_=self, x=650, y=250)
        label_val_wen.place(in_=self, x=650, y=350)
        label_val_thi.place(in_=self, x=650, y=450)
        label_val_fri.place(in_=self, x=650, y=550)
        combo_stat.place(in_=self, x=50, y=150)
        button_validate.place(in_=self, x=134, y=220)

    @staticmethod
    def validate():
        to_see = var_combo.get()
        if len(to_see) < 1:
            return
        tab_first = bdd.sort_annual_table()
        tab_date = []
        for t in tab_first:
            tab_date.append(t[1].split("-"))
        day = []
        for i in tab_date:
            day.append(calendar.weekday(int(i[2]), int(i[1]), int(i[0])))
        first = None
        i = 0
        while i < len(day):
            if day[i] == 4:
                first = i
                break
            i += 1
        week_tab = []
        if first is not None:
            last = first + 5
            while first < last:
                try:
                    week_tab.append(tab_first[first])
                except IndexError:
                    pass
                first += 1
        tab_day = [var_mon, var_tue, var_wen, var_thi, var_fri]
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
                    d.set(str(int(float(week_tab[i][j]))) + "h" + str(int(int(week_tab[i][j].split('.')[1]) * 60 / 100)))
                else:
                    d.set(week_tab[i][j])
            except IndexError:
                pass
            i -= 1

    def lift_stats(self):
        var_nb_user.set(str(bdd.get_number_user() - 1))
        self.lift()
