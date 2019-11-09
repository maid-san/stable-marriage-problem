from preferences import preferences
from feature import *
from graph import GraphSolver

def output_rotation_exchange(list):
    for i in list:
        preference  = preferences[i]
        gs = GraphSolver(preference)
        print(f"P(4,{i})")
        gs.output_graph(preference)
        print()
        matchings, _ = gs.how_many_stable_matching(output=True)
        print(f"Matching: {matchings}")

def output_csv_file():
    print("Instance,Matchings,Nodes,Latin1,Latin2,Latin3,Similar Relations")
    for i in range(len(preferences)):
        preference  = preferences[i]
        gs = GraphSolver(preference)

        if not gs.is_decomposed(gs.create_graph(preference)):
            matchings, _ = gs.how_many_stable_matching()
            nodes    = count_nodes(preference)
            latin1   = calc_latin_feature(preference)
            latin2   = calc_latin_feature_2(preference)
            latin3   = calc_latin_feature_3(preference)
            sr, _    = find_similar_relation(preference, 1, 1)

            print(f"{i},{matchings},{nodes},{latin1},{latin2},{latin3},{sr}")