import pm4py
import pandas as pd
from itertools import product, permutations
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


def data_to_log(data, k):
    df = pd.DataFrame(columns=['case', 'activity', 'timestamp'])
    for i, case in enumerate(data):
        if i % 1000 == k:
            for activity in case:
                df = df.append({'case': i, 'activity': activity, 'timestamp': datetime.now()}, ignore_index=True)
    # dataframe = pm4py.format_dataframe(df, case_id='case', activity_key='activity', timestamp_key='timestamp')
    return df


# ttt
data = []
with open("ttt_traces.csv", 'r') as f:
    for line in f:
        data.append(line.strip().split(","))
with ThreadPoolExecutor(1000) as executor:
    processes = [executor.submit(data_to_log, data, i) for i in range(1000)]
    results = [p.result() for p in processes]
dataframe = pd.concat(results)
dataframe.to_csv('ttt_log_df.csv', index=False)
