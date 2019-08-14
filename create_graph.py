import numpy as np
import networkx as nx
import copy

def create_graph(list):
    """
    create Stable Marriage Problem Graph from preference list
    """

    ret = nx.DiGraph()

    # Add node horizontal(man) direction
    for number, man_row in enumerate(list[0]):
        for i, rank_i in enumerate(man_row):
            for j, rank_j in enumerate(man_row):
                if rank_i > rank_j:
                    ret.add_edge(number * 4 + i, number * 4 + j)

    for number, woman_row in enumerate(list[1]):
        for i, rank_i in enumerate(woman_row):
            for j, rank_j in enumerate(woman_row):
                if rank_i > rank_j:
                    ret.add_edge(number + i * 4, number + j * 4)

    return ret

def create_subgraph(list, graph):
    """
    create subgraph(only woman's best and next good point) from master graph
    """

    ret = copy.deepcopy(graph)

    for number, woman_row in enumerate(list[1]):
        for i, rank in enumerate(woman_row):
            if rank != 1 and rank != 2:
                ret.remove_node(number + i * 4)

    return ret


preference = [
    [
        [1, 2, 3, 4],
        [2, 1, 4, 3],
        [4, 3, 1, 2],
        [3, 4, 2, 1]
    ],
    [
        [4, 2, 1, 3],
        [2, 4, 3, 1],
        [3, 1, 4, 2],
        [1, 3, 2, 4]
    ]
]

graph = create_graph(preference)
subgraph = create_subgraph(preference, graph)
print(list(nx.simple_cycles(subgraph)))