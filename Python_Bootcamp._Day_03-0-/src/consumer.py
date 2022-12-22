import redis
import sys
import json

bad_guys = []
if len(sys.argv) > 1 and sys.argv[1] == '-e':
    bad_guys = [int(arg) for arg in sys.argv[2:]]

r = redis.StrictRedis(host='localhost', port=6379, db=0)
p = r.pubsub()
p.subscribe('test')

for m in p.listen():
    if len(bad_guys) > 0:
        if type(m['data']) == bytes:
            if m['data'].decode('utf-8') == 'quit':
                break
            data = json.loads(m['data'].decode('utf-8'))
            from_id = int(data.get('metadata', {}).get('from', 0))
            to_id = int(data.get('metadata', {}).get('to', 0))
            amount = data.get('amount', 0)
            if to_id in bad_guys and amount > 0:
                data['metadata']['from'] = to_id
                data['metadata']['to'] = from_id
            print(data)
