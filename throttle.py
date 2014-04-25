from logging.handlers import RotatingFileHandler
from flask import Flask, request
import logging
from models.throttle_client import ThrottleClient
import redis

app = Flask(__name__)
app.config.from_object('settings')

app.config["DEBUG"] = True

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


def get_redis_client():
    return redis_client

@app.route("/receive", methods=['GET'])
def throttle_incoming():
    throttle_client = ThrottleClient(app.config,request.query_string)
    throttle_client.submit_normal_priority_job()
    return "Done"

def add_logger():
    log_file = app.config.get("LOGGING_FILE", "throttle.log")
    handler = RotatingFileHandler(log_file, maxBytes=10000, backupCount=10)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    app.logger.info('info')
    app.logger.info(type(app.logger))


if __name__ == "__main__":
    add_logger()
    host = app.config.get("APPLICATION_HOST", "127.0.0.1")
    port = app.config.get("APPLICATION_PORT", 7000)
    app.run(host=host, port=port)
