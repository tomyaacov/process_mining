import pm4py
from pm4py.algo.evaluation.generalization import algorithm as generalization_evaluator
from pm4py.algo.evaluation.simplicity import algorithm as simplicity_evaluator
import pandas as pd
from itertools import product, permutations
from datetime import datetime
import random

num_of_folds = 5


def data_to_log(data):

    dataframe = pm4py.format_dataframe(df, case_id='case', activity_key='activity', timestamp_key='timestamp')
    return pm4py.convert_to_event_log(dataframe)


# data generatioln
l = [zip(w1, w2)
     for w1 in permutations('ABCD') if w1.index("A") < w1.index("B") and w1.index("C") < w1.index("D")
     for w2 in permutations('1234') if w2.index("1") < w2.index("2") and w2.index("3") < w2.index("4")]

data = [[x + y for (x, y) in z] for z in l]
random.shuffle(data)

df = pd.DataFrame(columns=['case', 'activity', 'timestamp'])
for i, case in enumerate(data):
    for activity in case:
        df = df.append({'case': int(i), 'activity': activity, 'timestamp': datetime.now()}, ignore_index=True)

partitions = {
    "letter": lambda x: x[0],
    "number": lambda x: x[1]
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
pm4py.save_vis_petri_net(net, initial_marking, final_marking, "output/ab14_model.png")

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
    pm4py.save_vis_petri_net(net, initial_marking, final_marking, "output/ab14_model_" + p_name + ".png")

print("out model results:")
print(results)

