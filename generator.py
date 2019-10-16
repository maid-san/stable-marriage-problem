import numpy as np
import itertools
import os

def create_instances_file(n):
    d = {key:chr(i + 65) for i, key in enumerate(itertools.permutations([i + 1 for i in range(n)]))}

    with open(f"size{n}_instances.txt", mode='w') as f:
        for instance in itertools.product(itertools.permutations([i + 1 for i in range(n)]), repeat=n*2 - 1):
            instance = np.insert(np.array(instance), 0, [i + 1 for i in range(n)])
            reshaped = instance.reshape(2, n, n)
            if is_std(reshaped):
                for i in reshaped:
                    for j in i:
                        f.write(d[tuple(j.tolist())])
                f.write("\n")

def lex_comp(lhs, rhs):
    idxes = np.where(lhs != rhs)[0]

    if len(idxes) == 0:
        return False
    if lhs[idxes[0]] < rhs[idxes[0]]:
        return True
    elif lhs[idxes[0]] > rhs[idxes[0]]:
        return False

def is_std_impl(table, reference):
    n = np.shape(table)[1]

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
            if lex_comp(candidate.flatten(), reference.flatten()):
                return False

    return True

def is_std(table):
    reference = table.reshape(-1,)

    if not is_std_impl(table, reference):
        return False

    copied = np.copy(table)
    copied[0], copied[1] = copied[1], np.copy(copied[0])
    return is_std_impl(copied, reference)

def create_table(alphabets):
    size = len(alphabets) / 2
    d = {chr(i + 65):data for i, data in enumerate(itertools.permutations([i + 1 for i in range(size)]))}

    ret = [[[0 for i in range(size)] for j in range(size)] for k in range(2)]
    for i in range(2):
        for j in range(size):
            ret[i][j] = list(d[alphabets[i*2 + j]])

    return ret

create_instances_file(3)