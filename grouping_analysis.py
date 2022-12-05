from itertools import product, permutations
import pandas as pd
import pm4py
from datetime import datetime

# data generatioln
l = [zip(w1,w2)
for w1 in permutations('ABCD') if w1.index("A") < w1.index("B") and w1.index("C") < w1.index("D")
for w2 in permutations('1234') if w2.index("1") < w2.index("2") and w2.index("3") < w2.index("4")  ]

data = [[x+y for (x,y) in z] for z in l ]

def data_to_log(data):
    df = pd.DataFrame(columns=['case', 'activity', 'timestamp'])
    for i, case in enumerate(data):
        for activity in case:
            df = df.append({'case': i, 'activity': activity, 'timestamp': datetime.now()}, ignore_index=True)
    dataframe = pm4py.format_dataframe(df, case_id='case', activity_key='activity', timestamp_key='timestamp')
    return pm4py.convert_to_event_log(dataframe)


results = pd.DataFrame(columns=["group",
                                "places",
                                "transitions",
                                "arcs", ])
original_events = ['A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B4', 'C1', 'C2', 'C3', 'C4', 'D1', 'D2', 'D3', 'D4']
groupings = set()
for group in product(range(4), repeat=len(original_events)):
    events = []
    for i in range(4):
        events.append(",".join([x for j, x in zip(group, original_events) if j == i]))
    events = tuple(sorted(events))
    if events in groupings:
        continue
    groupings.add(events)
    event_mapper = {}
    for new_event in events:
        for e in new_event.split(","):
            event_mapper[e] = new_event
    converted_data = [[event_mapper[e] for e in w] for w in data]
    event_log = data_to_log(converted_data)
    net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(event_log)
    # pm4py.view_petri_net(net, initial_marking, final_marking)
    results = results.append({"group": events,
                              "places": len(net.places),
                              "transitions": len(net.transitions),
                              "arcs": len(net.arcs)},
                             ignore_index=True)
results.to_csv("results.csv", index=False)
