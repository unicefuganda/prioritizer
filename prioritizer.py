from flask import Flask, request
from models.blacklist_filter import BlacklistFilter
from models.encoder import Encoder
from models.filter_processor import FilterProcessor
from models.prioritylist import Blacklist
from models.receiver_count_filter import ReceiverCountFilter
from models.smsc_router import SMSCRouter
import redis
from models.caching_steps import StepsCache
from models.priority import Priority
from models.registration_message_filter import RegistrationMessageFilter
import logging
from logging.handlers import RotatingFileHandler


app = Flask(__name__)
app.config.from_object('settings')

app.config["DEBUG"] = True

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


def get_redis_client():
    return redis_client


def get_steps_cache_instance():
    steps_cache = StepsCache(get_redis_client(),
                             app.logger,
                             app.config["REGISTRATION_STEPS_API_USERNAME"],
                             app.config["REGISTRATION_STEPS_API_PASSWORD"],
                             app.config["REGISTRATION_STEPS_API_URL"],
                             app.config["STEPS_CACHE_KEY_NAME"])
    return steps_cache


@app.route("/router", methods=['GET'])
def outgoing_message_router():
    message = request.args.get('text', None)
    receivers = request.args.get('to', '')

    message_filter = RegistrationMessageFilter(get_steps_cache_instance(), message)
    receiver_count_filter = ReceiverCountFilter(receivers.split("+"), 1)

    blacklist = Blacklist(get_redis_client(), Encoder())
    blacklist_filter = BlacklistFilter(blacklist, message)

    high_filters = [message_filter, receiver_count_filter]
    low_filters = [blacklist_filter]

    processor = FilterProcessor(high_filters, low_filters)
    priority = processor.execute()

    smsc_router = SMSCRouter(app.config, app.logger)
    smsc_router.route(request.args, priority)

    return "Done"


@app.route("/update_script_steps")
def update_script_steps():
    steps_cache = get_steps_cache_instance()
    steps_cache.delete_script_steps_data()
    steps_cache.add_script_steps_data()
    return "Steps script in cache successfully updated"


blacklist = Blacklist(get_redis_client(), Encoder())


@app.route("/blacklist/add", methods=['POST'])
def add_poll_to_blacklist():
    blacklist.poll_text(request.form["poll_id"], request.form["poll_text"])
    blacklist.poll_text(request.form["poll_id"], request.form["poll_response"])
    return "Done"


@app.route("/blacklist/delete", methods=['POST'])
def delete_poll_from_blacklist():
    blacklist.delete_poll_text(request.form["poll_id"], request.form["poll_text"])
    blacklist.delete_poll_text(request.form["poll_id"], request.form["poll_response"])
    return "Done"


@app.route("/blacklist/contacts", methods=['POST'])
def add_poll_contacts_to_blacklist():
    poll_id = int(request.args.get("poll_id"))
    blacklist.poll_contacts(poll_id, request.get_json(True))
    return "Done"


def add_logger():
    log_file = app.config.get("LOGGING_FILE", "prioritizer.log")
    handler = RotatingFileHandler(log_file, maxBytes=10000, backupCount=10)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    app.logger.info('info')
    app.logger.info(type(app.logger))


if __name__ == "__main__":
    add_logger()
    host = app.config.get("APPLICATION_HOST", "127.0.0.1")
    port = app.config.get("APPLICATION_PORT", 5000)
    app.run(host=host, port=port)
