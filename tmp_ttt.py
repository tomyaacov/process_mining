import pm4py
from pm4py.algo.evaluation.generalization import algorithm as generalization_evaluator
from pm4py.algo.evaluation.simplicity import algorithm as simplicity_evaluator
import pandas as pd
from itertools import product, permutations
from project_utils import *
from data.ttt.transformations import partitions, events_map
from concurrent.futures import ThreadPoolExecutor

df = pd.read_csv("data/ttt/ttt_log.csv")

for k, v in partitions.items():
    df[k] = df['activity'].map(v)

net, initial_marking, final_marking = pm4py.read_pnml("ttt_models_2/ttt_model_intersection.pnml")
event_log = df_to_log(df)

def run_and_print(f, *args):
    output = f(*args)
    return f.__name__ + " : " + str(output)

with ThreadPoolExecutor(1000) as executor:
    processes = []
    processes.append(executor.submit(run_and_print, pm4py.fitness_token_based_replay, event_log, net, initial_marking, final_marking))
    processes.append(executor.submit(run_and_print, pm4py.precision_token_based_replay, event_log, net, initial_marking, final_marking))
    processes.append(executor.submit(run_and_print, generalization_evaluator.apply, event_log, net, initial_marking, final_marking))
    results = [p.result() for p in processes]

print(results)


