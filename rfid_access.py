#!/usr/bin/env python3
from Register import *
from Admin import *
from Stats import *
from List import *
import serial
import serial.serialutil
import id_call as call
import datetime
import time
from collections import Counter, OrderedDict


class App(tk.Frame):

    """Application Class"""

    def __init__(self, *args, **kwargs):
        global reg, enum, bdd
        tk.Frame.__init__(self, *args, **kwargs)

        # Setup 4 frames for the 4 pages of the application
        reg = Register(self)
        enum = List(self)
        stat = Stats(self)
        admin = Admin(self)
        call.id_call.enum = enum

        bdd = Page.get_bdd(enum)
        call.id_call.bdd = bdd

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
        stat_b = tk.Button(button_frame, text="Statistiques", width=20, height=1, command=stat.lift_stats,
                           font=BIG_FONT)
        admin_b = tk.Button(button_frame, text="Administration", width=20, height=1, command=admin.ask_password,
                            font=BIG_FONT)

        # Place all the buttons on the main windows
        reg_b.grid(row=0, column=0)
        enum_b.grid(row=0, column=1)
        stat_b.grid(row=0, column=2)
        admin_b.grid(row=0, column=3)
        enum.show()


def delete_window():

    """Function handle the close events"""

    bdd.close_db()
    root.destroy()


def is_in_list(listbox, name):

    """Check if a user is already in listbox"""

    i = 0
    list_val = listbox.get(0, tk.END)
    while i < len(list_val):
        if list_val[i] == name:
            return True, i
        i += 1
    return False, -1


def test_for_serial(win, ser, prev_id):

    """Listener for serial port"""

    listbox = List.get_list(call.id_call.enum)
    b = call.id_call.bdd

    # Try connection to serial port and handle fail
    if ser is None:
        try:
            ser = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=0)
        except serial.serialutil.SerialException:
            print("La connexion n'as pas pu être effectuée")
            ser = None

    # Read serial port
    if ser is not None:
        call.id_call.ser = ser
        try:
            id_card = "{}".format(ser.readline().decode("utf-8"))
            #print('\'' + id_card + '\'')
            try:
                # Get name by id_card
                int(id_card)
                name = b.get_name_by_id(id_card)
                print(name)
                if name is not None:
                    in_list, index = is_in_list(listbox, name)

                    # Store hour enter or leave
                    if prev_id != id_card and in_list is False:
                        listbox.insert(tk.END, name)
                        b.store_enter_by_id(id_card)
                    elif prev_id != id_card and in_list is True:
                        listbox.delete(index)
                        b.store_leave_by_id(id_card)

                    # Update other widgets
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

    # Recall the listener
    ret = win.after(500, test_for_serial, win, ser, prev_id)
    call.id_call.set_id_call(ret)


def get_unique_user(stats):

    """Return a list of unique user present in the previous day"""

    li = []
    for s in stats:
        li.append(s[1])
    li = list(set(li))
    return li


def update_database():

    """Compute stats from daily table and store it in annual table"""

    stats = bdd.get_daily_stats()

    bdd.create_annual_table()

    # Get timestamp from first line and compare the date
    date = datetime.datetime.now().strftime("%d-%m-%Y")
    try:
        base_stamp = stats[0][2]
    except IndexError:
        bdd.add_empty_line()
        return
    base_stamp = datetime.datetime.fromtimestamp(base_stamp).strftime("%d-%m-%Y")
    # print(date, base_stamp)

    if datetime.datetime.today().weekday() == 0:
        offset = 3600 * 24 * 2
    else:
        offset = 0
    future_date = datetime.datetime.fromtimestamp(time.time() - 3600 * 24 - offset).strftime("%d-%m-%Y")
    last_entries = bdd.sort_annual_table()
    try:
        last_date = last_entries[0][1]
    except IndexError:
        bdd.set_daily_stats(future_date, 0, 0, 0, None)
        bdd.clear_daily_table()
        bdd.add_empty_line()
        return
    if len(stats) == 1 and last_date != future_date:
        bdd.set_daily_stats(future_date, 0, 0, 0, None)
        bdd.clear_daily_table()
        bdd.add_empty_line()
        return

    # If date is yesterday, compute stats and store it
    if base_stamp != date:

        # Compute hour average
        moy = 0
        count = 1
        try:
            while count <= len(stats) - 1:
                moy += round(int(str(stats[count][3] - stats[count][2]).split('.')[0]) / 3600, 2)
                count += 1
        except TypeError:
            pass
        count -= 1
        try:
            moy /= count
        except ZeroDivisionError:
            bdd.set_daily_stats(base_stamp, 0, 0, 0, "")
            return

        # Get number of unique user the previous day
        uuser_list = get_unique_user(stats)
        nb_user = len(uuser_list)

        # Compute average age and most common town represented
        user_table = bdd.get_user_table()
        age = 0
        town_list = []
        for u in user_table:
            for i in uuser_list:
                if u[1] == i:
                    town_list.append(u[4])
                    age += u[2]
        age /= len(uuser_list)
        round(age, 1)
        town_dict = Counter(town_list)
        town_list = town_dict.most_common(2)
        #town_list = OrderedDict(sorted(town_dict.items(), key=lambda t: t[0]))
        print(town_dict, town_list)
#        i = 0
        town = town_list[0][0] + ' ' + town_list[1][0]
#        while i < 2 and i < len(town_list):
#            town += list(town_list)[i] + ' '
#            i += 1
        print(town)

        # Clear daily table and store data in annual
        bdd.set_daily_stats(base_stamp, nb_user, round(age, 1), round(moy, 2), town)
        bdd.clear_daily_table()
        bdd.add_empty_line()
        # print(base_stamp, nb_user, age, moy, town)


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
    img = tk.Image("photo", file=os.getenv("HOME") + "/.rfid_access/ressources/icon.gif")
    root.tk.call("wm", "iconphoto", root._w, img)

    # Handle windows close events
    root.protocol("WM_DELETE_WINDOW", delete_window)

    # Call listener to serial port
    root.after(1000, test_for_serial, root, None, 0)

    main = App(root)
    main.pack(side="top", fill="both", expand=True)
    update_database()

    root.mainloop()
