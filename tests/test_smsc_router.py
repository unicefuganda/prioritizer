from unittest import TestCase
from mock import Mock, patch
from models.priority import Priority
from models.smsc_router import SMSCRouter
import requests


class TestSMSCRouter(TestCase):

    def setUp(self):
        self.app_config = self.get_app_config()
        self.smsc_router = SMSCRouter(self.app_config)

    def test_that_for_message_with_low_priority_the_low_priority_smsc_id_is_used(self):
        url = self.smsc_router.generate_url("message", "111111,222222", Priority.LOW)
        smsc_id = url.split('&')[-1].split('=')[-1]

        self.assertEqual(smsc_id, self.app_config["KANNEL_LOW_PRIORITY_SMSC"])

    def test_that_for_message_with_high_priority_the_low_priority_smsc_id_is_used(self):
        url = self.smsc_router.generate_url("message", "111111,222222", Priority.HIGH)
        smsc_id = url.split('&')[-1].split('=')[-1]

        self.assertEqual(smsc_id, self.app_config["KANNEL_HIGH_PRIORITY_SMSC"])

    def test_that_make_http_request_message_gets_called_with_generated_url(self):
        self.smsc_router.make_http_request = Mock()
        self.smsc_router.generate_url = Mock(return_value="mocked_url")
        self.smsc_router.route(self.get_request_args(), Priority.HIGH)
        self.smsc_router.make_http_request.assert_called_with("mocked_url")

    @patch("requests.get")
    def test_that_requests_get_method_gets_called_by_make_http_request(self, mocked_requests_get):
        any_url = "http://random.url"
        self.smsc_router.make_http_request(any_url)
        mocked_requests_get.assert_called_with(any_url)

    @patch("requests.get", side_effect=requests.exceptions.HTTPError())
    def test_that_an_http_error_exception_gets_caught(self, mocked_requests_get):
        any_url = "invalid_url"

        try:
            self.smsc_router.make_http_request(any_url)
        except Exception, e:
            self.fail("Exception was not caught")

    def test_that_generate_url_method_is_called_with_a_plus_delimited_set_of_receivers(self):
        self.smsc_router.make_http_request = Mock()
        self.smsc_router.generate_url = Mock()
        self.smsc_router.route(self.get_request_args(), Priority.HIGH)
        self.smsc_router.generate_url.assert_called_with("any message", "111111+222222+3333333", Priority.HIGH)

    def get_app_config(self):
        config = {  "KANNEL_LOW_PRIORITY_SMSC": "1111",
                    "KANNEL_HIGH_PRIORITY_SMSC": "2222",
                    "KANNEL_SEND_SMS_URL": "http://0.0.0.0",
                    "KANNEL_SEND_SMS_FROM": "http://1.1.1.1",
                    "KANNEL_SEND_SMS_USERNAME": "kannel_username",
                    "KANNEL_SEND_SMS_PASSWORD": "kannel_password"
                }
        return config

    def get_request_args(self):
        return {"text":"any message", "to":"111111,222222,3333333"}

