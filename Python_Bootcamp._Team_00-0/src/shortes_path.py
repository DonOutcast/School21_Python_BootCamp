import argparse
from os import environ
import json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--from', type=str, required=True)
    parser.add_argument('--to', type=str, required=True)
    parser.add_argument('--non-directed', action='store_true')
    parser.add_argument('-v', action='store_true')
    args = parser.parse_args()

    graph_file = environ.get('WIKI_FILE', 'cache.json')
    with open(graph_file, 'r') as file:
        graph = json.loads(file.read())

    start = args.__dict__['from']
    finish = args.to
    if start not in graph['nodes'] or finish not in graph['nodes']:
        raise ValueError('incorrect node name')
    non_directed = args.__dict__['non_directed']

    found_exit = False
    distances = {start: 0}
    to_process = [start]
    measured = [start]

    while len(to_process) > 0 and not found_exit:
        for i in graph['edges']:
            if i['from'] == to_process[0] \
                    and i['to'] not in measured:
                distances[i['to']] = distances[i['from']] + 1
                measured.append(i['to'])
                to_process.append(i['to'])
                if i['to'] == finish:
                    found_exit = True
                    break
            if non_directed:
                if i['to'] == to_process[0] \
                        and i['from'] not in measured:
                    distances[i['from']] = distances[i['to']] + 1
                    measured.append(i['from'])
                    to_process.append(i['from'])
                    if i['from'] == finish:
                        found_exit = True
                        break
        to_process.pop(0)

    if found_exit:
        if (args.v):
            path = [finish]
            dist = distances[finish]
            cur_node = finish
            while dist > 1:
                for i in graph['nodes']:
                    if distances[i] == dist - 1:
                        for j in graph['edges']:
                            if j['from'] == i and j['to'] == cur_node:
                                cur_node = j['from']
                                break
                            elif non_directed \
                                    and j['to'] == i \
                                    and j['from'] == cur_node:
                                cur_node = j['to']
                                break
                path.insert(0, cur_node)
                dist -= 1
            path.insert(0, start)
            path = [f"'{i}'" for i in path]
            print(' -> '.join(path))
        print(distances[finish])
    else:
        print('Path not found')


if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        print(err)
