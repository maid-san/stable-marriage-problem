import numpy as np

def calc_latin_feature (table):
    n = np.shape(table)[1]

    res = 0
    for i in range(n):
        for j in range(n):
            f = lambda x: n if np.isnan(x) else x

            a = f(table[0][i][j])
            b = f(table[1][i][j])

            res += np.abs((a + b) - (n + 1))

    return res