from unittest import TestCase
from mockredis import mock_strict_redis_client
from models.encoder import Encoder
from models.priority import Priority
from models.prioritylist import Whitelist
from models.whitelist_contact_filter import WhitelistContactFilter


class TestWhitelistContactFilter(TestCase):

    def setUp(self):
        self.client = mock_strict_redis_client()
        self.whitelist = Whitelist(self.client, Encoder())

    def test_that_priority_is_high_when_contact_is_whitelisted(self):
        self.whitelist.poll_contacts("keyword_filter", "11111111")

        whitelist_filter = WhitelistContactFilter(self.whitelist, "11111111")
        priority = whitelist_filter.prioritize()
        self.assertEqual(priority, Priority.HIGH)

    def test_that_priority_is_unknown_when_contact_is_not_whitelisted(self):
        whitelist_filter = WhitelistContactFilter(self.whitelist, "11111111")
        priority = whitelist_filter.prioritize()
        self.assertEqual(priority, Priority.UNKNOWN)