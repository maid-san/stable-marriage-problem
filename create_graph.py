import numpy as np
import networkx as nx
import copy
import math

class GraphSolver:
    def __init__ (self, pref):
        self.preference = pref
        self.size = len(pref[0][0])

    def get_man_best_point(self, pref):
        ret = []

        for number, man_row in enumerate(pref[0]):
            for i, rank in enumerate(man_row):
                if rank == 1:
                    ret.append(number * self.size + i)

        return ret

    def get_woman_best_point(self, pref):
        ret = []

        for number, woman_row in enumerate(pref[1]):
            for i, rank in enumerate(woman_row):
                if rank == 1:
                    ret.append(number + i * self.size)

        return ret

    def create_graph(self, pref):
        """
        create Stable Marriage Problem Graph from preference list
        """
        ret = nx.DiGraph()

        # Add edge horizontal(man) direction
        for number, man_row in enumerate(pref[0]):
            for i, rank_i in enumerate(man_row):
                for j, rank_j in enumerate(man_row):
                    if rank_i > rank_j:
                        ret.add_edge(number * self.size + i, number * self.size + j)

        # Add edge vertical(woman) direction
        for number, woman_row in enumerate(pref[1]):
            for i, rank_i in enumerate(woman_row):
                for j, rank_j in enumerate(woman_row):
                    if rank_i > rank_j:
                        ret.add_edge(number + i * self.size, number + j * self.size)

        return ret

    def contract_graph(self, graph, man_best_point, woman_best_point):
        ret = copy.deepcopy(graph)
        delete = []

        for m in man_best_point:
            for pre in list(graph.predecessors(m)):
                if m % self.size == pre % self.size:
                    delete.append(pre)

        for w in woman_best_point:
            for pre in list(graph.predecessors(w)):
                if w / self.size == pre / self.size:
                    delete.append(pre)

        delete = list(set(delete))
        for d in delete:
            ret.remove_node(d)

        return ret, delete

    def create_subgraph(self, pref, graph):
        """
        create subgraph(only woman's best and next good point) from master graph
        """
        ret = copy.deepcopy(graph)

        for number, woman_row in enumerate(pref[1]):
            for i, rank in enumerate(woman_row):
                if not math.isnan(rank):
                    if rank != 1 and rank != 2:
                        ret.remove_node(number + i * self.size)

        return ret

    def reflesh_preference(self, pref, delete):
        ret = copy.deepcopy(pref)

        for d in delete:
            d_i = d / self.size
            d_j = d % self.size

            for i, man_row in enumerate(ret[0]):
                if i == d_i:
                    for j, rank in enumerate(man_row):
                        if j == d_j:
                            ret[0][i][j] = float('nan')
                        elif rank > pref[0][d_i][d_j]:
                            ret[0][i][j] -= 1

            for i, woman_row in enumerate(ret[1]):
                if i == d_j:
                    for j, rank in enumerate(woman_row):
                        if j == d_i:
                            ret[1][i][j] = float('nan')
                        elif rank > pref[1][d_j][d_i]:
                            ret[1][i][j] -= 1

        return ret

    def how_many_stable_matching(self):
        pref = copy.deepcopy(self.preference)
        i = 1

        _, delete_point = self.contract_graph(self.create_graph(pref), self.get_man_best_point(pref), self.get_woman_best_point(pref))
        pref = self.reflesh_preference(pref, delete_point)

        while True:
            graph    = self.create_graph(pref)
            subgraph = self.create_subgraph(pref, graph)
            cycles = list(nx.simple_cycles(subgraph))
            if len(cycles) == 0:
                break
            delete_point = list(set(cycles[0]) & set(self.get_woman_best_point(pref)))
            pref = self.reflesh_preference(pref, delete_point)

            i += len(cycles)
        return i

# Test Code
pref = [
            [
                [1, 2, 3],
                [3, 1, 2],
                [3, 2, 1]
            ],
            [
                [3, 1, 2],
                [1, 3, 2],
                [3, 1, 2]
            ]
        ]

gs = GraphSolver(pref)
print("Matching: " + str(gs.how_many_stable_matching()))
