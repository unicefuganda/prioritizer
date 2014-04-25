

class KeywordFilter(object):

    VALID_KEYWORDS = ["join"]
    ID = "keyword_filter"

    def __init__(self, whitelist, keyword, contact):
        self.whitelist = whitelist
        self.keyword = keyword
        self.contact = contact

    def prioritize(self):
        if self.keyword in self.VALID_KEYWORDS:
            self.whitelist.poll_contacts(self.ID, self.contact)