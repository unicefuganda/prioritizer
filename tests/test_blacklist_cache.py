from unittest import TestCase
from mock import patch, Mock
from mockredis import mock_strict_redis_client
from models.blacklist_cache import BlacklistCache


class TestBlacklistCache(TestCase):
    def setUp(self):
        self.client = mock_strict_redis_client()
        self.cache = BlacklistCache(self.client)

    @patch('redis.StrictRedis', mock_strict_redis_client)
    def test_blacklist_is_updated_with_new_word(self):
        text = "new info"
        key_name = "my script"
        self.cache.key_name = Mock(return_value=key_name)
        encoder_mock = Mock()
        encoder_mock.encode.return_value="encrypted_value"
        self.cache.encoder = encoder_mock

        self.cache.add_to_blacklist(text)
        self.assertTrue(self.client.sismember(key_name, "encrypted_value"))

    def test_that_key_name_is_blacklist(self):
        self.assertEquals(self.cache.key_name(), "ureport-high-priority-blacklist")

