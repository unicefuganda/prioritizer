from unittest import TestCase
from mock import patch, Mock
from mockredis import mock_strict_redis_client
from models.prioritylist import Blacklist, ContentTypes, Whitelist


class TestBlacklist(TestCase):

    def setUp(self):
        self.client = mock_strict_redis_client()
        self.encoder = Mock()
        self.encoder.encode = self.reverse_string
        self.blacklist = Blacklist(self.client, self.encoder)
        self.whitelist = Whitelist(self.client, self.encoder)
        self.poll_texts_key_name = "blacklist:poll_texts:231"
        self.poll_contacts_key_name = "blacklist:poll_contacts:231"

    def reverse_string(self, text):
        return text[::-1]

    def test_that_poll_text_can_be_black_listed(self):
        self.blacklist.poll_text(231, "sample text")
        self.assertTrue(self.client.sismember(self.poll_texts_key_name, self.reverse_string("sample text")))

    def test_that_an_array_of_poll_texts_can_be_black_listed(self):
        self.blacklist.poll_text(231, ["sample 1", "sample 2", "sample 3"])
        self.assertTrue(self.client.sismember(self.poll_texts_key_name, self.reverse_string("sample 1")))
        self.assertTrue(self.client.sismember(self.poll_texts_key_name, self.reverse_string("sample 2")))
        self.assertTrue(self.client.sismember(self.poll_texts_key_name, self.reverse_string("sample 3")))

        self.assertFalse(self.client.sismember(self.poll_texts_key_name, self.reverse_string("sample 4")))

    def test_that_only_inserted_text_exist(self):
        self.blacklist.poll_text(231, "valid text")

        self.assertFalse(self.blacklist.has_poll_text(231, "invalid text"))
        self.assertTrue(self.blacklist.has_poll_text(231, "valid text"))

    def test_that_poll_text_can_be_deleted(self):
        text_to_delete = "text to delete"

        self.blacklist.poll_text(231, text_to_delete)
        self.blacklist.poll_text(231, "text not to delete")
        self.assertTrue(self.blacklist.has_poll_text(231, text_to_delete))

        self.blacklist.delete_poll_text(231, text_to_delete)
        self.assertFalse(self.blacklist.has_poll_text(231, text_to_delete))

        self.assertTrue(self.blacklist.has_poll_text(231, "text not to delete"))

    def test_that_poll_contacts_can_be_black_listed(self):
        ones = "1111111"
        twos = "2222222"
        threes = "33333"

        self.blacklist.poll_contacts(231, [ones, twos])

        self.assertTrue(self.client.sismember(self.poll_contacts_key_name, ones))
        self.assertTrue(self.client.sismember(self.poll_contacts_key_name, twos))
        self.assertFalse(self.client.sismember(self.poll_contacts_key_name, threes))

    def test_that_inserted_poll_contact_exists(self):
        ones = "1111111"
        self.blacklist.poll_contacts(231, ones)
        self.assertTrue(self.blacklist.has_poll_contact(231, ones))

    def test_that_poll_contacts_can_be_deleted(self):
        ones = "1111111"
        twos = "2222222"
        threes = "33333"

        self.blacklist.poll_contacts(231, [ones, twos, threes])
        self.assertTrue(self.blacklist.has_poll_contact(231, ones))
        self.assertTrue(self.blacklist.has_poll_contact(231, twos))
        self.assertTrue(self.blacklist.has_poll_contact(231, threes))

        self.blacklist.delete_poll_contacts(231, [twos,threes])

        self.assertTrue(self.blacklist.has_poll_contact(231, ones))

        self.assertFalse(self.blacklist.has_poll_contact(231, twos))
        self.assertFalse(self.blacklist.has_poll_contact(231, threes))

    def test_that_whitelist_returns_a_valid_key_name(self):
        text_key_name = self.whitelist.get_key_name(231, ContentTypes.TEXT)
        contacts_key_name = self.whitelist.get_key_name(231, ContentTypes.CONTACTS)

        self.assertEqual(text_key_name.find("whitelist:"), 0)
        self.assertEqual(contacts_key_name.find("whitelist:"), 0)

    def test_that_we_can_fetch_the_poll_keys(self):
        self.blacklist.poll_text(231, "sample 1")
        self.blacklist.poll_text(232, "sample 2")

        poll_keys = self.blacklist.get_poll_text_keys()

        self.assertTrue('blacklist:poll_texts:231' in poll_keys and 'blacklist:poll_texts:232' in poll_keys)

    def test_that_only_poll_contact_keys_are_returned(self):
        self.blacklist.poll_contacts(231, "11111111")
        self.blacklist.poll_text(232, "sample 2")

        poll_contact_keys = self.blacklist.get_poll_contact_keys()

        self.assertEqual(len(poll_contact_keys), 1)

    def test_that_poll_keys_returns_nothing_when_no_poll_text_was_added(self):
        poll_keys = self.blacklist.get_poll_text_keys()
        self.assertEqual(poll_keys, [])

    def test_that_poll_keys_are_returned_for_only_the_specific_list_type(self):
        self.blacklist.poll_text(231, "sample 1")
        self.whitelist.poll_text(232, "sample 2")

        blacklist_poll_keys = self.blacklist.get_poll_text_keys()

        self.assertEqual(len(blacklist_poll_keys), 1)

    def test_that_polls_have_text(self):
        self.blacklist.poll_text(231, "sample 1")
        self.blacklist.poll_text(232, "sample 2")

        self.assertTrue(self.blacklist.contains_text("sample 1"))
        self.assertTrue(self.blacklist.contains_text("sample 2"))

        self.assertFalse(self.blacklist.contains_text("sample 3"))

    def test_that_polls_have_contact(self):
        self.blacklist.poll_contacts(231, "sample 1")
        self.blacklist.poll_contacts(232, "sample 2")

        self.assertTrue(self.blacklist.contains_contact("sample 1"))
        self.assertTrue(self.blacklist.contains_contact("sample 2"))

        self.assertFalse(self.blacklist.contains_contact("sample 3"))

    def test_that_add_expire_method_gets_called_with_key_name(self):
        self.blacklist.add_expire = Mock()
        self.blacklist.poll_text(231, "sample 1")

        self.blacklist.add_expire.assert_called_with("blacklist:poll_texts:231")

    def test_that_add_expire_only_adds_expire_when_no_time_to_live_exists(self):
        original_expire = self.blacklist.redis_client.expire
        self.blacklist.redis_client.expire = Mock()
        self.blacklist.poll_text(231, "sample 1")
        original_expire("blacklist:poll_texts:231", 86400)

        self.blacklist.poll_text(231, "sample 2")
        self.blacklist.redis_client.expire.assert_called_once_with("blacklist:poll_texts:231", 86400)