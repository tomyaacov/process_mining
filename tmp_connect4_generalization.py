import pm4py
from pm4py.algo.evaluation.generalization import algorithm as generalization_evaluator
from pm4py.algo.evaluation.simplicity import algorithm as simplicity_evaluator
from pm4py.algo.analysis.woflan import algorithm as woflan
import pandas as pd
from itertools import product, permutations
from project_utils import *
from data.connect4.transformations import partitions, events_map

df = pd.read_csv("data/connect4/connect4_log_50k.csv")

event_log = df_to_log(df)

results = {
#    "fitness_token_based_replay": [],
#    "fitness_alignments": [],
#    "precision_token_based_replay": [],
#    "precision_alignments": [],
    "places": [],
    "transitions": [],
    "arcs": []
}

# models_list = [
# "player",
# "column0",
# "column1",
# "column2",
# "column3",
# "column4",
# "column5",
# "column6"
# ]

pn_list = []
for p_name in partitions:
    net, initial_marking, final_marking = pm4py.read_pnml("connect4_models/connect4_model_" + p_name + ".pnml")
    results["places"].append(len(net.places))
    results["transitions"].append(len(net.transitions))
    results["arcs"].append(len(net.arcs))
    pn_list.append(net)
print("our model results:")
print(results)

net, initial_marking, final_marking = get_intersection_pn(pn_list)
generalization_evaluator_ = generalization_evaluator.apply(event_log, net, initial_marking, final_marking )
print("generalization_evaluator:", generalization_evaluator_)




