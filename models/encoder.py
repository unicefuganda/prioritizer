import hashlib

class Encoder:
    def encode(self,text):
        return hashlib.md5(text.encode("utf-8")).hexdigest()
