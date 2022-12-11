import pm4py
from pm4py.algo.evaluation.generalization import algorithm as generalization_evaluator
from pm4py.algo.evaluation.simplicity import algorithm as simplicity_evaluator
import pandas as pd
from itertools import product, permutations
from datetime import datetime
import random

df = pd.read_csv("ttt_log_df.csv")
df = df.iloc[:10_000, :]
partitions = {
    "player": lambda x: x[0],
    "cell0": lambda x: x[1] if x[1] == str(0) else "-",
    "cell1": lambda x: x[1] if x[1] == str(1) else "-",
    "cell2": lambda x: x[1] if x[1] == str(2) else "-",
    "cell3": lambda x: x[1] if x[1] == str(3) else "-",
    "cell4": lambda x: x[1] if x[1] == str(4) else "-",
    "cell5": lambda x: x[1] if x[1] == str(5) else "-",
    "cell6": lambda x: x[1] if x[1] == str(6) else "-",
    "cell7": lambda x: x[1] if x[1] == str(7) else "-",
    "cell8": lambda x: x[1] if x[1] == str(8) else "-",
    "row-O0,O1,O2": lambda x: "O0,O1,O2" if x in ['O0', 'O1', 'O2'] else "-",
    "row-X0,X1,X2": lambda x: "X0,X1,X2" if x in ['X0', 'X1', 'X2'] else "-",
    "row-O3,O4,O5": lambda x: "O3,O4,O5" if x in ['O3', 'O4', 'O5'] else "-",
    "row-X3,X4,X5": lambda x: "X3,X4,X5" if x in ['X3', 'X4', 'X5'] else "-",
    "row-O6,O7,O8": lambda x: "O6,O7,O8" if x in ['O6', 'O7', 'O8'] else "-",
    "row-X6,X7,X8": lambda x: "X6,X7,X8" if x in ['X6', 'X7', 'X8'] else "-",
    "row-O0,O3,O6": lambda x: "O0,O3,O6" if x in ['O0', 'O3', 'O6'] else "-",
    "row-X0,X3,X6": lambda x: "X0,X3,X6" if x in ['X0', 'X3', 'X6'] else "-",
    "row-O1,O4,O7": lambda x: "O1,O4,O7" if x in ['O1', 'O4', 'O7'] else "-",
    "row-X1,X4,X7": lambda x: "X1,X4,X7" if x in ['X1', 'X4', 'X7'] else "-",
    "row-O2,O5,O8": lambda x: "O2,O5,O8" if x in ['O2', 'O5', 'O8'] else "-",
    "row-X2,X5,X8": lambda x: "X2,X5,X8" if x in ['X2', 'X5', 'X8'] else "-",
    "row-O0,O4,O8": lambda x: "X0,O4,O8" if x in ['O0', 'O4', 'O8'] else "-",
    "row-X0,X4,X8": lambda x: "X0,X4,X8" if x in ['X0', 'X4', 'X8'] else "-",
    "row-O2,O4,O6": lambda x: "O2,O4,O6" if x in ['O2', 'O4', 'O6'] else "-",
    "row-X2,X4,X6": lambda x: "X2,X4,X6" if x in ['X2', 'X4', 'X6'] else "-"
}

for k, v in partitions.items():
    df[k] = df['activity'].map(v)

dataframe = pm4py.format_dataframe(df, case_id='case', activity_key='activity', timestamp_key='timestamp')
event_log = pm4py.convert_to_event_log(dataframe)
net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(event_log)
fitness_token_based_replay = pm4py.fitness_token_based_replay(event_log, net, initial_marking, final_marking )['average_trace_fitness']
fitness_alignments = pm4py.fitness_alignments(event_log, net, initial_marking, final_marking )['average_trace_fitness']
precision_token_based_replay = pm4py.precision_token_based_replay(event_log, net, initial_marking, final_marking )
precision_alignments = pm4py.precision_alignments(event_log, net, initial_marking, final_marking )
generalization_evaluator_ = generalization_evaluator.apply(event_log, net, initial_marking, final_marking )
simplicity_evaluator_ = simplicity_evaluator.apply(net)
pm4py.write_pnml(net, initial_marking, final_marking, "output/ttt_model.pnml")

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
for p_name in partitions:
    dataframe = pm4py.format_dataframe(df, case_id='case', activity_key=p_name, timestamp_key='timestamp')
    event_log = pm4py.convert_to_event_log(dataframe)
    net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(event_log)
    results["fitness_token_based_replay"].append(pm4py.fitness_token_based_replay(event_log, net, initial_marking, final_marking )['average_trace_fitness'])
    results["fitness_alignments"].append(pm4py.fitness_alignments(event_log, net, initial_marking, final_marking )['average_trace_fitness'])
    results["precision_token_based_replay"].append(pm4py.precision_token_based_replay(event_log, net, initial_marking, final_marking ))
    results["precision_alignments"].append(pm4py.precision_alignments(event_log, net, initial_marking, final_marking ))
    results["generalization_evaluator"].append(generalization_evaluator.apply(event_log, net, initial_marking, final_marking ))
    results["simplicity_evaluator"].append(simplicity_evaluator.apply(net))
    pm4py.write_pnml(net, initial_marking, final_marking, "output/ttt_model_" + p_name + ".pnml")

print("out model results:")
print(results)

