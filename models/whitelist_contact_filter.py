from models.keyword_filter import KeywordFilter
from models.priority import Priority


class WhitelistContactFilter(object):

    def __init__(self, whitelist, contact):
        self.contact = contact
        self.whitelist = whitelist

    def prioritize(self):
        if self.whitelist.has_poll_contact(KeywordFilter.ID, self.contact):
            return Priority.HIGH
        return Priority.UNKNOWN