import numpy as np

def add_couple(couples, male_propose, proposing, proposed):
    if male_propose == True:
        couple = np.array([proposed,  proposing])
    else:
        couple = np.array([proposing, proposed])
    return np.vstack((couples, couple))

def get_proposed(table, proposing, rank, X):
    tmp = np.where(table[X][proposing] == rank)[0]
    if tmp.size == 0:
        return None
    else:
        return tmp[0]

def get_candidate(couples, proposed, Y):
    tmp = np.where(couples[:, Y] == proposed)[0]
    if tmp.size == 0:
        return None
    else:
        return tmp[0]

def gale_shapley(table, male_propose=True):
    if male_propose == True:
        X = 1
        Y = 0
    else:
        X = 0
        Y = 1

    tmp = np.copy(table)
    couples = np.empty((0, 2), int)
    singles = [i for i in range(np.shape(table)[1])]

    while singles:
        proposing = singles.pop()

        rank = 0
        while True:
            proposed = get_proposed(tmp, proposing, rank, X)
            if proposed is None:
                rank += 1
                continue
            tmp[X][proposing][proposed] = -1

            candidate = get_candidate(couples, proposed, Y)
            if candidate is None:
                couples = add_couple(couples, male_propose, proposing, proposed)
                break
            else:
                rank_proposing = tmp[Y][proposed][proposing]
                rank_candidate = tmp[Y][proposed][candidate]

                if rank_proposing < rank_candidate:
                    couples = np.delete(couples, np.where(couples[:, Y] == proposed)[0][0], 0)
                    couples = add_couple(couples, male_propose, proposing, proposed)
                    singles.append(candidate)
                    break
                else:
                    rank += 1

    return couples