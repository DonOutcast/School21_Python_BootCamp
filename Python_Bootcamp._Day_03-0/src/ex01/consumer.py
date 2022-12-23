import redis
import json
import sys
import random
import time
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('log')


def read_bad_guys():
    bad_list = []
    if sys.argv[1] == '-e':
        for guy in sys.argv[2].split(','):
            if len(guy) == 10:
                bad_list.append(int(guy))
    return bad_list


def change_pubsub(bad_guys):
    r = redis.Redis(
        host='localhost',
        port=6379,
        password='',
        charset="utf-8",
        decode_responses=True,
    )
    flag = 0
    keys = ['from', 'to']
    listener = r.pubsub(ignore_subscribe_messages=True)
    listener.subscribe('producer')
    for message in listener.listen():
        message = json.loads(message['data'])
        metadata = message['metadata']
        from_user = metadata['from']
        to_user = metadata['to']
        amount = message['amount']
        if ((from_user in bad_guys) and amount > 0) or ((to_user in bad_guys) and amount > 0):
            ids = to_user, from_user
            metadata = dict(zip(keys, ids))
            message = {'metadata': metadata, 'amount': amount}
            message = json.dumps(message)
            logger.info(message)
        else:
            logger.info(message)
        flag += 1
        time.sleep(0.001)
        if flag == 20:
            listener.close()


if __name__ == "__main__":
    change_pubsub(read_bad_guys())
