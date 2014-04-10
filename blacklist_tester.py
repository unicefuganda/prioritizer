from models.encoder import Encoder
from models.prioritylist import Blacklist
import redis


def get_redis_client():
    return redis.StrictRedis(host='localhost', port=6379, db=0)

blacklist = Blacklist(get_redis_client(), Encoder())
blacklist.poll_text(232, "the beginning of time")

