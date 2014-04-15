from unittest import TestCase
from mock import Mock
from models.filter_processor import FilterProcessor
from models.priority import Priority


class TestFilterProcessor(TestCase):
    def setUp(self):
        self.filter_processor = FilterProcessor()

    def test_that_low_and_high_filters_can_be_passed_through_the_constructor(self):
        high_filters = [1, 2]
        low_filters = [1, 2, 3]

        filter_processor = FilterProcessor(high_filters, low_filters)

        self.assertEqual(high_filters, filter_processor.high_filters)
        self.assertEqual(low_filters, filter_processor.low_filters)

    def test_that_constructor_has_default_values(self):
        self.assertEqual(self.filter_processor.high_filters, None)
        self.assertEqual(self.filter_processor.low_filters, None)

    def test_that_low_filter_has_precedence_over_high_filter(self):
        processor = self.get_filter_processor_with(Priority.HIGH, Priority.LOW)
        priority = processor.execute()

        self.assertEqual(priority, Priority.LOW)

    def test_that_when_low_filter_returns_unknown_priority_high_priority_kicks_in(self):
        processor = self.get_filter_processor_with(Priority.HIGH, Priority.UNKNOWN)
        priority = processor.execute()

        self.assertEqual(priority, Priority.HIGH)

    def test_that_when_low_filter_returns_unknown_and_high_returns_low_priority_is_low(self):
        processor = self.get_filter_processor_with(Priority.LOW, Priority.UNKNOWN)
        priority = processor.execute()
        self.assertEqual(priority, Priority.LOW)

    def get_filter_processor_with(self, high_filter_priority, low_filter_priority):
        mocked_low_filter = Mock()
        mocked_low_filter.prioritize.return_value = low_filter_priority

        mocked_high_filter = Mock()
        mocked_high_filter.prioritize.return_value = high_filter_priority

        return FilterProcessor([mocked_high_filter], [mocked_low_filter])
