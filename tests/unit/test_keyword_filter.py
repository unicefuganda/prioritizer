from unittest import TestCase
from mock import patch
from mockredis import mock_strict_redis_client
from models.encoder import Encoder
from models.keyword_filter import KeywordFilter
from models.prioritylist import Whitelist


class TestKeywordFilter(TestCase):

    def setUp(self):
        self.client = mock_strict_redis_client()
        self.whitelist = Whitelist(self.client, Encoder())

    @patch("models.prioritylist.Whitelist.poll_contacts")
    def test_that_a_request_with_keyword_join_gets_the_number_white_listed(self, mocked_poll_contacts):
        keyword_filter = KeywordFilter(self.whitelist, "join", "0773267474")
        keyword_filter.prioritize()
        mocked_poll_contacts.assert_called_with("keyword_filter", "0773267474")

    @patch("models.prioritylist.Whitelist.poll_contacts")
    def test_that_only_contact_with_allowed_keyword_gets_white_listed(self, mocked_poll_contacts):
        keyword_filter = KeywordFilter(self.whitelist, "invalid_keyword", "0773267474")
        keyword_filter.prioritize()
        self.assertFalse(mocked_poll_contacts.called)

    @patch("models.prioritylist.Whitelist.poll_contacts")
    def test_that_allowed_keyword_other_than_join_also_gets_whitelisted(self, mocked_poll_contacts):
        keyword_filter = KeywordFilter(self.whitelist, "valid_keyword", "0773267474")
        keyword_filter.VALID_KEYWORDS.append("valid_keyword")
        keyword_filter.prioritize()
        mocked_poll_contacts.assert_called_with("keyword_filter", "0773267474")
