from Page import *


class List(Page):

    """Page where all the presents users are listed"""

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="Présence")
        label.pack()
