import numpy as np
import networkx as nx
import copy
import math
import pprint

class GraphSolver:
    def __init__ (self, pref):
        self.preference = pref
        self.size = len(self.preference[0][0])

    def create_graph(self, list):
        """
        create Stable Marriage Problem Graph from preference list
        """

        ret = nx.DiGraph()

        # Add edge horizontal(man) direction
        for number, man_row in enumerate(list[0]):
            for i, rank_i in enumerate(man_row):
                for j, rank_j in enumerate(man_row):
                    if rank_i > rank_j:
                        ret.add_edge(number * self.size + i, number * self.size + j)

        # Add edge vertical(woman) direction
        for number, woman_row in enumerate(list[1]):
            for i, rank_i in enumerate(woman_row):
                for j, rank_j in enumerate(woman_row):
                    if rank_i > rank_j:
                        ret.add_edge(number + i * self.size, number + j * self.size)

        return ret

    def create_subgraph(self, list, graph):
        """
        create subgraph(only woman's best and next good point) from master graph
        """

        ret = copy.deepcopy(graph)

        for number, woman_row in enumerate(list[1]):
            for i, rank in enumerate(woman_row):
                if not math.isnan(rank):
                    if rank != 1 and rank != 2:
                        ret.remove_node(number + i * self.size)

        return ret

    def get_woman_best_point(self, list):
        ret = []

        for number, woman_row in enumerate(list[1]):
            for i, rank in enumerate(woman_row):
                if rank == 1:
                    ret.append(number + i * self.size)

        return ret

    def get_man_best_point(self, list):
        ret = []

        for number, man_row in enumerate(list[0]):
            for i, rank in enumerate(man_row):
                if rank == 1:
                    ret.append(number * self.size + i)

        return ret

    def contract_graph (self, graph, man_best_point, woman_best_point):


        return graph

    def reflesh_preference(self, preference, delete):
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

    def how_many_stable_matching (self):
        pref = copy.deepcopy(self.preference)
        i = 1

        while True:
            graph = self.create_graph(pref)
            subgraph = self.create_subgraph(pref, graph)
            cycles = list(nx.simple_cycles(subgraph))

            # print("cycles: " + str(cycles))
            if len(cycles) == 0:
                break

            woman_best_point = self.get_woman_best_point(pref)
            delete_point = list(set(cycles[0]) & set(woman_best_point))
            pref = self.reflesh_preference(pref, delete_point)

            i += len(cycles)
        return i

pref = [
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

gs = GraphSolver(pref)
print("Matching: " + str(gs.how_many_stable_matching()))