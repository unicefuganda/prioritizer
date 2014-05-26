from models.encoder import Encoder
from models.prioritylist import Blacklist
import prioritizer
from tests.integration.gearman_throtle_base_test import GearmanThrottleBaseTest


class TestThrottlePrioritizerIntegration(GearmanThrottleBaseTest):

    def test_JOIN_messages_have_high_priority(self):
        high_priority_params = {'sender': '127', 'message': 'JOIN'}
        high_priority_german_url = self.generate_throttle_url(**high_priority_params)
        high_priority_ureport_url = self.generate_ureport_url(**high_priority_params)
        self.assert_high_priority(high_priority_german_url, high_priority_ureport_url)

    def test_not_JOIN_messages_have_low_priority(self):
        params = {'sender': '1234', 'message': 'anything'}
        german_url = self.generate_throttle_url(**params)
        ureport_url = self.generate_ureport_url(**params)
        self.assert_low_priority(german_url, ureport_url)

    def test_blacklisted_contacts_has_low_priority(self):
        blacklist = Blacklist(prioritizer.get_redis_client(), Encoder())
        blacklisted_number = "1234"
        blacklist.poll_contacts(231, blacklisted_number)
        params = {'sender': blacklisted_number, 'message': 'JOIN'}
        german_url = self.generate_throttle_url(**params)
        ureport_url = self.generate_ureport_url(**params)

        self.assert_low_priority(german_url, ureport_url)

        blacklist.delete_poll_contacts(231, blacklisted_number)
