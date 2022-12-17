import pm4py
from pm4py.algo.simulation.playout.petri_net import algorithm as simulator
from pm4py.objects.petri_net.obj import PetriNet, Marking
from pm4py.objects.petri_net.utils import petri_utils
import pandas as pd
from datetime import datetime

def get_modified_pn(net, events_map):
    transition_map = {
    }
    places_map = {
    }
    mod_net = PetriNet("new_petri_net")
    for p in net.places:
        places_map[p.name] = PetriNet.Place(p.name)
        mod_net.places.add(places_map[p.name])
    for t in net.transitions:
        if t.label in events_map:
            transition_map[t.label] = []
            for t_ext in events_map[t.label]:
                new_t = PetriNet.Transition(t_ext, t_ext)
                mod_net.transitions.add(new_t)
                transition_map[t.label].append(new_t)
        else:
            transition_map[t.name] = PetriNet.Transition(t.name, None)
            mod_net.transitions.add(transition_map[t.name])
    for a in net.arcs:
        if isinstance(a.source, PetriNet.Transition):
            if a.source.label in events_map:
                for t_ext in transition_map[a.source.label]:
                    petri_utils.add_arc_from_to(t_ext, places_map[a.target.name], mod_net)
            else:
                petri_utils.add_arc_from_to(transition_map[a.source.name], places_map[a.target.name], mod_net)
        else:
            if a.target.label in events_map:
                for t_ext in transition_map[a.target.label]:
                    petri_utils.add_arc_from_to(places_map[a.source.name], t_ext, mod_net)
            else:
                petri_utils.add_arc_from_to(places_map[a.source.name], transition_map[a.target.name], mod_net)
    initial_marking = Marking()
    initial_marking[places_map["source"]] = 1
    final_marking = Marking()
    final_marking[places_map["sink"]] = 1
    return mod_net, initial_marking, final_marking

def get_intersection_pn(pn_list):
    transition_map = {
    }
    places_map = {
    }
    intersection_net = PetriNet("intersection_pn")
    places_map["source"] = PetriNet.Place("source")
    intersection_net.places.add(places_map["source"])
    places_map["sink"] = PetriNet.Place("sink")
    intersection_net.places.add(places_map["sink"])
    transition_map["from_source"] = PetriNet.Transition("from_source", None)
    intersection_net.transitions.add(transition_map["from_source"])
    transition_map["to_sink"] = PetriNet.Transition("to_sink", None)
    intersection_net.transitions.add(transition_map["to_sink"])
    petri_utils.add_arc_from_to(places_map["source"], transition_map["from_source"], intersection_net)
    petri_utils.add_arc_from_to(transition_map["to_sink"], places_map["sink"], intersection_net)
    for i, net in enumerate(pn_list):
        for p in net.places:
            new_name = str(i) + "_" + p.name
            places_map[new_name] = PetriNet.Place(new_name)
            intersection_net.places.add(places_map[new_name])
        for t in net.transitions:
            if t.label is None: # helper transition
                new_name = str(i) + "_" + t.name
                transition_map[new_name] = PetriNet.Transition(new_name, None)
                intersection_net.transitions.add(transition_map[new_name])
            else:
                if t.label not in transition_map:
                    transition_map[t.label] = PetriNet.Transition(t.name, t.label)
                    intersection_net.transitions.add(transition_map[t.name])
        for a in net.arcs:
            if isinstance(a.source, PetriNet.Transition):
                if a.source.label is None:  # helper transition
                    petri_utils.add_arc_from_to(transition_map[str(i) + "_" + a.source.name],
                                                places_map[str(i) + "_" + a.target.name],
                                                intersection_net)
                else:
                    petri_utils.add_arc_from_to(transition_map[a.source.name],
                                                places_map[str(i) + "_" + a.target.name],
                                                intersection_net)
            else:
                if a.target.label is None:  # helper transition
                    petri_utils.add_arc_from_to(places_map[str(i) + "_" + a.source.name],
                                                transition_map[str(i) + "_" + a.target.name],
                                                intersection_net)
                else:
                    petri_utils.add_arc_from_to(places_map[str(i) + "_" + a.source.name],
                                                transition_map[a.target.name],
                                                intersection_net)
        petri_utils.add_arc_from_to(transition_map["from_source"], places_map[str(i) + "_" + "source"], intersection_net)
        petri_utils.add_arc_from_to(places_map[str(i) + "_" + "sink"], transition_map["to_sink"], intersection_net)

    initial_marking = Marking()
    initial_marking[places_map["source"]] = 1
    final_marking = Marking()
    final_marking[places_map["sink"]] = 1
    return intersection_net, initial_marking, final_marking

