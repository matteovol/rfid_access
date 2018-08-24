from Page import *


class Admin(Page):

    """Administration page, a password is required to enter this page"""

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        # Init Label
        label_title = tk.Label(self, text="Changer le mot de passe administrateur", font=BIG_FONT)
        label_actual = tk.Label(self, text="Mot de passe actuel:", font=BIG_FONT)
        label_new = tk.Label(self, text="Nouveau mot de passe:", font=BIG_FONT)
        label_confirm = tk.Label(self, text="Confirmation du nouveau mot de passe:", font=BIG_FONT)

        # Init buttons
        button_stat_h = tk.Button(self, text="Réinitialiser les statistiques\nhebdomadaires", width=22, font=BIG_FONT)
        button_stat_a = tk.Button(self, text="Réinitialiser les statistiques\nannuelles", width=22, font=BIG_FONT)
        button_stat_u = tk.Button(self, text="Supprimer un usager", width=22, height=2, font=BIG_FONT)
        button_stat_ua = tk.Button(self, text="Supprimer tout les usagers", width=22, height=2, font=BIG_FONT)
        button_stat_pass = tk.Button(self, text="Changer le mot de passe", font=BIG_FONT)

        # Place elements on screen
        button_stat_h.place(in_=self, x=100, y=100)
        button_stat_a.place(in_=self, x=100, y=210)
        button_stat_u.place(in_=self, x=100, y=320)
        button_stat_ua.place(in_=self, x=100, y=430)
        label_title.place(in_=self, x=600, y=100)
        label_actual.place(in_=self, x=600, y=100)
        label_new.place(in_=self, x=600, y=100)
        label_confirm.place(in_=self, x=600, y=100)
        button_stat_pass.place(in_=self, x=500, y=500)

    def ask_password(self):
        _password = ""
        win_pass = tk.Tk()
        win_pass.geometry("200x100")
        win_pass.resizable(height=False, width=False)
        win_pass.iconbitmap("questhead")
        pwd_entry = tk.Entry(win_pass, show='*')

        def on_pwd_entry(_evt):
            global _password
            _password = pwd_entry.get()
            self.lift()
            win_pass.destroy()

        def on_ok_click():
            global _password
            _password = pwd_entry.get()
            self.lift()
            win_pass.destroy()

        tk.Label(win_pass, text="Mot de passe:").pack()
        pwd_entry.pack(side="top")
        pwd_entry.bind('<Return>', on_pwd_entry)
        tk.Button(win_pass, command=on_ok_click, text="OK").pack(side="top")
