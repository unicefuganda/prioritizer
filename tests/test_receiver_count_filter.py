from unittest import TestCase
from models.priority import Priority
from models.receiver_count_filter import ReceiverCountFilter
from mock import Mock


class TestReceiverCountFilter(TestCase):

    def test_that_priority_is_high_when_number_of_receivers_is_one(self):
        count_filter = ReceiverCountFilter(["111111111"])
        priority = count_filter.prioritize()
        self.assertEqual(priority, Priority.HIGH)

    def test_that_priority_is_low_when_number_of_receivers_is_more_than_default_one(self):
        count_filter = ReceiverCountFilter(["111111111", "222222222"])
        priority = count_filter.prioritize()
        self.assertEqual(priority, Priority.LOW)

    def test_that_priority_is_high_when_number_of_receivers_is_two_and_maximum_receiver_count_is_two(self):
        count_filter = ReceiverCountFilter(["111111111", "222222222"], 2)
        priority = count_filter.prioritize()
        self.assertEqual(priority, Priority.HIGH)

    def test_that_priority_is_low_if_there_are_no_receivers(self):
        count_filter = ReceiverCountFilter([])
        priority = count_filter.prioritize()
        self.assertEqual(priority, Priority.LOW)
