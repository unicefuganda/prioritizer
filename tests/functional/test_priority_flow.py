from models.encoder import Encoder
from models.prioritylist import Blacklist
import prioritizer
from tests.functional.priority_test_case import PriorityTestCase


class TestStepsCache(PriorityTestCase):

    def setUp(self):
        self.blacklist = Blacklist(prioritizer.get_redis_client(), Encoder())

    def tearDown(self):
        self.blacklist.delete_poll_text_set(231)

    def test_that_a_registration_message_is_prioritized_as_high_priority(self):
        self.assert_high_priority(
            self.get_url("http://%s/router?text=How+did+you+hear+about+U+REPORT?&to=256704000000"))

    def test_that_a_message_with_single_recipient_gets_prioritized_as_high_priority(self):
        self.assert_high_priority(self.get_url("http://%s/router?text=Hi&to=256704000000"))

    def test_that_a_none_registration_message_with_two_recipients_gets_low_priority(self):
        self.assert_low_priority(self.get_url("http://%s/router?text=Hi&to=256704000000+256704000001"))

    def test_that_a_blacklisted_message_to_one_person_gets_low_priority(self):
        self.blacklist.poll_text(231, "Blacklisted message")
        self.assert_low_priority(self.get_url("http://%s/router?text=Blacklisted+message&to=256704000000"))