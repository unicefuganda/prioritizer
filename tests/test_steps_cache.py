from unittest import TestCase
from mock import patch, Mock, MagicMock
from mockredis import mock_strict_redis_client
from models.caching_steps import StepsCache
from flask import json

def encode_mock(encode_values):
    def side_effect(args):
        return encode_values[args]
    mock = MagicMock(side_effect=side_effect)
    return mock


class TestStepsCache(TestCase):

    def setUp(self):
        self.client = mock_strict_redis_client()
        self.cache = StepsCache(self.client, "username", "password", "http://random/url", "ureport-registration-steps")

    @patch('redis.StrictRedis', mock_strict_redis_client)
    def test_that_data_from_api_is_stored(self):
        key_name = "my script"
        first_value = "step 1 1"
        second_value = "step 1 2"
        data = [first_value, second_value]
        encoded_data = {first_value: "encrypted_first_value", second_value: "encrypted_second_value"}
        self.cache.get_key_name = Mock(return_value=key_name)
        self.cache.get_steps_information = Mock(return_value=data)
        self.cache.encoder.encode = encode_mock(encoded_data)

        self.cache.add_script_steps_data()

        self.assertTrue(self.client.sismember(key_name, "encrypted_first_value"))
        self.assertTrue(self.client.sismember(key_name, "encrypted_second_value"))

    def test_that_script_step_data_gets_deleted(self):
        script_name = 'my_script'
        first_step = 'step 1 1'
        self.client.sadd(script_name, first_step)
        self.cache.get_key_name = Mock(return_value=script_name)
        self.cache.delete_script_steps_data()

        self.assertFalse(self.client.exists(script_name))

    def test_that_method_checks_for_existance_of_text_in_cache_set(self):
        self.cache.get_steps_information = Mock(return_value=["expected message 1", "expected message 2"])
        self.cache.add_script_steps_data()

        in_cache = self.cache.has_text("expected message 1")

        self.assertTrue(in_cache)

    def test_that_invalid_text_is_not_in_cache(self):
        self.cache.get_steps_information = Mock(return_value=["expected message 1", "expected message 2"])
        self.cache.add_script_steps_data()

        in_cache = self.cache.has_text("none expected message")

        self.assertFalse(in_cache)

    def test_that_key_name_is_ureport(self):
        self.assertEquals(self.cache.get_key_name(), "ureport-registration-steps")

    @patch('base64.encodestring')
    @patch('urllib2.Request')
    @patch('urllib2.urlopen')
    def test_authorized_response(self, urlopen_mock, request_class_mock, encoded_str_mock):
        request_mock = Mock()
        add_header = Mock()
        request_mock.add_header = add_header
        request_class_mock.return_value = request_mock
        fake_response = "response"
        urlopen_mock.return_value = fake_response
        auth_data = "user:passwd"
        encoded_str_mock.return_value = auth_data

        self.assertEquals(self.cache.get_authorized_response("my_http_address"), fake_response)
        urlopen_mock.assert_called_once_with(request_mock)
        request_mock.add_header.assert_called_once_with('Authorization', 'Basic %s' % auth_data)

    def test_retrieve_of_json_data_from_api(self):
        json_response = json.dumps({"steps": ["step 1", "step 2"]})
        response_mock = Mock()
        response_mock.read = Mock(return_value=json_response)
        self.cache.get_authorized_response = Mock(return_value=response_mock)

        self.assertListEqual(self.cache.get_steps_information(), ["step 1", "step 2"])