import logging
from unittest import TestCase
from mock import patch, Mock
from models.throttle_worker import ThrottleWorker


class TestThrottleWorker(TestCase):


    @patch("requests.get")
    def test_that_router_receive_gets_called_with_parameters(self, mocked_requests_get):
        gearman_worker = None
        gearman_job = Mock()
        gearman_job.data = "url-parameters"

        worker = ThrottleWorker(self.get_app_config())
        response = worker.call_router_receive(gearman_worker, gearman_job)

        mocked_requests_get.assert_called_with("http://random.address/router/receive?password=supersecret&url-parameters")

        self.assertEqual("ok", response)

    @patch("gearman.GearmanWorker.register_task")
    def test_that_on_initiation_gearman_worker_registers_the_task(self, mocked_register_task):
        worker = ThrottleWorker(self.get_app_config())
        mocked_register_task.assert_called_with("call_router_receive", worker.call_router_receive)

    @patch("gearman.GearmanWorker.set_client_id")
    def test_that_on_initiation_client_id_is_set_for_the_worker(self, mocked_set_client_id):
        worker = ThrottleWorker(self.get_app_config(), "sample-worker")
        mocked_set_client_id.assert_called_with("sample-worker")

    @patch("gearman.GearmanWorker.work")
    def test_that_calling_start_method_on_throttle_work_puts_the_gearman_worker_to_work(self, mocked_work):
        worker = ThrottleWorker(self.get_app_config())
        worker.start()
        mocked_work.assert_called_with()

    @patch("models.throttle_worker.ThrottleWorker.log_info")
    @patch("requests.get")
    def test_that_logging_gets_called(self, mocked_requests_get, mocked_log_info):
        _app_config = self.get_app_config()
        mock_german_job = Mock(data=None)
        url = "%s?password=%s&%s" % (_app_config["ROUTER_RECEIVE_URL"], _app_config["UREPORT_APP_PASSWORD"], mock_german_job.data)
        worker = ThrottleWorker(_app_config, logger=logging)

        worker.call_router_receive(None, mock_german_job)

        mocked_log_info.assert_called_with(mock_german_job, None, url)

    def get_app_config(self):
        config = {  "GEARMAN_SERVER": "0.0.0.0:4730",
                    "ROUTER_RECEIVE_TASK_NAME": "call_router_receive",
                    "ROUTER_RECEIVE_URL": "http://random.address/router/receive",
                    "UREPORT_APP_PASSWORD": "supersecret"
                }
        return config