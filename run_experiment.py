import pm4py
from pm4py.algo.evaluation.generalization import algorithm as generalization_evaluator
from pm4py.algo.evaluation.simplicity import algorithm as simplicity_evaluator
import pandas as pd
from itertools import product, permutations
from project_utils import *
from data.ttt.transformations import partitions, events_map

df = pd.read_csv("data/ttt/ttt_log.csv")

for k, v in partitions.items():
    df[k] = df['activity'].map(v)

event_log = df_to_log(df)
net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(event_log)
fitness_token_based_replay = pm4py.fitness_token_based_replay(event_log, net, initial_marking, final_marking )
fitness_alignments = pm4py.fitness_alignments(event_log, net, initial_marking, final_marking )
precision_token_based_replay = pm4py.precision_token_based_replay(event_log, net, initial_marking, final_marking )
precision_alignments = pm4py.precision_alignments(event_log, net, initial_marking, final_marking )
generalization_evaluator_ = generalization_evaluator.apply(event_log, net, initial_marking, final_marking )
simplicity_evaluator_ = simplicity_evaluator.apply(net)
try:
    pm4py.write_pnml(net, initial_marking, final_marking, "output/ad14_model.pnml")
except Exception as e:
    print(e.args)

print("general model results:")
print("fitness_token_based_replay:", fitness_token_based_replay)
print("fitness_alignments:", fitness_alignments)
print("precision_token_based_replay:", precision_token_based_replay)
print("precision_alignments:", precision_alignments)
print("generalization_evaluator:", generalization_evaluator_)
print("simplicity_evaluator:", simplicity_evaluator_)

results = {
    "fitness_token_based_replay": [],
    "fitness_alignments": [],
    "precision_token_based_replay": [],
    "precision_alignments": [],
    "generalization_evaluator": [],
    "simplicity_evaluator": [],
}
pn_list = []

for p_name in partitions:
    dataframe = pm4py.format_dataframe(df, case_id='case', activity_key=p_name, timestamp_key='timestamp')
    event_log = pm4py.convert_to_event_log(dataframe)
    net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(event_log)
    net, initial_marking, final_marking = get_modified_pn(net, events_map[p_name])
    event_log = df_to_log(df)
    results["fitness_token_based_replay"].append(pm4py.fitness_token_based_replay(event_log, net, initial_marking, final_marking ))
    results["fitness_alignments"].append(pm4py.fitness_alignments(event_log, net, initial_marking, final_marking ))
    results["precision_token_based_replay"].append(pm4py.precision_token_based_replay(event_log, net, initial_marking, final_marking ))
    results["precision_alignments"].append(pm4py.precision_alignments(event_log, net, initial_marking, final_marking ))
    results["generalization_evaluator"].append(generalization_evaluator.apply(event_log, net, initial_marking, final_marking ))
    results["simplicity_evaluator"].append(simplicity_evaluator.apply(net))
    try:
        pm4py.write_pnml(net, initial_marking, final_marking, "output/ad14_model_" + p_name + ".pnml")
    except Exception as e:
        print(e.args)
    pn_list.append(net)

print("our model results:")
print(results)
net, initial_marking, final_marking = get_intersection_pn(pn_list)
fitness_token_based_replay = pm4py.fitness_token_based_replay(event_log, net, initial_marking, final_marking )
fitness_alignments = pm4py.fitness_alignments(event_log, net, initial_marking, final_marking )
precision_token_based_replay = pm4py.precision_token_based_replay(event_log, net, initial_marking, final_marking )
precision_alignments = pm4py.precision_alignments(event_log, net, initial_marking, final_marking )
generalization_evaluator_ = generalization_evaluator.apply(event_log, net, initial_marking, final_marking )
simplicity_evaluator_ = simplicity_evaluator.apply(net)

print("intersected model results:")
print("fitness_token_based_replay:", fitness_token_based_replay)
print("fitness_alignments:", fitness_alignments)
print("precision_token_based_replay:", precision_token_based_replay)
print("precision_alignments:", precision_alignments)
print("generalization_evaluator:", generalization_evaluator_)
print("simplicity_evaluator:", simplicity_evaluator_)