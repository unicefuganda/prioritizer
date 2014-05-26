from unittest import TestCase
import requests
import settings
import gearman
import re
import throttle


class GearmanThrottleBaseTest(TestCase):

    def setUp(self):
        self.gm_client = gearman.GearmanAdminClient([settings.GEARMAN_SERVER])
        self.redis_client = throttle.get_redis_client()
        self.log_file_before_requests = self.read_throttle_log_file()

    def tearDown(self):
        self.redis_client.delete("whitelist:poll_contacts:keyword_filter")

    def read_throttle_log_file(self):
        logfile = open(settings.THROTTLE_WORK_LOG_FILE, 'r')
        lines = logfile.readlines()
        logfile.close()
        return lines

    def wait_until_empty_queue_in_gearman(self, status):
        while(status[0]["queued"] != 0):
            status = self.gm_client.get_status()

    def assert_jobs_queued(self, status):
        self.assertEqual(status[0]["workers"], 1)
        self.assertEqual(status[0]["queued"], 3)
        self.assertEqual(status[0]["task"], 'call_router_receive')

    def assert_high_priority_task_is_not_done_last(self, high_priority_ureport_url):
        log_lines = self.read_throttle_log_file()
        added_log_data = log_lines[len(self.log_file_before_requests):]
        reg = re.compile(".*\/router\/receive\?message\=.*")
        request_lines = filter(reg.match, added_log_data)
        self.assertEqual(3, len(request_lines))
        all_request_urls = ", ".join(request_lines)
        self.assertIn(high_priority_ureport_url, all_request_urls)
        self.assertNotIn(high_priority_ureport_url, request_lines[-1])

    def assert_high_priority(self, high_priority_german_url, high_priority_ureport_url):
        requests.get(self.generate_throttle_url(sender="128", message="test"))
        requests.get(self.generate_throttle_url(sender="129", message="test"))
        requests.get(high_priority_german_url)

        status = self.gm_client.get_status()
        self.assert_jobs_queued(status)
        self.wait_until_empty_queue_in_gearman(status)

        self.assert_high_priority_task_is_not_done_last(high_priority_ureport_url)

    def _get_query_string(self, sender, message):
        return '?message=%s&sender=%s&backend=dev' % (message, sender)

    def generate_throttle_url(self, sender, message):
        return settings.THROTTLE_URL + self._get_query_string(sender, message)

    def generate_ureport_url(self, sender, message):
        return settings.ROUTER_RECEIVE_URL + self._get_query_string(sender, message)