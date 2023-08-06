class Message(object):

    def __init__(self, msg=""):
        self.msg = str()
        self.add_message(msg)

    def add_message(self, message):
        self.msg = "{}\n{}".format(self.msg, message)

    @property
    def message(self):
        return self.msg

    def clear_message(self):
        self.msg = str()