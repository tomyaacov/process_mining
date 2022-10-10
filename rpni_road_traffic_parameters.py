from aalpy.learning_algs.deterministic_passive.RPNI import run_RPNI
from rapidfuzz.distance.Levenshtein import distance
import random
import time

alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]

positive_list = []
with open("data/Road_Traffic_Processed.csv", 'r') as f:
    for line in f:
        if len(line.strip()) > 0:
            positive_list.append("".join(line.strip().split(",")))
        else:  # empty word
            positive_list.append("")

import pandas as pd
df = pd.DataFrame({'transition_completion': [],
                   'desired_negative_size': [],
                   'threshold_distance': [],
                   'accuracy': []})

for transition_completion in ['self_loop' or 'sink_state']:
    for desired_negative_size in [500, 1000, 1500]:
        for threshold_distance in [1,2,3,4,5]:

            positive_size = len(positive_list)
            positive_set = set(positive_list)
            negative_set = set()
            data_negative_size = 0
            trash = set()
            distances = []
            start = time.time()
            while data_negative_size < desired_negative_size:
                suggestion = random.choices(alphabet, k=random.randint(0, 11))
                w = "".join(suggestion)
                if w in negative_set:
                    continue
                if w in trash:
                    continue
                if w in positive_set:
                    continue
                min_distance = float('inf')
                for p in positive_set:
                    d = distance(w, p)
                    if d < min_distance:
                        min_distance = d
                    if min_distance <= threshold_distance:
                        trash.add(w)
                        distances.append((w, min_distance))
                        print(w, min_distance)
                        break
                if min_distance > threshold_distance:
                    negative_set.add(w)
                    data_negative_size += 1
                    distances.append((w, min_distance))
                    print(w, min_distance)

            data = []
            for x in positive_list:
                data.append((tuple(x), True))
            for x in negative_set:
                data.append((tuple(x), False))
            random.shuffle(data)

            k = 3
            acc_all = 0
            for i in range(k):
                test = [x for idx, x in enumerate(data) if idx % k == i]
                train = list(set([x for idx, x in enumerate(data) if idx % k != i]))
                model = run_RPNI(train, automaton_type='dfa')
                model.make_input_complete(transition_completion)
                for seq, l in test:
                    if len(seq) > 0:
                        out = model.execute_sequence(model.initial_state, seq)[-1]
                    else:
                        out = model.initial_state.is_accepting
                    if out == l and l:
                        acc_all += 1

            print("accuracy test all:", acc_all/len(positive_list))
            df.loc[len(df.index)] = [transition_completion, desired_negative_size, threshold_distance, acc_all/len(positive_list)]

df.to_csv("results.csv")
