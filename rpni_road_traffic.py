from aalpy.learning_algs.deterministic_passive.RPNI import run_RPNI
from aalpy.utils import save_automaton_to_file
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


transition_completion = 'self_loop'
desired_negative_size = 500
threshold_distance = 2
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

def simplify_graph(file):
    import pydot
    graphs = pydot.graph_from_dot_file(file)
    graph = graphs[0]
    graph.del_node('"\\n"')
    node_names = [x.get_name() for x in graph.get_nodes()]
    for src in node_names:
        for des in node_names:
            edges = graph.get_edge(src, des)
            if len(edges) > 1:
                new_label = '"' + ",".join([x.get_label() for x in edges]) + '"'
                graph.del_edge(src, des)
                graph.add_edge(pydot.Edge(src, des, label=new_label))
    graph.write_raw(file)

model = run_RPNI(list(set(data)), automaton_type='dfa')
save_automaton_to_file(model, path="output/model")
simplify_graph("output/model.dot")
