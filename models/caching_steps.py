from flask import json
import hashlib
import urllib2, base64
from models.encoder import Encoder


class StepsCache:

    def __init__(self, client, username, password, url, cache_key_name):
        self.client = client
        self.username = username
        self.password = password
        self.url = url
        self.cache_key_name = cache_key_name
        self.encoder = Encoder()

    def get_key_name(self):
        return self.cache_key_name

    def add_script_steps_data(self):
        script_steps = self.get_steps_information()
        for value in script_steps:
            self.client.sadd(self.get_key_name(), self.encoder.encode(value))

    def get_steps_information(self):
        response = self.get_authorized_response(self.url)

        data = json.loads(response.read())
        return data["steps"]

    def delete_script_steps_data(self):
        self.client.delete(self.get_key_name())

    def has_text(self, text):
        return self.client.sismember(self.get_key_name(), self.encoder.encode(text))

    def get_authorized_response(self, url):
        request = urllib2.Request(url)
        base64string = base64.encodestring('%s:%s' % (self.username, self.password)).replace('\n', '')
        request.add_header("Authorization", "Basic %s" % base64string)
        response = urllib2.urlopen(request)
        return response
