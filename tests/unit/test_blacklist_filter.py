from unittest import TestCase
from mockredis import mock_strict_redis_client
from models.blacklist_filter import BlacklistFilter
from models.encoder import Encoder
from models.priority import Priority
from models.prioritylist import Blacklist


class TestBlacklistFilter(TestCase):

    def setUp(self):
        self.client = mock_strict_redis_client()
        self.blacklist = Blacklist(self.client, Encoder())

    def test_that_priority_is_undefined_when_nothing_is_blacklisted(self):
        blacklist_filter = BlacklistFilter(self.blacklist, "any message")
        priority = blacklist_filter.prioritize()
        self.assertEqual(priority, Priority.UNKNOWN)

    def test_that_priority_is_low_for_something_that_is_blacklisted(self):
        self.blacklist.poll_text(231, "blacklisted text")

        blacklist_filter = BlacklistFilter(self.blacklist, "blacklisted text")
        priority = blacklist_filter.prioritize()
        self.assertEqual(priority, Priority.LOW)

