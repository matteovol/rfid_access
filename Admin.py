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

        # Init StringVar for Entry
        var_actual = tk.StringVar()
        var_new = tk.StringVar()
        var_confirm = tk.StringVar()

        # Init Entry
        entry_actual = tk.Entry(self, font=BIG_FONT, textvariable=var_actual, show='*', width=40)
        entry_new = tk.Entry(self, font=BIG_FONT, textvariable=var_new, show='*', width=40)
        entry_confirm = tk.Entry(self, font=BIG_FONT, textvariable=var_confirm, show='*', width=40)

        # Init buttons
        button_stat_h = tk.Button(self, text="Réinitialiser les statistiques\nhebdomadaires", width=22, font=BIG_FONT,
                                  command=self.delete_hebdo)
        button_stat_a = tk.Button(self, text="Réinitialiser les statistiques\nannuelles", width=22, font=BIG_FONT,
                                  command=self.delete_annual)
        button_stat_u = tk.Button(self, text="Supprimer un usager", width=22, height=2, font=BIG_FONT,
                                  command=self.delete_user)
        button_stat_ua = tk.Button(self, text="Supprimer tout les usagers", width=22, height=2, font=BIG_FONT,
                                   command=self.delete_all_users)
        button_stat_pass = tk.Button(self, text="Changer le mot de passe", width=22, font=BIG_FONT,
                                     command=self.change_password)

        # Place elements on screen
        button_stat_h.place(in_=self, x=100, y=100)
        button_stat_a.place(in_=self, x=100, y=210)
        button_stat_u.place(in_=self, x=100, y=320)
        button_stat_ua.place(in_=self, x=100, y=430)
        label_title.place(in_=self, x=650, y=60)
        label_actual.place(in_=self, x=600, y=120)
        entry_actual.place(in_=self, x=600, y=170)
        label_new.place(in_=self, x=600, y=210)
        entry_new.place(in_=self, x=600, y=260)
        label_confirm.place(in_=self, x=600, y=300)
        entry_confirm.place(in_=self, x=600, y=350)
        button_stat_pass.place(in_=self, x=700, y=400)

        # Setup the tab order (navigation in widget using the tab button)
        new_order = (button_stat_h, button_stat_a, button_stat_u, button_stat_ua, entry_actual, entry_new,
                     entry_confirm, button_stat_pass)
        for w in new_order:
            w.lift()

    def ask_password(self):
        _password = ""
        win_pass = tk.Tk()
        width = 200
        height = 100
        ws = win_pass.winfo_screenwidth()
        hs = win_pass.winfo_screenheight()
        x = (ws / 2) - (width / 2)
        y = (hs / 2) - (height / 2)
        win_pass.geometry("{}x{}+{}+{}".format(width, height, int(x), int(y)))
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

    @staticmethod
    def delete_annual():
        pass

    @staticmethod
    def delete_hebdo():
        pass

    @staticmethod
    def delete_user():
        pass

    @staticmethod
    def delete_all_users():
        pass

    @staticmethod
    def change_password():
        pass
