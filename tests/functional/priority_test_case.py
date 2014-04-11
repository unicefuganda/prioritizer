from unittest import TestCase
import re
import requests
import settings


class PriorityTestCase(TestCase):
    def get_smsc_details(self, text, smsc_name):
        regex = "%s.*sent ([0-9]*)," % smsc_name
        return re.compile(regex).search(text).groups()[0]

    def get_url(self, url):
        return url % settings.PRIORITIZER_ADDRESS

    def assert_url_priority(self, url, priority):
        initial_high, initial_low = self.get_smsc_sent_values()
        requests.get(url)
        current_high, current_low = self.get_smsc_sent_values()

        if priority == "high":
            self.assertTrue(int(current_high) > int(initial_high))

        if priority == "low":
            self.assertTrue(int(current_low) > int(initial_low))

    def get_smsc_sent_values(self):
        kannel_status_page_url = settings.KANNEL_STATUS_URL
        response = requests.get(kannel_status_page_url)

        return self.get_smsc_details(response.text, "hi_smsc"), self.get_smsc_details(response.text, "lo_smsc")

    def assert_low_priority(self, url):
        self.assert_url_priority(url, "low")

    def assert_high_priority(self, url):
        self.assert_url_priority(url, "high")
