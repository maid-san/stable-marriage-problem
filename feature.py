import numpy as np
import networkx as nx
from graph import GraphSolver
from statistics import mean

def count_nodes(table):
    gs = GraphSolver(table)
    return len(gs.create_graph(table).nodes())

def count_first_rotation(table):
    gs = GraphSolver(table)
    _, delete_point = gs.contract_graph(gs.create_graph(table), gs.get_points(table, 0, 1), gs.get_points(table, 1, 1))
    table = gs.reflesh_preference(table, delete_point)
    return len(gs.find_rotations(table))

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

def calc_latin_feature_3(table):
    n = np.shape(table)[1]

    arr = []

    for i in range(n):
        tmp = []
        count_nan = len(table[1][i])
        for j in range(n):
            a = table[1][i][j]
            b = table[0][j][i]

            if np.isnan(a) or np.isnan(b):
                continue
            tmp.append(np.abs(a + b) - (n - count_nan + 1))
        arr.append(np.var(tmp))

    return np.mean(arr)

def calc_cyclic_feature(pref):
    n = np.shape(pref)[0]
    dis = []

    for i in range(n):
        if i == len(pref) - 1:
            j = 0
        else:
            j = i + 1

        a = np.array(pref[i])
        b = np.array(pref[j])

        a[np.isnan(a)] = n + 1
        b[np.isnan(b)] = n + 1

        dis.append(np.linalg.norm(a - b))

    return np.var(dis)

def calc_cyclic_feature_2(pref):
    n = np.shape(pref)[0]
    dis = []

    for i in range(n):
        if i == len(pref) - 1:
            j = 0
        else:
            j = i + 1

        a = np.array(pref[i])
        b = np.array(pref[j])

        a[np.isnan(a)] = n + 1
        b[np.isnan(b)] = n + 1

        dis.append(np.linalg.norm(a - b))

    return np.mean(dis)

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

def calc_preference_distance(pref):
    dis = []
    n = np.shape(pref)[0]

    for i in range(len(pref)):
        for j in range(i + 1, len(pref)):
            a = np.array(pref[i])
            b = np.array(pref[j])

            a[np.isnan(a)] = n + 1
            b[np.isnan(b)] = n + 1

            dis.append(np.linalg.norm(a - b))

    return np.mean(dis)

def count_latin_rotation(rotations_latin_feature):
    matching = [f for f in rotations_latin_feature if f == 0]

    return len(matching)

def count_strong_latinly_rotation(rotations_latin_feature):
    matching = [f for f in rotations_latin_feature if f < 0.25]

    return len(matching)

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