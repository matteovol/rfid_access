import tkinter.messagebox as ms
import tkinter.filedialog as fd
import tkinter.ttk as ttk
from PIL import ImageTk
from PIL import Image
from Page import *


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
        button_valid = tk.Button(self, text="Valider", command=self.validate_entry, font=BIG_FONT)
        button_open = tk.Button(self, text="Importer une photo", command=lambda: self.open_pic(can), font=BIG_FONT)

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

    @staticmethod
    def validate_entry():
        """Check the entry validity and register the student"""
        name = var_name.get()
        first = var_first.get()
        age = var_age.get()
        class_ = var_class.get()
        if len(name) < 1 or len(first) < 1 or len(age) < 1 or len(class_) < 1 or len(file_name) < 1:
            ms.showerror("Error", "Veuillez remplir tout les champs avant de valider l'inscription")
        else:
            try:
                int(var_age.get())
            except ValueError:
                ms.showerror("Error", "Veuillez entrer un nombre dans la case \'Age\'")
            print(name, first, age, class_)

    @staticmethod
    def open_pic(can):
        """Open an image"""
        global file_name
        file_name = fd.askopenfilename(title="Ouvrir une image", filetypes=[("images files", ".png .jpg .bmp .gif")])
        if len(file_name) > 1:
            try:
                can.delete(image_list[0])
            except IndexError:
                pass
            print("'" + file_name + "'")
            try:
                pics = Image.open(file_name)
                if pics.width > 300:
                    ratio = pics.width / 300
                    pics = pics.resize((300, int(pics.height / ratio)), Image.ANTIALIAS)
                pics_resize = ImageTk.PhotoImage(pics)
                can.config(width=pics_resize.width(), height=pics_resize.height())
                image_list.append(can.create_image(0, 0, image=pics_resize, anchor=tk.NW))
                can.image = pics_resize
                pics.save(file_name[:len(file_name) - 4] + "_resized" + file_name[len(file_name) - 4:])
                pics.close()
            except IOError:
                ms.showerror("Error", "Une erreur s'est produite, essayez de recommencer la procédure ou de redémarrer"
                                      " le logiciel")
