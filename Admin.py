from Page import *


class Admin(Page):

    """Administration page, a password is required to enter this page"""

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        # Init Label
        label = tk.Label(self, text="Changer le mot de passe administrateur")

        # Init buttons
        button_stat_h = tk.Button(self, text="Réinitialiser les statistiques hebdomadaires")
        button_stat_a = tk.Button(self, text="Réinitialiser les statistiques annuelles")
        button_stat_u = tk.Button(self, text="Supprimer un usager")
        button_stat_ua = tk.Button(self, text="Supprimer tout les usagers")
        button_stat_pass = tk.Button(self, text="Changer le mot de passe")

        # Place elements on screen
        button_stat_h.place(in_=self, x=100, y=100)
        label.pack()