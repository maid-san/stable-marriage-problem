import numpy as np
import networkx as nx
from graph import GraphSolver
from statistics import mean

def calc_latin_feature(table):
    n = np.shape(table)[1]

    arr = []
    for i in range(n):
        for j in range(n):
            a = table[0][i][j]
            b = table[1][j][i]

            if np.isnan(a) or np.isnan(b):
                continue

            arr.append(np.abs((a + b) - (n + 1)))

    return np.mean(arr)

def calc_latin_feature_2(table):
    n = np.shape(table)[1]

    arr = []
    for i in range(n):
        for j in range(n):
            a = table[0][i][j]
            b = table[1][j][i]

            if np.isnan(a) or np.isnan(b):
                continue

            arr.append(a + b)

    return np.var(arr)

def count_nodes(table):
    gs = GraphSolver(table)
    return len(gs.create_graph(table).nodes())

def count_maximam_rotation_nodes(rotations):
    if len(rotations) == 0:
        return 0

    lens = [len(rotation) for rotation in rotations]
    return max(lens)

def count_large_rotation(rotations):
    if len(rotations) == 0:
        return 0

    lens = [len(rotation) for rotation in rotations if len(rotation) > 4]
    return len(lens)

def calc_rotation_latin_feature(table):
    n = np.shape(table)[1]

    gs = GraphSolver(table)
    _, delete_point = gs.contract_graph(gs.create_graph(table), gs.get_points(table, 0, 1), gs.get_points(table, 1, 1))
    table = gs.reflesh_preference(table, delete_point)

    res = []
    while True:
        rotations = gs.find_rotations(table)

        if len(rotations) == 0:
            break

        for rotation in rotations:
            tmp = []
            for node in rotation:
                n_i = node // n
                n_j = node %  n

                a = table[0][n_i][n_j]
                b = table[1][n_j][n_i]

                tmp.append(np.abs((a + b) - (n + 1)))
            res.append(np.mean(tmp))

        delete_point = list(set(rotations[0]) & set(gs.get_points(table, 1, 1)))
        table = gs.reflesh_preference(table, delete_point)

    if len(res) != 0:
        return np.mean(res), res
    else:
        return n - 1

def calc_rotation_latin_feature_2(table):
    n = np.shape(table)[1]

    gs = GraphSolver(table)
    _, delete_point = gs.contract_graph(gs.create_graph(table), gs.get_points(table, 0, 1), gs.get_points(table, 1, 1))
    table = gs.reflesh_preference(table, delete_point)

    res = []
    while True:
        rotations = gs.find_rotations(table)

        if len(rotations) == 0:
            break

        for rotation in rotations:
            tmp = []
            for node in rotation:
                n_i = node // n
                n_j = node %  n

                a = table[0][n_i][n_j]
                b = table[1][n_j][n_i]

                tmp.append(a + b)
            res.append(np.var(tmp))

        delete_point = list(set(rotations[0]) & set(gs.get_points(table, 1, 1)))
        table = gs.reflesh_preference(table, delete_point)

    if len(res) != 0:
        return np.mean(res), res
    else:
        return n - 1

def count_latin_rotation(rotations_latin_feature):
    matching = [f for f in rotations_latin_feature if f == 0]

    return len(matching)

def count_strong_latinly_rotation(rotations_latin_feature):
    matching = [f for f in rotations_latin_feature if f < 0.25]

    return len(matching)