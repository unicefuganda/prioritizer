from unittest import TestCase
from mock import patch, call
from mockredis import mock_strict_redis_client
from models.encoder import Encoder
from models.incoming_contact_filter import IncomingContactFilter
from models.priority import Priority
from models.prioritylist import Blacklist


class TestIncomingContactFilter(TestCase):

    RANDOM_CONTACT = 111111

    def setUp(self):
        self.client = mock_strict_redis_client()
        self.blacklist = Blacklist(self.client, Encoder())
        self.contact_filter = IncomingContactFilter(self.blacklist, self.RANDOM_CONTACT)

    def test_that_priority_is_high_when_number_is_not_blacklisted(self):
        priority = self.contact_filter.prioritize()
        self.assertEqual(priority, Priority.HIGH)

    def test_that_priority_is_low_when_a_number_is_blacklisted(self):
        self.contact_filter.blacklist.poll_contacts(231, [self.RANDOM_CONTACT])
        priority = self.contact_filter.prioritize()
        self.assertEqual(priority, Priority.LOW)

    @patch("models.prioritylist.Blacklist.delete_poll_contacts")
    def test_that_contact_is_removed_from_blacklist_when_present(self, mocked_delete_poll_contacts):
        self.contact_filter.prioritize()
        assert not mocked_delete_poll_contacts.called

        self.contact_filter.blacklist.poll_contacts(231, [self.RANDOM_CONTACT])
        self.contact_filter.prioritize()
        mocked_delete_poll_contacts.assert_called_with('231', [self.RANDOM_CONTACT])

    @patch("models.prioritylist.Blacklist.delete_poll_contacts")
    def test_that_contact_is_removed_from_all_blacklist_polls(self, mocked_delete_poll_contacts):
        self.contact_filter.blacklist.poll_contacts(231, [self.RANDOM_CONTACT])
        self.contact_filter.blacklist.poll_contacts(232, [self.RANDOM_CONTACT])

        self.contact_filter.prioritize()

        expected = [call('231', [self.RANDOM_CONTACT]), call('232', [self.RANDOM_CONTACT])]
        self.assertEqual(mocked_delete_poll_contacts.mock_calls, expected)