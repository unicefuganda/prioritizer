from models.throttle_worker import ThrottleWorker
import settings

app_config = {"GEARMAN_SERVER": settings.GEARMAN_SERVER, "ROUTER_RECEIVE_TASK_NAME": settings.ROUTER_RECEIVE_TASK_NAME,
              "ROUTER_RECEIVE_URL": settings.ROUTER_RECEIVE_URL}

worker = ThrottleWorker(app_config)
worker.start()
