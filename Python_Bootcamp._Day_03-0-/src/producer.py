import json
import logging
import random
import redis

# python3 consumer.py -e 2222222222 4444444444

logging.basicConfig(filename='tmp.log', encoding='utf-8', level=logging.DEBUG)


def generate_id():
    mylist = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    return int("".join(random.choices(mylist, k=10)))


def generate_data(from_id=0, to_id=0, amount=0):
    __data = {
        "metadata": {
            "from": from_id if from_id != 0 else generate_id(),
            "to": to_id if to_id != 0 else generate_id(),
        },
        # "amount": random.randrange(-10000, 10001)
        "amount": amount
    }
    logging.info(__data)
    return json.dumps(__data)


queue = redis.StrictRedis(host='localhost', port=6379, db=0)
channel = queue.pubsub()

queue.publish("test", generate_data(amount=-10000))
queue.publish("test", generate_data(from_id=1111111111, to_id=2222222222, amount=10000))
queue.publish("test", generate_data(from_id=3333333333, to_id=4444444444, amount=-3000))
queue.publish("test", generate_data(from_id=2222222222, to_id=5555555555, amount=5000))
queue.publish("test", generate_data(from_id=2000000000, amount=10000))
queue.publish("test", "quit")
