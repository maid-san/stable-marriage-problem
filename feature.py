import numpy as np

def calc_feature(pref):
    return np.linalg.det(np.array(pref[0])), np.linalg.det(np.array(pref[1]))