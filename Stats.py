from Page import *


class Stats(Page):

    """Page when all the stats collected are listed"""

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        # Init var for label
        var_nb_user = tk.StringVar()

        var_nb_user.set("0")

        # Init label
        label_nb_user = tk.Label(self, text="Nombre d'inscrits :", font=BIG_FONT)
        label_user_var = tk.Label(self, textvariable=var_nb_user, font=BIG_FONT)

        # Place elem on screen
        label_nb_user.place(in_=self, x=50, y=50)
        label_user_var.place(in_=self, x=300, y=50)
