import numpy as np
import networkx as nx
from graph import GraphSolver
from statistics import mean

def calc_latin_feature(table):
    n = np.shape(table)[1]

    res = 0
    number = 0
    for i in range(n):
        for j in range(n):
            a = table[0][i][j]
            b = table[1][j][i]

            if np.isnan(a) or np.isnan(b):
                continue

            res += np.abs((a + b) - (n + 1))
            number += 1

    return res / number

def calc_rotation_number(table):
    n  = np.shape(table)[1]
    gs = GraphSolver(table)

    _, delete_point = gs.contract_graph(gs.create_graph(table),
    gs.get_points(table, 0, 1), gs.get_points(table, 1, 1))
    table = gs.reflesh_preference(table, delete_point)
    rotations = gs.find_rotations(table)

    return len(rotations)

def calc_rotation_latin(table):
    n = np.shape(table)[1]

    gs = GraphSolver(table)
    _, delete_point = gs.contract_graph(gs.create_graph(table), gs.get_points(table, 0, 1), gs.get_points(table, 1, 1))
    table = gs.reflesh_preference(table, delete_point)

    rotations = gs.find_rotations(table)

    if len(rotations) == 0:
        return n - 1

    res = []
    for rot in rotations:
        tmp = 0
        i = 0
        for node in rot:
            i += 1
            n_i = node // n
            n_j = node %  n

            a = table[0][n_i][n_j]
            b = table[1][n_j][n_i]

            tmp += np.abs((a + b) - (n + 1))
        res.append(tmp / i)

    return mean(res)
