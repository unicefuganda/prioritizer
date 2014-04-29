import gearman


class ThrottleClient(object):
    def __init__(self, app_config, query_string, logger=None):
        self.logger = logger
        self.app_config = app_config
        self.query_string = query_string
        self.gm_client = gearman.GearmanClient([self.app_config["GEARMAN_SERVER"]])

    def submit_high_priority_job(self):
        self.submit_background_job(gearman.PRIORITY_HIGH)

    def submit_low_priority_job(self):
        self.submit_background_job(gearman.PRIORITY_LOW)

    def submit_normal_priority_job(self):
        self.submit_background_job(gearman.PRIORITY_NONE)

    def submit_background_job(self, priority):
        if self.logger is not None:
            self.logger.info('[%s] [%s]', priority, self.query_string)
        self.gm_client.submit_job(self.app_config["ROUTER_RECEIVE_TASK_NAME"], self.query_string,
                                  priority=priority, background=True)