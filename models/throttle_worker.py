import gearman
import requests


class ThrottleWorker(object):

    def __init__(self, app_config, client_id="throttle-worker", logger=None):
        self.app_config = app_config
        self.logger = logger
        self.gm_worker = gearman.GearmanWorker([self.app_config["GEARMAN_SERVER"]])
        self.gm_worker.register_task(self.app_config["ROUTER_RECEIVE_TASK_NAME"], self.call_router_receive)
        self.gm_worker.set_client_id(client_id)

    def call_router_receive(self, gearman_worker, gearman_job):
        url = "%s?password=%s&%s" % (self.app_config["ROUTER_RECEIVE_URL"], self.app_config["UREPORT_APP_PASSWORD"], gearman_job.data)
        if self.logger is not None:
            self.log_info(gearman_job, gearman_worker, url)
        requests.get(url)
        return "ok"

    def start(self):
        self.gm_worker.work()

    def log_info(self, gearman_job, gearman_worker, url):
        self.logger.info("---------------")
        self.logger.info("[%s] - [%s] - [%s] - (%s)", gearman_job.unique, gearman_worker.worker_client_id, gearman_job.task, gearman_job.data)
        self.logger.info("%s", url)
