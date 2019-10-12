import numpy as np
import itertools
import os

def create_instances_file(n):
    d = {key:chr(i + 65) for i, key in enumerate(itertools.permutations([i + 1 for i in range(n)]))}

    with open("./tmp.txt", mode='w') as f:
        for instance in itertools.product(itertools.permutations([i + 1 for i in range(n)]), repeat=n*2 - 1):
            instance = np.insert(np.array(instance), 0, [i + 1 for i in range(n)])
            for i in std(instance.reshape(2, n, n)):
                for j in i:
                    f.write(d[tuple(j.tolist())])
            f.write("\n")

    os.system(f"cat tmp.txt | sort | uniq > size{n}_instances_a.txt")
    os.system(f"rm tmp.txt")

def create_table(alphabets):
    size = len(alphabets) / 2
    d = {chr(i + 65):data for i, data in enumerate(itertools.permutations([i + 1 for i in range(size)]))}

    ret = [[[0 for i in range(size)] for j in range(size)] for k in range(2)]
    for i in range(2):
        for j in range(size):
            ret[i][j] = list(d[alphabets[i*2 + j]])

    return ret

def comp(lhs, rhs):
    for l, r in zip(lhs, rhs):
        if l < r:
            return True
        elif l > r:
            return False
    return False

def std_impl(table):
    n = np.shape(table)[1]

    res = np.copy(table)
    for i in range(n):
        tmp = np.copy(table)

        tmp[0][0], tmp[0][i] = tmp[0][i], np.copy(tmp[0][0])
        tmp[1][:, 0], tmp[1][:, i] = tmp[1][:, i], np.copy(tmp[1][:, 0])

        order = np.argsort(tmp[0][0])
        tmp[0] = tmp[0][:, order]
        tmp[1] = tmp[1][order, :]

        iota = [i + 1 for i in range(n - 1)]
        for perm_part in itertools.permutations(iota):
            perm = [0] + list(perm_part)
            candidate = np.copy(tmp)
            candidate[0] = candidate[0][perm, :]
            candidate[1] = candidate[1][:, perm]
            if comp(candidate.flatten(), res.flatten()):
                res = candidate

    return res

def std(table):
    tmp1 = std_impl(table)

    table[0], table[1] = table[1], np.copy(table[0])
    tmp2 = std_impl(table)

    if comp(tmp1.flatten(), tmp2.flatten()):
        return tmp1
    else:
        return tmp2