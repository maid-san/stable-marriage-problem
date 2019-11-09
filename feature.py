import numpy as np
import networkx as nx
from graph import GraphSolver
from statistics import mean

def count_nodes(table):
    gs = GraphSolver(table)
    return len(gs.create_graph(table).nodes())

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

def find_similar_relation(pref, sex, rank):
    n = np.shape(pref)[1]
    if rank >= n:
        raise ValueError("rank area is [1, n)")

    res = []
    for i in range(n):
        idx_tgt1 = pref[sex][i].index(rank)
        idx_tgt2 = pref[sex][i].index(rank + 1)
        for j in range(i, n):
            if pref[sex][j][idx_tgt1] == rank + 1 and pref[sex][j][idx_tgt2] == rank:
                res.append((i, j))

    return len(res), res
