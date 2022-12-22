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
    df[k] = df['activity'].map(v)

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
net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(event_log)
print("inductive:")
evaluate(event_log, net, initial_marking, final_marking)
try:
    pm4py.write_pnml(net, initial_marking, final_marking, "output/connect4_model_inductive.pnml")
except Exception as e:
    print(e.args)