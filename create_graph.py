import numpy as np
import networkx as nx
import copy
import math
import pprint

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
            if not math.isnan(rank):
                if rank != 1 and rank != 2:
                    ret.remove_node(number + i * 4)

    return ret

def get_woman_best_point(list):
    ret = []

    for number, woman_row in enumerate(list[1]):
        for i, rank in enumerate(woman_row):
            if rank == 1:
                ret.append(number + i * 4)

    return ret

def reflesh_preference(preference, delete):
    ret = copy.deepcopy(preference)

    for d in delete:
        d_i = d / 4
        d_j = d % 4

        for i, man_row in enumerate(ret[0]):
            if i == d_i:
                for j, rank in enumerate(man_row):
                    if j == d_j:
                        ret[0][i][j] = float('nan')
                    elif rank > ret[0][d_i][d_j]:
                        ret[0][i][j] -= 1

        for i, woman_row in enumerate(ret[1]):
            for j, _ in enumerate(woman_row):
                if j == d_i:
                    if ret[1][i][j] == 1:
                        ret[1][i][j] = float('nan')
                    else:
                        ret[1][i][j] -= 1

    return ret


preference = [
    [
        [1, 2, 3, 4],
        [2, 1, 4, 3],
        [3, 4, 1, 2],
        [4, 3, 2, 1]
    ],
    [
        [4, 3, 2, 1],
        [3, 4, 1, 2],
        [2, 1, 4, 3],
        [1, 2, 3, 4]
    ]
]

i = 1
while True:
    woman_best_point = get_woman_best_point(preference)
    print("woman_best_point: " + str(woman_best_point))
    graph = create_graph(preference)
    subgraph = create_subgraph(preference, graph)
    cycles = list(nx.simple_cycles(subgraph))
    print(cycles)
    if len(cycles) == 0:
        break
    delete_point = list(set(cycles[0]) & set(woman_best_point))
    preference = reflesh_preference(preference, delete_point)

    i += 1
print("count of stable matching: " + str(i))