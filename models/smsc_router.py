from models.priority import Priority
import requests


class SMSCRouter(object):

    def __init__(self, app_config):
        self.app_config = app_config

    def format_receivers_for_kannel(self, request_args):
        return request_args.replace(",", "+")

    def route(self, request_args, priority):
        url = self.generate_url(request_args["text"], self.format_receivers_for_kannel(request_args["to"]), priority)
        self.make_http_request(url)

    def make_http_request(self, url):
        try:
            response = requests.get(url)
        except requests.RequestException, e:
            # TODO: log the exception
            pass

    def get_kannel_smsc_id(self, priority):
        if priority is Priority.HIGH:
            smsc_id = self.app_config["KANNEL_HIGH_PRIORITY_SMSC"]
        else:
            smsc_id = self.app_config["KANNEL_LOW_PRIORITY_SMSC"]
        return smsc_id

    def generate_url(self, message, receivers, priority):
        smsc_id = self.get_kannel_smsc_id(priority)

        return "%(base_url)s?from=%(from)s&username=%(username)s&password=%(password)s&text=%(text)s&to=%(receivers)s&smsc=%(smsc)s" % \
               {"base_url": self.app_config["KANNEL_SEND_SMS_URL"],
                "from": self.app_config["KANNEL_SEND_SMS_FROM"],
                "username": self.app_config["KANNEL_SEND_SMS_USERNAME"],
                "password": self.app_config["KANNEL_SEND_SMS_PASSWORD"],
                "text": message,
                "receivers": receivers,
                "smsc": smsc_id
                }