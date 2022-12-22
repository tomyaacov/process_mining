import pm4py
import pandas as pd
from itertools import product, permutations
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
CONCURRENCY = 100

def data_to_log(data, k):
    df = pd.DataFrame(columns=['case', 'activity', 'timestamp'])
    for i, case in enumerate(data):
        if i % CONCURRENCY == k:
            print(i)
            for activity in case:
                df = df.append({'case': i, 'activity': activity, 'timestamp': datetime.now()}, ignore_index=True)
    # dataframe = pm4py.format_dataframe(df, case_id='case', activity_key='activity', timestamp_key='timestamp')
    return df


# ttt
data = []
with open("data/connect4/connect4_traces_10k.csv", 'r') as f:
    for line in f:
        data.append(line.strip().split(","))
from time import time
ts = time()
with ThreadPoolExecutor(CONCURRENCY) as executor:
    processes = [executor.submit(data_to_log, data, i) for i in range(CONCURRENCY)]
    results = [p.result() for p in processes]
dataframe = pd.concat(results)
print(ts - time())
dataframe.to_csv('connect4_log_10k.csv', index=False)
# 10 - 578
# 100 - 449