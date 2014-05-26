from logging.handlers import RotatingFileHandler
from flask import Flask, request
import logging
from models.encoder import Encoder
from models.filter_processor import FilterProcessor
from models.incoming_contact_filter import IncomingContactFilter
from models.keyword_filter import KeywordFilter
from models.priority import Priority
from models.prioritylist import Whitelist, Blacklist
from models.throttle_client import ThrottleClient
from models.whitelist_contact_filter import WhitelistContactFilter
import redis

app = Flask(__name__)
app.config.from_object('settings')

app.config["DEBUG"] = True

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


def get_redis_client():
    return redis_client


def process_request(app_config, query_string, priority):
    throttle_client = ThrottleClient(app_config, query_string, app.logger)

    if priority is Priority.HIGH:
        throttle_client.submit_high_priority_job()

    elif priority is Priority.LOW:
        throttle_client.submit_low_priority_job()

    else:
        throttle_client.submit_normal_priority_job()


@app.route("/receive", methods=['GET'])
def throttle_incoming():
    whitelist = Whitelist(get_redis_client(), Encoder())
    blacklist = Blacklist(get_redis_client(), Encoder())
    contact = request.args.get('sender')
    message = request.args.get('message')

    keyword_filter = KeywordFilter(whitelist, message, contact)
    contact_filter = WhitelistContactFilter(whitelist, contact)
    incoming_contact_filter = IncomingContactFilter(blacklist, contact)

    high_filters = [keyword_filter, contact_filter]
    low_filters = [incoming_contact_filter]

    processor = FilterProcessor(high_filters, low_filters)
    priority = processor.execute()

    process_request(app.config, request.query_string, priority)

    return "Done"


def add_logger():
    log_file = app.config.get("LOGGING_FILE", "throttle.log")
    handler = RotatingFileHandler(log_file, maxBytes=10000, backupCount=10)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    app.logger.info(type(app.logger))


if __name__ == "__main__":
    add_logger()
    host = app.config.get("APPLICATION_HOST", "127.0.0.1")
    port = app.config.get("APPLICATION_PORT", 7000)
    app.run(host=host, port=port)
