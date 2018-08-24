from Page import *


class List(Page):

    """Page where all the presents users are listed"""

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        # Init invisible frame to place correctly the list
        fr1 = tk.Frame(self, width=1, height=50)
        fr1.grid(row=0, column=1)
        fr2 = tk.Frame(self, width=50, height=1)
        fr2.grid(row=1, column=0)

        # Init scrollable list
        scroll = tk.Scrollbar(self, orient=tk.VERTICAL)
        scroll.grid(row=1, column=2, sticky=tk.NS, rowspan=50)
        listbox = tk.Listbox(self, yscrollcommand=scroll.set, width=50, height=16, font=BIG_FONT)
        for i in range(1000):
            listbox.insert(tk.END, str(i))
        listbox.grid(row=1, column=1, rowspan=50)
        scroll.config(command=listbox.yview)

        # Init invisible frames to place in the grid
        fr3 = tk.Frame(self, width=20, height=1)
        fr3.grid(row=1, column=3)
        fr4 = tk.Frame(self, width=1, height=15)
        fr4.grid(row=3, column=4)
        fr5 = tk.Frame(self, width=1, height=25)
        fr5.grid(row=5, column=4)
        fr6 = tk.Frame(self, width=1, height=15)
        fr6.grid(row=8, column=4)

        # Init labels
        label_add = tk.Label(self, text="Ajouter un élève à la liste", font=BIG_FONT)
        label_del = tk.Label(self, text="Retirer un élève de la liste", font=BIG_FONT)

        # Init var for entry
        var_add = tk.StringVar()
        var_del = tk.StringVar()

        # Init entry
        entry_add = tk.Entry(self, textvariable=var_add, font=BIG_FONT)
        entry_del = tk.Entry(self, textvariable=var_del, font=BIG_FONT)

        # Init buttons to interact with the list
        button_add = tk.Button(self, text="Ajouter", font=BIG_FONT, command=self.add_to_list)
        button_del = tk.Button(self, text="Retirer", font=BIG_FONT, command=self.del_from_list)

        # Setup widgets on the screen
        label_add.grid(row=1, column=4)
        entry_add.grid(row=2, column=4)
        button_add.grid(row=4, column=4)
        label_del.grid(row=6, column=4)
        entry_del.grid(row=7, column=4)
        button_del.grid(row=9, column=4)

    def add_to_list(self):
        pass

    def del_from_list(self):
        pass
