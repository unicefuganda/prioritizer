from unittest import TestCase
import requests
import settings
import gearman
import re


class TestThrottlePrioritizerIntegration(TestCase):
    def setUp(self):
        self.gm_client = gearman.GearmanAdminClient([settings.GEARMAN_SERVER])

    def read_throttle_log_file(self):
        logfile = open(settings.THROTTLE_WORK_LOG_FILE, 'r')
        lines = logfile.readlines()
        logfile.close()
        return lines

    def wait_until_empty_queue_in_gearman(self, status):
        while(status[0]["queued"] != 0):
            status = self.gm_client.get_status()

    def test_get_requests_from_throttle_triggers_workers_to_write_log_files_in_priority_order(self):
        send_gearman_url = 'http://127.0.0.1/gearmanthrottle/receive?message=test&sender=%(NUMBER)s&backend=dev&keyword=%(KEYWORD)s'
        send_comsumer_url = 'http://127.0.0.1/router/receive?message=test&sender=%(NUMBER)s&backend=dev&keyword=%(KEYWORD)s'
        high_priority_message_params = {'NUMBER': '127', 'KEYWORD': 'JOIN'}
        low_priority_message_params = {'NUMBER': '128', 'KEYWORD': ''}
        another_low_priority_message_params = {'NUMBER': '129', 'KEYWORD': ''}

        log_file_before_requests = self.read_throttle_log_file()

        requests.get(send_gearman_url % low_priority_message_params)
        requests.get(send_gearman_url % another_low_priority_message_params)
        requests.get(send_gearman_url % high_priority_message_params)

        status = self.gm_client.get_status()

        self.assertEqual(status[0]["workers"], 1)
        self.assertEqual(status[0]["queued"], 3)
        self.assertEqual(status[0]["task"], 'call_router_receive')

        self.wait_until_empty_queue_in_gearman(status)
        log_lines = self.read_throttle_log_file()

        added_log_data = log_lines[len(log_file_before_requests):]
        reg = re.compile(".*\/router\/receive\?message\=test.*")
        request_lines = filter(reg.match, added_log_data)

        self.assertEqual(3, len(request_lines))
        high_priority_ureport_url = send_comsumer_url % high_priority_message_params
        self.assertNotIn(high_priority_ureport_url, request_lines[-1])
