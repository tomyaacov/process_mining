import pm4py

log = pm4py.read_xes("data/Road_Traffic_Fine_Management_Process.xes")
net, initial_marking, final_marking = pm4py.discover_petri_net_alpha(log)
pm4py.view_petri_net(net, initial_marking, final_marking)
