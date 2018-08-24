from Page import *


class Stats(Page):

    """Page when all the stats collected are listed"""

    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="Statistiques")
        label.pack()
