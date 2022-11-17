import pandas as pd
from datetime import datetime
import pm4py

data = [
    ["A", "B", "D"],
    ["A", "B", "C", "D"],
    ["A", "B", "C", "C", "D"],
    ["A", "B", "C", "C", "C", "D"],
    ["A", "B", "C", "C", "C", "C", "D"],
    ["A", "B", "C", "C", "C", "C", "C", "D"],
    ["A", "B", "C", "C", "C", "C", "C", "C", "D"],
]

df = pd.DataFrame(columns=['case', 'activity', 'timestamp'])
for i, case in enumerate(data):
    for activity in case:
        df = df.append({'case': i, 'activity': activity, 'timestamp': datetime.now()}, ignore_index=True)
dataframe = pm4py.format_dataframe(df, case_id='case', activity_key='activity', timestamp_key='timestamp')
event_log = pm4py.convert_to_event_log(dataframe)

net, initial_marking, final_marking = pm4py.discover_petri_net_alpha(event_log)
pm4py.save_vis_petri_net(net, initial_marking, final_marking, "output/alpha_model.png")

net, initial_marking, final_marking = pm4py.discover_petri_net_alpha_plus(event_log)
pm4py.save_vis_petri_net(net, initial_marking, final_marking, "output/alpha_plus_model.png")

net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(event_log)
pm4py.save_vis_petri_net(net, initial_marking, final_marking, "output/inductive_model.png")

net, initial_marking, final_marking = pm4py.discover_petri_net_heuristics(event_log, dependency_threshold=0.99)
pm4py.save_vis_petri_net(net, initial_marking, final_marking, "output/heuristic_model.png")
