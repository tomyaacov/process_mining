from aalpy.learning_algs.deterministic_passive.RPNI import run_RPNI
from rapidfuzz.distance.Levenshtein import distance
import random
import time

alphabet = ["A", "B", "C"]

data_positive = set()
with open("data/ABC.csv", 'r') as f:
    for line in f:
        if len(line.strip()) > 0:
            data_positive.add("".join(line.strip().split(",")))
        else:  # empty word
            data_positive.add("")

data_positive_size = len(data_positive)
data_negative = set()
data_negative_size = 0
trash = set()
threshold_distance = 2
distances = []
start = time.time()
while data_negative_size < data_positive_size:
    suggestion = random.choices(["A", "B", "C"], k=random.randint(0, 11))
    w = "".join(suggestion)
    if w in data_negative:
        continue
    if w in trash:
        continue
    if w in data_positive:
        continue
    min_distance = float('inf')
    for p in data_positive:
        d = distance(w, p)
        if d < min_distance:
            min_distance = d
        if min_distance <= threshold_distance:
            trash.add(w)
            distances.append((w, min_distance))
            print(w, min_distance)
            continue
    data_negative.add(w)
    data_negative_size += 1
    distances.append((w, min_distance))
    print(w, min_distance)
print(f"Runtime:  {time.time() - start}")


