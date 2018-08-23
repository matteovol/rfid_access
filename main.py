from Register import *
from Admin import *
from Stats import *
from List import *


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

        # Setup all the 4 buttons to switch between the 4 pages
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
    # Setup the main window
    root = tix.Tk()
    root.title("Gestion des usagers")
    root.geometry("1280x720")
    root.resizable(width=False, height=False)
    main = App(root)
    main.pack(side="top", fill="both", expand=True)
    root.mainloop()
