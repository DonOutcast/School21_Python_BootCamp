import redis
import json
import random
import time
import logging
#  python3 consumer.py -e 2222222222 1111111111


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('log')


def queue_publish(count=10):
    r = redis.Redis(
        host='localhost',
        port=6379,
        password='',
        charset="utf-8",
        decode_responses=True,
    )
    keys = ['from', 'to']
    ids = [1111111111, 5625162372, 7833780089, 4815162342]
    for i in range(count):
        id_for_send = random.sample(ids, k=2)
        metadata = dict(zip(keys, id_for_send))
        message = {'metadata': metadata, 'amount': random.randint(-1000, 1000)}
        message = json.dumps(message)
        logger.info(message)
        time.sleep(0.001)
    ids = [2222222222, 3133780085, 5625162372, 7833780089]
    for i in range(count):
        id_for_send = random.sample(ids, k=2)
        metadata = dict(zip(keys, id_for_send))
        message = {'metadata': metadata, 'amount': random.randint(-1000, 1000)}
        json_obj = json.dumps(message)
        logger.info(message)
        r.set("producer", json_obj)
        r.publish('producer', json_obj)
        time.sleep(0.001)
    r.close()


if __name__ == "__main__":
    queue_publish(10)
