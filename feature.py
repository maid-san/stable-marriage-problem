import numpy as np

def calc_latin_feature (table):
    n = np.shape(table)[1]

    res = 0
    number = 0
    for i in range(n):
        for j in range(n):
            a = table[0][i][j]
            b = table[1][i][j]

            if np.isnan(a) or np.isnan(b):
                continue

            res += np.abs((a + b) - (n + 1))
            number += 1

    return res / number