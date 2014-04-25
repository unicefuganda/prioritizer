import gearman
import requests


class ThrottleWorker(object):

    def __init__(self, app_config):
        self.app_config = app_config
        self.gm_worker = gearman.GearmanWorker([self.app_config["GEARMAN_SERVER"]])
        self.gm_worker.register_task(self.app_config["ROUTER_RECEIVE_TASK_NAME"], self.call_router_receive)

    def call_router_receive(self, gearman_worker, gearman_job):
        url = "%s?%s" % (self.app_config["ROUTER_RECEIVE_URL"], gearman_job.data)
        # print "[INFO] %s" % url
        requests.get(url)
        return "ok"

    def start(self):
        self.gm_worker.work()