from tests.integration.gearman_throtle_base_test import GearmanThrottleBaseTest


class TestThrottlePrioritizerIntegration(GearmanThrottleBaseTest):

    def test_get_requests_from_throttle_triggers_workers_to_write_log_files_in_priority_order(self):
        high_priority_params = {'sender': '127', 'message': 'JOIN'}
        high_priority_german_url = self.generate_throttle_url(**high_priority_params)
        high_priority_ureport_url = self.generate_ureport_url(**high_priority_params)
        self.assert_high_priority(high_priority_german_url, high_priority_ureport_url)
