import gearman


class ThrottleClient(object):
    def __init__(self, app_config, query_string):
        self.app_config = app_config
        self.query_string = query_string
        self.gm_client = gearman.GearmanClient([self.app_config["GEARMAN_SERVER"]])

    def submit_high_priority_job(self):
        self.gm_client.submit_job(self.app_config["ROUTER_RECEIVE_TASK_NAME"], self.query_string,
                                  priority=gearman.PRIORITY_HIGH, background=True)

    def submit_low_priority_job(self):
        self.gm_client.submit_job(self.app_config["ROUTER_RECEIVE_TASK_NAME"], self.query_string,
                                  priority=gearman.PRIORITY_LOW, background=True)

    def submit_normal_priority_job(self):
        self.gm_client.submit_job(self.app_config["ROUTER_RECEIVE_TASK_NAME"], self.query_string, background=True)