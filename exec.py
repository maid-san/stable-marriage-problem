from preferences import preferences
from feature import *
from graph import GraphSolver

# for i in [255,291]:
#     preference  = preferences[i]
#     gs = GraphSolver(preference)
#     print(f"P(4,{i})")
#     gs.output_graph(preference)
#     print()
#     matchings, _ = gs.how_many_stable_matching()
#     print(f"Matching: {matchings}")

print("Instance,Matchings,Nodes,First Rotation,Latin1,Latin2,Latin3,cyclic,cyclic2,")
for i in range(len(preferences)):
    preference  = preferences[i]
    gs = GraphSolver(preference)

    if not gs.is_decomposed(gs.create_graph(preference)):
        matchings, _ = gs.how_many_stable_matching()
        nodes    = count_nodes(preference)
        first_rotation = count_first_rotation(preference)
        latin1   = calc_latin_feature(preference)
        latin2   = calc_latin_feature_2(preference)
        latin3   = calc_latin_feature_3(preference)
        cyclic   = calc_cyclic_feature(preference[1])
        cyclic2  = calc_cyclic_feature_2(preference[1])

        print(f"{i},{matchings},{nodes},{first_rotation},{latin1},{latin2},{latin3},{cyclic},{cyclic2},")