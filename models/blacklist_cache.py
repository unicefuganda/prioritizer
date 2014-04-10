from models.encoder import Encoder


class BlacklistCache:

    def __init__(self, client):
        self.client = client
        self.encoder = Encoder()

    def add_to_blacklist(self, text):
        encoded_text = self.encoder.encode(text)
        self.client.sadd(self.key_name(), encoded_text)

    def key_name(self):
        return "ureport-high-priority-blacklist"
