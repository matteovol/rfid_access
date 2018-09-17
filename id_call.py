class IdCall:

    """Object to be used as a global variable (dirty but i dunno how to do otherwise)"""

    def __init__(self, call):

        """Init all the values to None"""

        self.id_call = call
        self.root = None
        self.ser = None
        self.enum = None
        self.bdd = None

    def set_id_call(self, call):

        """Set id call"""

        self.id_call = call

    def get_id_call(self):

        """Get id call"""

        return self.id_call

    def set_root(self, root):

        """Set root"""

        self.root = root

    def get_root(self):

        """get root"""

        return self.root


id_call = IdCall(1)
