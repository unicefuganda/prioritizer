import sys
from models.throttle_worker import ThrottleWorker
import settings
import logging

app_config = {"GEARMAN_SERVER": settings.GEARMAN_SERVER, "ROUTER_RECEIVE_TASK_NAME": settings.ROUTER_RECEIVE_TASK_NAME,
              "ROUTER_RECEIVE_URL": settings.ROUTER_RECEIVE_URL, "UREPORT_APP_PASSWORD": settings.UREPORT_APP_PASSWORD }

logging.basicConfig(filename=settings.THROTTLE_WORK_LOG_FILE, level=logging.INFO)

if len(sys.argv) == 1:
    print "Worker client id is required."
    exit()

worker_name = "worker-%s" % str(sys.argv[1])
logging.info("Starting worker: %s", worker_name)

worker = ThrottleWorker(app_config, worker_name, logging)
worker.start()
