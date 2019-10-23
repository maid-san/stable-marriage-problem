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
