from unittest import TestCase
from models.priority import Priority
from models.registration_message_filter import RegistrationMessageFilter
from mock import Mock


class TestRegistrationMessageFilter(TestCase):

    def test_that_message_can_be_prioritized(self):
        mocked_steps_cache = Mock()
        mocked_steps_cache.has_text.return_value = True
        message_filter = RegistrationMessageFilter(mocked_steps_cache, "any message")

        priority = message_filter.prioritize()

        self.assertEqual(priority, Priority.HIGH)

    def test_that_text_message_gets_priotized_with_low_priority(self):
        mocked_steps_cache = Mock()
        mocked_steps_cache.has_text.return_value = False
        message_filter = RegistrationMessageFilter(mocked_steps_cache, "any message")

        priority = message_filter.prioritize()
        self.assertEqual(priority, Priority.LOW)