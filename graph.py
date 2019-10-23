import numpy as np
import networkx as nx
import copy
import math

class GraphSolver:
    def __init__ (self, pref):
        self.preference = pref
        self.size = len(pref[0][0])

    def get_points(self, pref, sex, tgt):
        """
        sex: 0=man, 1=woman
        tgt: target rank
        """
        ret = []

        for number, row in enumerate(pref[sex]):
            for i, rank in enumerate(row):
                if rank == tgt:
                    if sex == 0:
                        ret.append(number * self.size + i)
                    elif sex == 1:
                        ret.append(number + i * self.size)
                    else:
                        return

        return ret

    def is_decomposed(self, graph):
        return not nx.is_weakly_connected(graph)

    def is_subset(self, list1, list2):
        return set(list1).issubset(list2)

    def is_rotation(self, pref, cycle):
        if len(cycle) % 2 != 0:
            return False

        woman_best_points = self.get_points(pref, 1, 1)
        woman_next_points = self.get_points(pref, 1, 2)

        return self.is_subset(cycle[0::2], woman_best_points) and self.is_subset(cycle[1::2], woman_next_points) or \
               self.is_subset(cycle[1::2], woman_best_points) and self.is_subset(cycle[0::2], woman_next_points)

    def create_graph(self, pref):
        """
        Create Stable Marriage Problem Graph from preference list.
        """
        ret = nx.DiGraph()

        # Add edge horizontal(man) direction
        for number, man_row in enumerate(pref[0]):
            for i, rank_i in enumerate(man_row):
                for j, rank_j in enumerate(man_row):
                    if rank_i > rank_j:
                        ret.add_edge(number * self.size + i, number * self.size + j)
                    if rank_j == 1:
                        ret.add_node(number * self.size + j)

        # Add edge vertical(woman) direction
        for number, woman_row in enumerate(pref[1]):
            for i, rank_i in enumerate(woman_row):
                for j, rank_j in enumerate(woman_row):
                    if rank_i > rank_j:
                        ret.add_edge(number + i * self.size, number + j * self.size)
                    if rank_j == 1:
                        ret.add_node(number + j * self.size)

        return ret

    def contract_graph(self, graph, man_best_point, woman_best_point):
        """
        Delete the points which is linked into man's best point vertical direction and linked into woman's horizontal direction.
        """
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
        Create subgraph(only woman's best and next good point) from master graph
        """
        ret = copy.deepcopy(graph)

        for number, woman_row in enumerate(pref[1]):
            for i, rank in enumerate(woman_row):
                if not math.isnan(rank):
                    if rank != 1 and rank != 2:
                        ret.remove_node(number + i * self.size)

        return ret

    def reflesh_preference(self, old_pref, delete):
        """
        Delete any points from preference list and reflesh preference rank.
        """
        new_pref = copy.deepcopy(old_pref)

        for d in delete:
            d_i = d // self.size
            d_j = d % self.size

            for i, man_row in enumerate(new_pref[0]):
                if i == d_i:
                    for j, rank in enumerate(man_row):
                        if j == d_j:
                            new_pref[0][i][j] = float('nan')
                        elif rank > old_pref[0][d_i][d_j]:
                            new_pref[0][i][j] -= 1

            for i, woman_row in enumerate(new_pref[1]):
                if i == d_j:
                    for j, rank in enumerate(woman_row):
                        if j == d_i:
                            new_pref[1][i][j] = float('nan')
                        elif rank > old_pref[1][d_j][d_i]:
                            new_pref[1][i][j] -= 1

        return new_pref

    def how_many_stable_matching(self):
        """
        Count the stable matching from the member's preference list.
        """

        pref = copy.deepcopy(self.preference)
        i = 1

        _, delete_point = self.contract_graph(self.create_graph(pref), self.get_points(pref, 0, 1), self.get_points(pref, 1, 1))
        pref = self.reflesh_preference(pref, delete_point)

        while True:
            graph    = self.create_graph(pref)
            subgraph = self.create_subgraph(pref, graph)
            rotations = [c for c in list(nx.simple_cycles(subgraph)) if self.is_rotation(pref, c) == True]
            if len(rotations) == 0:
                break
            delete_point = list(set(rotations[0]) & set(self.get_points(pref, 1, 1)))
            pref = self.reflesh_preference(pref, delete_point)

            i += len(rotations)
        return i