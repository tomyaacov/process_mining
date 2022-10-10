from pm4py.objects.conversion.log import converter as xes_converter
from pm4py.objects.log.importer.xes import importer as xes_importer

file_name = 'data/Road_Traffic_Fine_Management_Process.xes'

log = xes_importer.apply(file_name)
pd = xes_converter.apply(log, variant=xes_converter.Variants.TO_DATA_FRAME)

print(pd[['case:concept:name', 'concept:name', 'time:timestamp']].head(10))

pd.to_csv(file_name.replace(".xes", ".csv"), index=False)

df = pd[['case:concept:name', 'concept:name', 'time:timestamp']]

df = df.sort_values(by=['case:concept:name', 'time:timestamp'])

map = {'Add penalty': 'A',
       'Appeal to Judge': 'B',
       'Create Fine': 'C',
       'Insert Date Appeal to Prefecture': 'D',
       'Insert Fine Notification': 'E',
       'Notify Result Appeal to Offender': 'F',
       'Payment': 'G',
       'Receive Result Appeal from Prefecture': 'H',
       'Send Appeal to Prefecture': 'I',
       'Send Fine': 'J',
       'Send for Credit Collection': 'K'}

df['event'] = df['concept:name'].map(map)

data = {}
for index, row in df.iterrows():
    if row['case:concept:name'] in data:
        data[row['case:concept:name']].append(row['event'])
    else:
        data[row['case:concept:name']] = [row['event']]

data = list(data.values())
import csv

with open("data/Road_Traffic_Processed.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(data)
