import tkinter.messagebox as ms
import tkinter.filedialog as fd
import tkinter.ttk as ttk
from PIL import ImageTk
from PIL import Image
from Page import *
import os
import id_call as call
import serial
from main import test_for_serial


class Register(Page):

    """Register page. The inscription form must be fully completed to register someone"""

    def __init__(self, *args, **kwargs):
        global var_age, var_class, var_first, var_name, image_list, file_name
        Page.__init__(self, *args, **kwargs)
        image_list = []
        file_name = ""

        # Declare all label of the inscription form
        label_name = tk.Label(self, text="Nom:", font=BIG_FONT)
        label_first = tk.Label(self, text="Prénom:", font=BIG_FONT)
        label_age = tk.Label(self, text="Age:", font=BIG_FONT)
        label_class = tk.Label(self, text="Classe:", font=BIG_FONT)
        label_name.focus_set()

        # StringVar to get the values set in the inscription form
        var_name = tk.StringVar()
        var_first = tk.StringVar()
        var_age = tk.StringVar()
        var_class = tk.StringVar()

        # Entry text to fill form
        entry_name = tk.Entry(self, textvariable=var_name, font=BIG_FONT)
        entry_first = tk.Entry(self, textvariable=var_first, font=BIG_FONT)
        entry_age = tk.Entry(self, textvariable=var_age, font=BIG_FONT)

        # Dropdown list to chose the student's
        values = ["6ème", "5ème", "4ème", "3ème", "Seconde", "Première", "Terminale", "Autre"]
        combo = ttk.Combobox(self, width=19, font=BIG_FONT, textvariable=var_class, values=values, state="readonly")

        # create the image frame and canvas
        frame = tk.Frame(self, bd=2, relief=tk.RAISED, height=400, width=300, bg="gray")
        can = tk.Canvas(frame, width=300, height=400)
        frame.grid_propagate(0)

        # Buttons present in this page
        button_valid = tk.Button(self, text="Valider", command=lambda: self.validate_entry(can, self), font=BIG_FONT)
        button_open = tk.Button(self, text="Importer une photo", command=lambda: self.open_pic(can, self), font=BIG_FONT)

        # Print all elements on the Register frame
        label_name.place(in_=self, x=100, y=80)
        entry_name.place(in_=self, x=100, y=120)
        label_first.place(in_=self, x=100, y=170)
        entry_first.place(in_=self, x=100, y=210)
        label_age.place(in_=self, x=100, y=260)
        entry_age.place(in_=self, x=100, y=300)
        label_class.place(in_=self, x=100, y=350)
        combo.place(in_=self, x=100, y=390)
        frame.place(in_=self, x=600, y=50)
        button_open.place(in_=self, x=623, y=470)
        button_valid.place(in_=self, x=150, y=540)
        can.pack()

        # Set a new widget order
        new_order = (entry_name, entry_first, entry_age, combo, button_open, button_valid)
        for w in new_order:
            w.lift()

    @staticmethod
    def get_id_card():
        while True:
            if call.id_call.ser is not None:
                try:
                    id_card = "{}".format(call.id_call.ser.readline().decode("utf-8"))
                    print('\'' + id_card + '\'')
                    try:
                        int(id_card)
                        return id_card
                    except ValueError:
                        pass
                except serial.serialutil.SerialException:
                    print("Data could not be read")

    @staticmethod
    def validate_entry(can, self):

        """Check the entry validity and register the student"""

        last = var_name.get()
        first = var_first.get()
        age = var_age.get()
        class_ = var_class.get()
        root = call.id_call.get_root()
        root.after_cancel(call.id_call.get_id_call())
        if len(last) < 1 or len(first) < 1 or len(age) < 1 or len(class_) < 1 or len(file_name) < 1:
            ms.showerror("Error", "Veuillez remplir tout les champs avant de valider l'inscription")
        else:
            try:
                int(var_age.get())
            except ValueError:
                ms.showerror("Error", "Veuillez entrer un nombre dans la case \'Age\'")
                return
            name = first + " " + last
            card_id = self.get_id_card()
            print(name, age, class_, final_dir, card_id)
            bdd = Page.get_bdd(self)
            ret = bdd.check_existing_user(name)
            if ret != 0:
                name = name + " ({})".format(ret)
            bdd.register_user(name, age, class_, final_dir, card_id)
            ms.showinfo("Info", "L'inscription est validée")
            var_name.set("")
            var_first.set("")
            var_age.set("")
            var_class.set("")
            can.delete(image_list[0])
            call.id_call.root.after(1000, test_for_serial, root, call.id_call.ser, 0)

    @staticmethod
    def open_pic(can, self):

        """Open an image and store a resized version in a folder"""

        global file_name, final_dir
        file_name = fd.askopenfilename(title="Ouvrir une image", filetypes=[("images files", ".png .jpg .bmp .gif")])
        if len(var_name.get()) < 1 or len(var_first.get()) < 1:
            ms.showerror("Erreur", "Veuillez d'abord remplir les champs à gauche")
            return
        if len(file_name) > 1:
            # Delete an existing image in the canvas
            try:
                can.delete(image_list[0])
            except IndexError:
                pass

            # Open the image and resize it to 300px width
            try:
                pics = Image.open(file_name)
                if pics.width > 300:
                    ratio = pics.width / 300
                    pics = pics.resize((300, int(pics.height / ratio)), Image.ANTIALIAS)
                pics_resize = ImageTk.PhotoImage(pics)
                can.config(width=pics_resize.width(), height=pics_resize.height())
                image_list.append(can.create_image(0, 0, image=pics_resize, anchor=tk.NW))
                can.image = pics_resize

                # Create the folder
                try:
                    os.mkdir("pics")
                except IOError:
                    pass

                # Save the file
                cur_dir = os.getcwd()
                name = var_first.get() + " " + var_name.get()
                bdd = Page.get_bdd(self)
                ret = bdd.check_existing_user(name)
                if ret != 0:
                    name = name + " ({})".format(ret)
                final_dir = cur_dir + "\pics\\" + name + file_name[len(file_name) - 4:]
                pics.save(final_dir)
                pics.close()

            except IOError:
                ms.showerror("Error", "Une erreur s'est produite, essayez de recommencer la procédure ou de redémarrer"
                                      + " le logiciel")
