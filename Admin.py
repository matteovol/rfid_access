from Page import *
from hashlib import sha256
import tkinter.messagebox as ms
from tkinter import ttk
import tkinter.filedialog as fd


class Admin(Page):
    """Administration page, a password is required to enter this page"""

    def __init__(self, *args, **kwargs):
        global var_actual, var_new, var_confirm, bdd
        Page.__init__(self, *args, **kwargs)

        bdd = Page.get_bdd(self)

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
        button_export_users = tk.Button(self, text="Exporter la table utilisateur\nen CSV", width=22, font=BIG_FONT,
                                        command=self.export_user)
        button_export_an = tk.Button(self, text="Exporter la table des\nstatistiques en CSV", width=22, font=BIG_FONT,
                                     command=self.export_annual)
        button_stat_a = tk.Button(self, text="Réinitialiser les statistiques\nannuelles", width=22, font=BIG_FONT,
                                  command=self.delete_annual)
        button_stat_u = tk.Button(self, text="Supprimer un usager", width=22, height=2, font=BIG_FONT,
                                  command=lambda: self.delete_user(self))
        button_stat_ua = tk.Button(self, text="Supprimer tout les usagers", width=22, height=2, font=BIG_FONT,
                                   command=self.delete_all_users)
        button_stat_pass = tk.Button(self, text="Changer le mot de passe", width=22, font=BIG_FONT,
                                     command=lambda: self.change_password())

        # Place elements on screen
        button_export_users.place(in_=self, x=100, y=70)
        button_export_an.place(in_=self, x=100, y=180)
        button_stat_a.place(in_=self, x=100, y=290)
        button_stat_u.place(in_=self, x=100, y=400)
        button_stat_ua.place(in_=self, x=100, y=510)
        label_title.place(in_=self, x=650, y=60)
        label_actual.place(in_=self, x=600, y=120)
        entry_actual.place(in_=self, x=600, y=170)
        label_new.place(in_=self, x=600, y=210)
        entry_new.place(in_=self, x=600, y=260)
        label_confirm.place(in_=self, x=600, y=300)
        entry_confirm.place(in_=self, x=600, y=350)
        button_stat_pass.place(in_=self, x=700, y=400)

        # Setup the tab order (navigation in widget using the tab button)
        new_order = (button_export_users, button_export_an, button_stat_a, button_stat_u, button_stat_ua, entry_actual,
                     entry_new, entry_confirm, button_stat_pass)
        for w in new_order:
            w.lift()

    def ask_password(self):

        """Create a window to ask password and grant access to admin's page"""

        # Check if an admin password is set
        ret = bdd.check_admin_password()
        if ret is True:
            # Setup the window
            _password = ""
            win_pass = tk.Tk()
            win_pass.title("")
            width = 200
            height = 100
            ws = win_pass.winfo_screenwidth()
            hs = win_pass.winfo_screenheight()
            x = (ws / 2) - (width / 2)
            y = (hs / 2) - (height / 2)
            win_pass.geometry("{}x{}+{}+{}".format(width, height, int(x), int(y)))
            win_pass.resizable(height=False, width=False)
            win_pass.iconbitmap("ressources/icon.ico")
            pwd_entry = tk.Entry(win_pass, show='*')

            def on_ok():

                """Check the password's validity"""

                global _password
                _password = pwd_entry.get()
                hash_admin = bdd.get_admin_hash()
                hash_passwd = sha256(_password.encode()).hexdigest()
                if str(hash_passwd) == hash_admin:
                    self.lift()
                else:
                    ms.showerror("Error", "Bad password")
                win_pass.destroy()

            tk.Label(win_pass, text="Mot de passe:").pack()
            pwd_entry.pack(side="top")
            pwd_entry.bind("<Return>", lambda ok: on_ok())
            tk.Button(win_pass, command=on_ok, text="OK").pack(side="top")
            win_pass.mainloop()

    @staticmethod
    def delete_annual():

        """Delete values from the annual table"""

        rep = ms.askquestion("Question", "Voulez vous supprimer les statistiques anuelles")
        if rep == "yes":
            bdd.clear_annual_table()
            ms.showinfo("Info", "Les statistiques annuelles ont été supprimées")

    @staticmethod
    def export_user():

        """Export user table to csv file, can be imported to excel"""

        file_name = fd.asksaveasfilename(title="Enregistrer les utilisateurs",
                                         filetypes=[("csv files", ".csv "), ("text files", ".txt"),
                                                    ("all files", "*.*")])
        file = open(file_name, "w")
        users = bdd.get_user_table()
        file.write("id,name,age,classe,commune\n")
        for u in users:
            i = 0
            while i < len(u) - 1:
                file.write(str(u[i]) + ",")
                i += 1
            file.write("\n")
        file.close()

    @staticmethod
    def export_annual():

        """Export annual stat table to CSV file, can be imported in Excel"""

        file_name = fd.asksaveasfilename(title="Enregistrer les statistiques",
                                         filetypes=[("csv files", "*.csv"), ("text files", "*.txt"),
                                                    ("all files", "*.*")])
        file = open(file_name, "w")
        stats = bdd.get_annual_table()
        file.write("id,date,nomdre utilisateur,age moyen,temps moyen,commune\n")
        for s in stats:
            i = 0
            while i < len(s):
                file.write(str(s[i]) + ",")
                i += 1
            file.write("\n")
        file.close()

    @staticmethod
    def get_values():

        """Get all the registered user from the database"""

        values = []
        name = bdd.get_names()
        i = 1
        while i < len(name):
            values.append(name[i][0])
            i += 1
        return values

    @staticmethod
    def delete_user(self):

        """Open a window to choose an user to delete from the database"""

        # Setup window
        win_del = tk.Tk()
        win_del.title("")
        width = 200
        height = 100
        ws = win_del.winfo_screenwidth()
        hs = win_del.winfo_screenheight()
        x = (ws / 2) - (width / 2)
        y = (hs / 2) - (height / 2)
        win_del.geometry("{}x{}+{}+{}".format(width, height, int(x), int(y)))
        win_del.resizable(height=False, width=False)
        win_del.iconbitmap("ressources/icon.ico")

        def delete(name):
            """Delete the user from table and show an information message"""

            bdd.delete_user(name)
            ms.showinfo("Info", "L'utilisateur {} a été supprimé de la liste".format(name))
            win_del.destroy()

        values = self.get_values()
        combo = ttk.Combobox(win_del, values=values, state="readonly")
        tk.Label(win_del, text="Quel utilisateur faut-il supprimer ?").pack()
        combo.pack()
        tk.Button(win_del, text="Valider", command=lambda: delete(combo.get())).pack()
        win_del.mainloop()

    @staticmethod
    def delete_all_users():

        """Ask the user to delete all the user in the 'users' table"""

        rep = ms.askquestion("Question", "Voulez vous vraiment vider la liste des utilisateurs ?")
        if rep == "yes":
            bdd.delete_table("users")
            ms.showinfo("Info", "La liste des utilisateurs a été vidée")

    @staticmethod
    def change_password():

        """Change the password on the admin page"""

        actual = var_actual.get()
        new = var_new.get()
        confirm = var_confirm.get()
        hash_admin = bdd.get_admin_hash()
        hash_actual = str(sha256(actual.encode()).hexdigest())
        if hash_actual == hash_admin:
            if new == confirm:
                hash_new = str(sha256(new.encode()).hexdigest())
                bdd.change_admin_password(hash_new)
                ms.showinfo("Mot de passe", "Le mot de passe administrateur a été changé")
            else:
                ms.showerror("Error", "Les nouveaux mots de passe ne correspondent pas")
        else:
            ms.showerror("Error", "Le mot de passe administrateur ne correspond pas")
        var_actual.set("")
        var_new.set("")
        var_confirm.set("")
