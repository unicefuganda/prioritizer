from tests.functional.priority_test_case import PriorityTestCase


class TestStepsCache(PriorityTestCase):

    def test_that_a_registration_message_is_prioritized_as_high_priority(self):
        self.assert_high_priority(
            self.get_url("http://%s/router?text=How+did+you+hear+about+U+REPORT?&to=256704000000"))

    def test_that_a_message_with_single_recipient_gets_prioritized_as_high_priority(self):
        self.assert_high_priority(self.get_url("http://%s/router?text=Hi&to=256704000000"))

