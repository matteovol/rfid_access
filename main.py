from Register import *
from Admin import *
from Stats import *
from List import *
import serial
import serial.serialutil
import id_call as call


class App(tk.Frame):

    """Application Class"""

    def __init__(self, *args, **kwargs):
        global reg, enum
        tk.Frame.__init__(self, *args, **kwargs)

        # Setup 4 frames for the 4 pages of the application
        reg = Register(self)
        enum = List(self)
        stat = Stats(self)
        admin = Admin(self)
        call.id_call.enum = enum

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
        enum_b = tk.Button(button_frame, text="Liste", width=19, height=1, command=enum.lift_list, font=BIG_FONT)
        stat_b = tk.Button(button_frame, text="Statistiques", width=20, height=1, command=stat.lift_stats, font=BIG_FONT)
        admin_b = tk.Button(button_frame, text="Administration", width=20, height=1, command=admin.ask_password,
                            font=BIG_FONT)

        # Place all the buttons on the main windows
        reg_b.grid(row=0, column=0)
        enum_b.grid(row=0, column=1)
        stat_b.grid(row=0, column=2)
        admin_b.grid(row=0, column=3)
        reg.show()


def _delete_window(ouais):
    pass


def is_in_list(listbox, name):
    i = 0
    list_val = listbox.get(0, tk.END)
    while i < len(list_val):
        if list_val[i] == name:
            return True, i
        i += 1
    return False, -1


def test_for_serial(win, ser, prev_id):
    listbox = List.get_list(call.id_call.enum)
    bdd = Page.get_bdd(call.id_call.enum)

    if ser is None:
        try:
            ser = serial.Serial("COM4", baudrate=9600, timeout=0)
        except serial.serialutil.SerialException:
            print("La connexion n'as pas pu être effectuée")
            ser = None

    if ser is not None:
        call.id_call.ser = ser
        try:
            id_card = "{}".format(ser.readline().decode("utf-8"))
            print('\'' + id_card + '\'')
            try:
                int(id_card)
                name = bdd.get_name_by_id(id_card)
                print(name)
                if name is not None:
                    in_list, index = is_in_list(listbox, name)

                    if prev_id != id_card and in_list is False:
                        listbox.insert(tk.END, name)
                        bdd.store_hour_enter_by_id(id_card)
                    elif prev_id != id_card and in_list is True:
                        listbox.delete(index)
                        bdd.store_hour_leave_by_id(id_card)
                    val_list = listbox.get(0, tk.END)
                    combo_del = List.get_combo(call.id_call.enum)
                    combo_del.config(values=val_list)
                    prev_id = id_card
            except ValueError:
                prev_id = 0
                pass
        except serial.serialutil.SerialException:
            print("Data could not be read")
            ser = None
    ret = win.after(500, test_for_serial, win, ser, prev_id)
    call.id_call.set_id_call(ret)


if __name__ == "__main__":
    # Setup the main window
    root = tk.Tk()
    call.id_call.set_root(root)

    # Setup windows size and position
    root.title("Identification RFID")
    width = 1280
    height = 720
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws / 2) - (width / 2)
    y = (hs / 2) - (height / 2)
    root.geometry("{}x{}+{}+{}".format(width, height, int(x), int(y)))
    root.resizable(width=False, height=False)

    root.iconbitmap("ressources/icon.ico")
    root.bind("<Destroy>", _delete_window)
    root.after(1000, test_for_serial, root, None, 0)

    main = App(root)
    main.pack(side="top", fill="both", expand=True)

    root.mainloop()
