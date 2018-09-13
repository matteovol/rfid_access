class IdCall:

    def __init__(self, call):
        self.id_call = call
        self.root = None
        self.ser = None
        self.enum = None
        self.bdd = None

    def set_id_call(self, call):
        self.id_call = call

    def get_id_call(self):
        return self.id_call

    def set_root(self, root):
        self.root = root

    def get_root(self):
        return self.root


id_call = IdCall(1)
