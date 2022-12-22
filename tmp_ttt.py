import pm4py
from pm4py.algo.analysis.woflan import algorithm as woflan
from data.ad14.transformations import partitions, events_map
from project_utils import *

pn_list = []
for p_name in partitions:
    net, initial_marking, final_marking = pm4py.read_pnml("AD14_models/ad14_model_" + p_name + ".pnml")
    pn_list.append(net)
net, initial_marking, final_marking = get_intersection_pn(pn_list)
is_sound = woflan.apply(net, initial_marking, final_marking,
                        parameters={woflan.Parameters.RETURN_ASAP_WHEN_NOT_SOUND: True,
                                    woflan.Parameters.PRINT_DIAGNOSTICS: False,
                                    woflan.Parameters.RETURN_DIAGNOSTICS: False})
print("ad14 intersection")
print("is_sound:", is_sound)

from data.ttt.transformations import partitions, events_map

pn_list = []
for p_name in partitions:
    net, initial_marking, final_marking = pm4py.read_pnml("ttt_models/ttt_model_" + p_name + ".pnml")
    pn_list.append(net)
net, initial_marking, final_marking = get_intersection_pn(pn_list)
is_sound = woflan.apply(net, initial_marking, final_marking,
                        parameters={woflan.Parameters.RETURN_ASAP_WHEN_NOT_SOUND: True,
                                    woflan.Parameters.PRINT_DIAGNOSTICS: False,
                                    woflan.Parameters.RETURN_DIAGNOSTICS: False})
print("ttt intersection")
print("is_sound:", is_sound)




