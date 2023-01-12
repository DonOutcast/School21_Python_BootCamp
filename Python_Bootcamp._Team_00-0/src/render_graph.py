import networkx as nx
import matplotlib.pyplot as plt
import json
from collections import Counter
from os import environ
import numpy as np
import altair as alt
import nx_altair as nxa

kNodeSize = 100
kMinNodes = 10
kPicWidth = 6.4
kPicHeight = 4.8


def size_formula(connections: int):
    return connections * kNodeSize


def main():
    graph_file = environ.get('WIKI_FILE', 'test_graph.json')
    with open(graph_file, 'r') as file:
        content = json.loads(file.read())

    graph = nx.Graph()
    connections = Counter()
    for i in content['edges']:
        if i['to'] in content['nodes'] and i['from'] != i['to']:
            graph.add_edge(i['from'], i['to'])
            connections[i['from']] += 1
            connections[i['to']] += 1

    sizes = [size_formula(connections[i]) for i in graph.nodes]
    num_nodes = len(graph.nodes)
    pic_size_coef = num_nodes ** 0.5
    if pic_size_coef < 1:
        pic_size_coef = 1

    plt.figure(figsize=(kPicWidth * pic_size_coef, \
                        kPicHeight * pic_size_coef))
    nx.spring_layout(graph)
    nx.draw(graph, with_labels=True, node_size=sizes, alpha=0.8, edge_color=(0.5, 0.5, 0.5))
    plt.savefig('wiki_graph.png')

    # bonus part
    for i in graph.nodes:
        graph.nodes[i]['name'] = i
        graph.nodes[i]['connections'] = connections[i]
    chart = nxa.draw_networkx(
        G=graph,
        node_color='connections',
        node_tooltip=['name', 'connections']
    ).properties(
        width=640,
        height=480
    )

    chart.save('wiki_graph.html')


if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        print(err)
