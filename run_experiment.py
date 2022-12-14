import pm4py
from pm4py.algo.evaluation.generalization import algorithm as generalization_evaluator
from pm4py.algo.evaluation.simplicity import algorithm as simplicity_evaluator
from pm4py.algo.analysis.woflan import algorithm as woflan
import pandas as pd
from itertools import product, permutations
from project_utils import *
from data.connect4.transformations import partitions, events_map

df = pd.read_csv("data/connect4/connect4_log_50k.csv")

for k, v in partitions.items():
    if callable(v):
        df[k] = df['activity'].map(v)
    else:
        df[k] = df['activity'].map(lambda x: v[x])

def evaluate(event_log, net, initial_marking, final_marking):
    fitness_token_based_replay = pm4py.fitness_token_based_replay(event_log, net, initial_marking, final_marking)
    precision_token_based_replay = pm4py.precision_token_based_replay(event_log, net, initial_marking, final_marking)
    generalization_evaluator_ = generalization_evaluator.apply(event_log, net, initial_marking, final_marking)
    simplicity_evaluator_ = simplicity_evaluator.apply(net)
    print("general model results:")
    # is_sound = woflan.apply(net, initial_marking, final_marking, parameters={woflan.Parameters.RETURN_ASAP_WHEN_NOT_SOUND: True,
    #                                                                      woflan.Parameters.PRINT_DIAGNOSTICS: False,
    #                                                                      woflan.Parameters.RETURN_DIAGNOSTICS: False})
    # print("is_sound:", is_sound)
    print("fitness_token_based_replay:", fitness_token_based_replay)
    # print("fitness_alignments:", fitness_alignments)
    print("precision_token_based_replay:", precision_token_based_replay)
    # print("precision_alignments:", precision_alignments)
    print("generalization_evaluator:", generalization_evaluator_)
    print("simplicity_evaluator:", simplicity_evaluator_)
    print("places:", len(net.places))
    print("transitions:", len(net.transitions))
    print("arcs:", len(net.arcs))



event_log = df_to_log(df)
# net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(event_log)
# print("inductive:")
# evaluate(event_log, net, initial_marking, final_marking)
# try:
#     pm4py.write_pnml(net, initial_marking, final_marking, "output/connect4_model_inductive.pnml")
# except Exception as e:
#     print(e.args)
# net, initial_marking, final_marking = pm4py.discover_petri_net_alpha(event_log)
# print("alpha:")
# evaluate(event_log, net, initial_marking, final_marking)
# try:
#     pm4py.write_pnml(net, initial_marking, final_marking, "output/connect4_model_alpha.pnml")
# except Exception as e:
#     print(e.args)
# net, initial_marking, final_marking = pm4py.discover_petri_net_alpha_plus(event_log)
# print("alph plus:")
# evaluate(event_log, net, initial_marking, final_marking)
# try:
#     pm4py.write_pnml(net, initial_marking, final_marking, "output/connect4_model_alpha_plus.pnml")
# except Exception as e:
#     print(e.args)
# net, initial_marking, final_marking = pm4py.discover_petri_net_heuristics(event_log)
# print("heuristic:")
# evaluate(event_log, net, initial_marking, final_marking)
# try:
#     pm4py.write_pnml(net, initial_marking, final_marking, "output/connect4_model_heuristic.pnml")
# except Exception as e:
#     print(e.args)

results = {
#    "fitness_token_based_replay": [],
#    "fitness_alignments": [],
#    "precision_token_based_replay": [],
#    "precision_alignments": [],
#    "generalization_evaluator": [],
    "simplicity_evaluator": [],
    "places": [],
    "transitions": [],
    "arcs": []
}
pn_list = []

for p_name in partitions:
    dataframe = pm4py.format_dataframe(df, case_id='case', activity_key=p_name, timestamp_key='timestamp')
    event_log = pm4py.convert_to_event_log(dataframe)
    net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(event_log)
    net, initial_marking, final_marking = get_modified_pn(net, events_map[p_name])
    event_log = df_to_log(df)
    # results["fitness_token_based_replay"].append(pm4py.fitness_token_based_replay(event_log, net, initial_marking, final_marking ))
    # results["fitness_alignments"].append(pm4py.fitness_alignments(event_log, net, initial_marking, final_marking ))
    # results["precision_token_based_replay"].append(pm4py.precision_token_based_replay(event_log, net, initial_marking, final_marking ))
    # results["precision_alignments"].append(pm4py.precision_alignments(event_log, net, initial_marking, final_marking ))
    # results["generalization_evaluator"].append(generalization_evaluator.apply(event_log, net, initial_marking, final_marking ))
    results["simplicity_evaluator"].append(simplicity_evaluator.apply(net))
    results["places"].append(len(net.places))
    results["transitions"].append(len(net.transitions))
    results["arcs"].append(len(net.arcs))
    try:
        pm4py.write_pnml(net, initial_marking, final_marking, "output/connect4_model_" + p_name + ".pnml")
    except Exception as e:
        print(e.args)
    pn_list.append(net)

print("our model results:")
print(results)
df = df[df["case"]%50 == 0]
event_log = df_to_log(df)
net, initial_marking, final_marking = get_intersection_pn(pn_list)
try:
    pm4py.write_pnml(net, initial_marking, final_marking, "output/connect4_model_" + "intersected" + ".pnml")
except Exception as e:
    print(e.args)
fitness_token_based_replay = pm4py.fitness_token_based_replay(event_log, net, initial_marking, final_marking )
#fitness_alignments = pm4py.fitness_alignments(event_log, net, initial_marking, final_marking )
precision_token_based_replay = pm4py.precision_token_based_replay(event_log, net, initial_marking, final_marking )
#precision_alignments = pm4py.precision_alignments(event_log, net, initial_marking, final_marking )
generalization_evaluator_ = generalization_evaluator.apply(event_log, net, initial_marking, final_marking )
simplicity_evaluator_ = simplicity_evaluator.apply(net)

print("intersected model results:")
print("fitness_token_based_replay:", fitness_token_based_replay)
#print("fitness_alignments:", fitness_alignments)
print("precision_token_based_replay:", precision_token_based_replay)
#print("precision_alignments:", precision_alignments)
print("generalization_evaluator:", generalization_evaluator_)
print("simplicity_evaluator:", simplicity_evaluator_)