def set_from_log(log):
    log_set = set()
    for trace in log:
        formatted_trace = tuple()
        for e in trace:
            formatted_trace += (e["concept:name"],)
        log_set.add(formatted_trace)
    return log_set

def list_to_df(data):
    df = pd.DataFrame(columns=['case', 'activity', 'timestamp'])
    for i, case in enumerate(data):
        for activity in case:
            df = df.append({'case': i, 'activity': activity, 'timestamp': datetime.now()}, ignore_index=True)
    return df

def df_to_log(df):
    dataframe = pm4py.format_dataframe(df, case_id='case', activity_key='activity', timestamp_key='timestamp')
    return pm4py.convert_to_event_log(dataframe)

def data_to_log(data):
    return df_to_log(list_to_df(data))


events_map = {
"AD14_models/AD14_model_letter.pnml":{
    "A": ["A"+str(x) for x in range(1,5)],
    "B": ["B"+str(x) for x in range(1,5)],
    "C": ["C"+str(x) for x in range(1,5)],
    "D": ["D"+str(x) for x in range(1,5)],
},
"AD14_models/AD14_model_number.pnml":{
    "1": [str(x)+"1" for x in "ABCD"],
    "2": [str(x)+"2" for x in "ABCD"],
    "3": [str(x)+"3" for x in "ABCD"],
    "4": [str(x)+"4" for x in "ABCD"],
},
}
# net1, initial_marking1, final_marking1 = pm4py.read_pnml("AD14_models/AD14_model_letter.pnml")
# net2, initial_marking2, final_marking2 = pm4py.read_pnml("AD14_models/AD14_model_number.pnml")
#
# net1, initial_marking1, final_marking1 = get_modified_pn(net1, events_map["AD14_models/AD14_model_letter.pnml"])
# net2, initial_marking2, final_marking2 = get_modified_pn(net2, events_map["AD14_models/AD14_model_number.pnml"])
#
# intersection_net, initial_marking, final_marking = get_intersection_pn([net1, net2])
#
# pm4py.view_petri_net(net1, initial_marking1, final_marking1)
# pm4py.view_petri_net(net2, initial_marking2, final_marking2)
# pm4py.view_petri_net(intersection_net, initial_marking, final_marking)
#
#
# simulated_log = simulator.apply(net1, initial_marking1, variant=simulator.Variants.EXTENSIVE,
#                                 parameters={simulator.Variants.EXTENSIVE.value.Parameters.MAX_TRACE_LENGTH: 4})
# a = set_from_log(simulated_log)
#
# simulated_log = simulator.apply(net2, initial_marking2, variant=simulator.Variants.EXTENSIVE,
#                                 parameters={simulator.Variants.EXTENSIVE.value.Parameters.MAX_TRACE_LENGTH: 4})
# b = set_from_log(simulated_log)
#
# simulated_log = simulator.apply(intersection_net, initial_marking, variant=simulator.Variants.EXTENSIVE,
#                                 parameters={simulator.Variants.EXTENSIVE.value.Parameters.MAX_TRACE_LENGTH: 4})
# c = set_from_log(simulated_log)
#
# print(a.intersection(b))
# print(c)

