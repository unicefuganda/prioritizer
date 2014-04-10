from models.priority import Priority


class BlacklistFilter():

    def __init__(self, blacklist, message):
        self.blacklist = blacklist
        self.message = message

    def prioritize(self):
        if self.blacklist.contains_text(self.message):
            return Priority.LOW
        return Priority.UNKNOWN