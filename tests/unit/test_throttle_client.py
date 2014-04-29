from unittest import TestCase
from mock import patch
from models.throttle_client import ThrottleClient


class TestThrottleClient(TestCase):

    def setUp(self):
        self.query_str = "sender=1111&message=hi&backend=console"
        self.client = ThrottleClient(self.get_app_config(), self.query_str)

    @patch("gearman.GearmanClient.submit_job")
    def test_that_a_high_priority_job_can_be_submitted(self, mocked_submit_job):
        self.client.submit_high_priority_job()
        mocked_submit_job.assert_called_with("call_router_receive", self.query_str, priority='HIGH', background=True)

    @patch("gearman.GearmanClient.submit_job")
    def test_that_a_low_priority_job_can_be_submitted(self, mocked_submit_job):
        self.client.submit_low_priority_job()
        mocked_submit_job.assert_called_with("call_router_receive", self.query_str, priority='LOW', background=True)

    @patch("gearman.GearmanClient.submit_job")
    def test_that_a_normal_priority_job_can_be_submitted(self, mocked_submit_job):
        self.client.submit_normal_priority_job()
        mocked_submit_job.assert_called_with("call_router_receive", self.query_str, priority=None, background=True)

    def get_app_config(self):
        config = {  "GEARMAN_SERVER": "0.0.0.0:4730",
                    "ROUTER_RECEIVE_TASK_NAME": "call_router_receive",
                    "ROUTER_RECEIVE_URL": "http://random.address/router/receive"
                }
        return config