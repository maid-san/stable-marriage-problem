def is_std_impl(table, reference):
    n = np.shape(table)[1]
    for i in range(n):
        tmp = np.copy(table)

        tmp[0][0], tmp[0][i] = tmp[0][i], np.copy(tmp[0][0])
        tmp[1][:, 0], tmp[1][:, i] = tmp[1][:, i], np.copy(tmp[1][:, 0])

        order = np.argsort(tmp[0][0])
        tmp[0] = tmp[0][:, order]
        tmp[1] = tmp[1][order, :]

        tmp_tmp = np.hstack([tmp[0], tmp[1].T])
        order = np.lexsort(np.rot90(tmp_tmp))
        tmp[0] = tmp[0][order, :]
        tmp[1] = tmp[1][:, order]

        if lex_comp(tmp.reshape(-1,), reference):
            return False

    return True

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

def count_first_rotation(table):
    gs = GraphSolver(table)
    _, delete_point = gs.contract_graph(gs.create_graph(table), gs.get_points(table, 0, 1), gs.get_points(table, 1, 1))
    table = gs.reflesh_preference(table, delete_point)
    return len(gs.find_rotations(table))

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

def calc_node_adjacency(pref):
    n = np.shape(pref)[1]
    adj = []

    for row in pref[1]:
        adj.append(abs(row.index(1) - row.index(2)))

    adj = [1 if i == n-1 else i for i in adj]

    return np.mean(adj)

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