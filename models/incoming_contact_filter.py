from models.priority import Priority


class IncomingContactFilter(object):

    def __init__(self, blacklist, contact):
        self.blacklist = blacklist
        self.contact = contact

    def get_blacklisted_poll_ids(self):
        contact_keys = self.blacklist.get_poll_contact_keys()
        poll_ids = self.blacklist.get_poll_ids_from_keys(contact_keys)
        return poll_ids

    def prioritize(self):
        if self.blacklist.contains_contact(self.contact):
            poll_ids = self.get_blacklisted_poll_ids()

            for poll_id in poll_ids:
                self.blacklist.delete_poll_contacts(poll_id, [self.contact])

            return Priority.LOW
        return Priority.HIGH