from Page import *


class Stats(Page):

    """Page where all the stats collected are listed"""

    def __init__(self, *args, **kwargs):
        global var_nb_user, bdd
        Page.__init__(self, *args, **kwargs)

        bdd = Page.get_bdd(self)

        # Init var for label
        var_nb_user = tk.StringVar()
        var_nb_user.set(str(bdd.get_number_user() - 1))

        # Init label
        label_nb_user = tk.Label(self, text="Nombre d'inscrits :", font=BIG_FONT)
        label_user_var = tk.Label(self, textvariable=var_nb_user, font=BIG_FONT)

        # Place elem on screen
        label_nb_user.place(in_=self, x=50, y=50)
        label_user_var.place(in_=self, x=300, y=50)

    @staticmethod
    def compute_daily_stat():
        stats = bdd.get_daily_stats()
        tab = []
        for s in stats:
            tab.append(s[2] - s[1])
        print(tab)

    def lift_stats(self):
        var_nb_user.set(str(bdd.get_number_user() - 1))
        self.compute_daily_stat()
        self.lift()
