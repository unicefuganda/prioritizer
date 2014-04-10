
class ContentTypes():
    TEXT = "text"
    CONTACTS = "contacts"


class PriorityListFoundation():

    POLL_TEXT_KEY = "%s:poll_texts:%s"
    POLL_CONTACTS_KEY = "%s:poll_contacts:%s"

    KEY_EXPIRE_TIME = 86400

    def __init__(self, list_name, redis_client, encoder):
        self.redis_client = redis_client
        self.encoder = encoder
        self.list_name = list_name

    def has(self, poll_id, content_type, contents):
        key_name = self.get_key_name(poll_id, content_type)
        contents = self.filter_contents(content_type, contents)
        return self.redis_client.sismember(key_name, contents)

    def contains(self, content_type, contents):
        keys = self.get_poll_keys(content_type)
        poll_key_ids = self.get_poll_ids_from_keys(keys)

        for poll_id in poll_key_ids:
            if self.has(poll_id, content_type, contents):
                return True

        return False

    def delete(self, poll_id, content_type, contents):
        contents = self.get_content_array(contents)
        key_name = self.get_key_name(poll_id, content_type)
        contents = self.filter_contents(content_type, contents)
        self.redis_client.srem(key_name, *contents)

    def add(self, poll_id, content_type, contents):
        contents = self.get_content_array(contents)
        key_name = self.get_key_name(poll_id, content_type)
        contents = self.filter_contents(content_type, contents)
        self.redis_client.sadd(key_name, *contents)
        self.add_expire(key_name)

    def add_expire(self, key):
        if self.redis_client.ttl(key) is None:
            self.redis_client.expire(key, self.KEY_EXPIRE_TIME)

    def get_poll_keys(self, content_type):
        stem = "poll_texts" if content_type is ContentTypes.TEXT else "poll_contacts"
        keys = self.redis_client.keys("%s:%s:*" % (self.list_name, stem))
        return keys

    def get_key_name(self, poll_id, content_type):
        if content_type == ContentTypes.TEXT:
            return self.POLL_TEXT_KEY % (self.list_name, poll_id)
        else:
            return self.POLL_CONTACTS_KEY % (self.list_name, poll_id)

    def get_poll_ids_from_keys(self, poll_keys):
        return map(lambda key: key.split(':')[-1], poll_keys)

    def get_content_array(self, contents):
        return [contents] if isinstance(contents, basestring) else contents

    def encode_contents(self, contents):
        if isinstance(contents, basestring):
            return self.encoder.encode(contents)
        return map(self.encoder.encode, contents)

    def filter_contents(self, content_type, contents):
        if content_type == ContentTypes.TEXT:
            contents = self.encode_contents(contents)
        return contents


class PriorityList(PriorityListFoundation):

    def __init__(self, list_name, redis_client, encoder):
        PriorityListFoundation.__init__(self, list_name, redis_client, encoder)

    def poll_text(self, poll_id, text):
        self.add(poll_id, ContentTypes.TEXT, text)

    def poll_contacts(self, poll_id, contacts):
        self.add(poll_id, ContentTypes.CONTACTS, contacts)

    def has_poll_text(self, poll_id, text):
        return self.has(poll_id, ContentTypes.TEXT, text)

    def has_poll_contact(self, poll_id, contact):
        return self.has(poll_id, ContentTypes.CONTACTS, contact)

    def delete_poll_text(self, poll_id, text):
        self.delete(poll_id, ContentTypes.TEXT, text)

    def delete_poll_contacts(self, poll_id, contacts):
        self.delete(poll_id, ContentTypes.CONTACTS, contacts)

    def get_poll_contact_keys(self):
        return self.get_poll_keys(ContentTypes.CONTACTS)

    def get_poll_text_keys(self):
        return self.get_poll_keys(ContentTypes.TEXT)

    def contains_text(self, text):
        return self.contains(ContentTypes.TEXT, text)

    def contains_contact(self, contact):
        return self.contains(ContentTypes.CONTACTS, contact)


class Blacklist(PriorityList):

    def __init__(self, redis_client, encoder):
        PriorityList.__init__(self, "blacklist", redis_client, encoder)


class Whitelist(PriorityList):

    def __init__(self, redis_client, encoder):
        PriorityList.__init__(self, "whitelist", redis_client, encoder)