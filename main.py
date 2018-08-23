import tkinter as tk
import tkinter.messagebox as ms
import tkinter.tix as tix
import tkinter.filedialog as fd
import tkinter.font as font

BIG_FONT = "arial 20"
MEDUIM_FONT = "arial 20"


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


class Register(Page):

    """Register page. The inscription form must be fully completed to register someone"""

    def __init__(self, *args, **kwargs):
        global var_age, var_class, var_first, var_name
        Page.__init__(self, *args, **kwargs)

        # Declare all label of the inscription form
        label_name = tk.Label(self, text="Nom:", font=MEDUIM_FONT)
        label_first = tk.Label(self, text="Prénom:", font=MEDUIM_FONT)
        label_age = tk.Label(self, text="Age:", font=MEDUIM_FONT)
        label_class = tk.Label(self, text="Classe:", font=MEDUIM_FONT)
        label_name.focus_set()

        # StringVar to get the values set in the inscription form
        var_name = tk.StringVar()
        var_first = tk.StringVar()
        var_age = tk.StringVar()
        var_class = tk.StringVar()

        # Entry text to fill form
        entry_name = tk.Entry(self, textvariable=var_name, font=MEDUIM_FONT)
        entry_first = tk.Entry(self, textvariable=var_first, font=MEDUIM_FONT)
        entry_age = tk.Entry(self, textvariable=var_age, font=MEDUIM_FONT)

        # Dropdown list to chose the student's
        bigfont = font.Font(family="Arial", size=15)
        combo = tix.ComboBox(self, editable=1, dropdown=1, variable=var_class)
        combo.entry.config(state="readonly")
        root.option_add("TCombobox*Listbox*Font", bigfont)
        combo.insert(0, "6ème")
        combo.insert(1, "5ème")
        combo.insert(2, "4ème")
        combo.insert(3, "3ème")
        combo.insert(4, "Seconde")
        combo.insert(5, "Première")
        combo.insert(6, "Terminale")
        combo.insert(7, "Autre")

        # create the image frame
        frame = tk.Frame(self, bd=2, relief=tk.RAISED, height=400, width=300, bg="gray")
        frame.grid_propagate(0)

        # Buttons present in this page
        button_valid = tk.Button(self, text="Valider", command=self.validate_entry, font=MEDUIM_FONT)
        button_open = tk.Button(self, text="Ouvrir une photo", command=lambda: self.open_pic(frame), font=MEDUIM_FONT)

        # Print all elements on the Register frame
        label_name.place(in_=self, x=100, y=80)
        entry_name.place(in_=self, x=100, y=120)
        label_first.place(in_=self, x=100, y=170)
        entry_first.place(in_=self, x=100, y=210)
        label_age.place(in_=self, x=100, y=260)
        entry_age.place(in_=self, x=100, y=300)
        label_class.place(in_=self, x=100, y=350)
        combo.place(in_=self, x=100, y=390)
        button_valid.place(in_=self, x=150, y=440)
        frame.place(in_=self, x=600, y=50)
        button_open.place(in_=self, x=700, y=470)

    @staticmethod
    def validate_entry():
        """Check the entry validity and register the student"""
        name = var_name.get()
        first = var_first.get()
        age = var_age.get()
        class_ = var_class.get()
        if len(name) < 1 or len(first) < 1 or len(age) < 1 or len(class_) < 1:
            ms.showerror("Error", "Veuillez remplir tout les champs avant de valider l'inscription")
        else:
            try:
                int(var_age.get())
            except ValueError:
                ms.showerror("Error", "Veuillez entrer un nombre dans la case \'Age\'")
            print(name, first, age, class_)

    @staticmethod
    def open_pic(frame):
        """Open an image"""
        file_name = fd.askopenfilename(title="Ouvrir une image", filetypes=[("png files", ".png"), ("all files", ".*")])
        pics = tk.PhotoImage(file=file_name)
        can = tk.Canvas(frame, width=pics.width(), height=pics.height(), bg="white")
        can.create_image(0, 0, image=pics, anchor=tk.NW)
        can.pack()


class List(Page):

    """Page where all the presents users are listed"""

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="Présence")
        label.pack()


class Stats(Page):

    """Page when all the stats collected are listed"""

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="Statistiques")
        label.pack()


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


class App(tk.Frame):

    """Application Class"""

    def __init__(self, *args, **kwargs):
        global reg
        tk.Frame.__init__(self, *args, **kwargs)

        # Setup 4 frames for the 4 pages of the application
        reg = Register(self)
        enum = List(self)
        stat = Stats(self)
        admin = Admin(self)

        button_frame = tk.Frame(self)
        container = tk.Frame(self)
        button_frame.pack(side="top", fill='x', expand=False)
        container.pack(side="top", fill="both", expand=True)

        # Place all the 4 frames on the main windows, they are superimposed
        reg.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        enum.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        stat.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        admin.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        # Setup all the 4 buttons to switxh between the 4 pages
        reg_b = tk.Button(button_frame, text="Inscription", width=19, height=1, command=reg.lift, font=BIG_FONT)
        enum_b = tk.Button(button_frame, text="Liste", width=19, height=1, command=enum.lift, font=BIG_FONT)
        stat_b = tk.Button(button_frame, text="Statistiques", width=20, height=1, command=stat.lift, font=BIG_FONT)
        admin_b = tk.Button(button_frame, text="Administration", width=20, height=1, command=admin.lift, font=BIG_FONT)

        # Place all the buttons on the main windows
        reg_b.grid(row=0, column=0)
        enum_b.grid(row=0, column=1)
        stat_b.grid(row=0, column=2)
        admin_b.grid(row=0, column=3)
        reg.show()


if __name__ == "__main__":
    global root
    # Setup the main window
    root = tix.Tk()
    root.title("Gestion des usagers")
    root.geometry("1280x720")
    root.resizable(width=False, height=False)
    main = App(root)
    main.pack(side="top", fill="both", expand=True)
    root.mainloop()
