import os
import pm4py
from pm4py.algo.simulation.playout.petri_net import algorithm as simulator
from pm4py.objects.petri_net.obj import PetriNet, Marking
from pm4py.objects.petri_net.utils import petri_utils

MAX_TRACE_LENGTH = 9
NO_TRACES = 1_000_000

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

def set_from_log(log):
    log_set = set()
    for trace in simulated_log:
        formatted_trace = tuple()
        for e in trace:
            formatted_trace += (e["concept:name"],)
        log_set.add(formatted_trace)
    return log_set

events_map = {
"ttt_models/ttt_model_player.pnml":{
    "X": ["X"+str(x) for x in range(9)],
    "O": ["O" + str(x) for x in range(9)]
},
"ttt_models/ttt_model_cell0.pnml":{
    "0": ["X0", "O0"],
    "-": ["X"+str(x) for x in range(9) if x!=0] + ["O" + str(x) for x in range(9) if x!=0]
},
"ttt_models/ttt_model_cell1.pnml":{
    "1": ["X1", "O1"],
    "-": ["X"+str(x) for x in range(9) if x!=1] + ["O" + str(x) for x in range(9) if x!=1]
},
"ttt_models/ttt_model_cell2.pnml":{
    "2": ["X2", "O2"],
    "-": ["X"+str(x) for x in range(9) if x!=2] + ["O" + str(x) for x in range(9) if x!=2]
},
"ttt_models/ttt_model_cell3.pnml":{
    "3": ["X3", "O3"],
    "-": ["X"+str(x) for x in range(9) if x!=3] + ["O" + str(x) for x in range(9) if x!=3]
},
"ttt_models/ttt_model_cell4.pnml":{
    "4": ["X4", "O4"],
    "-": ["X"+str(x) for x in range(9) if x!=4] + ["O" + str(x) for x in range(9) if x!=4]
},
"ttt_models/ttt_model_cell5.pnml":{
    "5": ["X5", "O5"],
    "-": ["X"+str(x) for x in range(9) if x!=5] + ["O" + str(x) for x in range(9) if x!=5]
},
"ttt_models/ttt_model_cell6.pnml":{
    "6": ["X6", "O6"],
    "-": ["X"+str(x) for x in range(9) if x!=6] + ["O" + str(x) for x in range(9) if x!=6]
},
"ttt_models/ttt_model_cell7.pnml":{
    "7": ["X7", "O7"],
    "-": ["X"+str(x) for x in range(9) if x!=7] + ["O" + str(x) for x in range(9) if x!=7]
},
"ttt_models/ttt_model_cell8.pnml":{
    "8": ["X8", "O8"],
    "-": ["X"+str(x) for x in range(9) if x!=8] + ["O" + str(x) for x in range(9) if x!=8]
},
"ttt_models/ttt_model_row-O0,O1,O2.pnml":{
    "O0,O1,O2": ['O0', 'O1', 'O2'],
    "-": ["X"+str(x) for x in range(9)] + ["O" + str(x) for x in range(9) if x not in [0,1,2]]
},
"ttt_models/ttt_model_row-X0,X1,X2.pnml":{
    "X0,X1,X2": ['X0', 'X1', 'X2'],
    "-": ["X"+str(x) for x in range(9) if x not in [0,1,2]] + ["O" + str(x) for x in range(9)]
},
"ttt_models/ttt_model_row-O3,O4,O5.pnml":{
    "O3,O4,O5": ['O3', 'O4', 'O5'],
    "-": ["X"+str(x) for x in range(9)] + ["O" + str(x) for x in range(9) if x not in [3,4,5]]
},
"ttt_models/ttt_model_row-X3,X4,X5.pnml":{
    "X3,X4,X5": ['X3', 'X4', 'X5'],
    "-": ["X"+str(x) for x in range(9) if x not in [3,4,5]] + ["O" + str(x) for x in range(9)]
},
"ttt_models/ttt_model_row-O6,O7,O8.pnml":{
    "O6,O7,O8": ['O6', 'O7', 'O8'],
    "-": ["X"+str(x) for x in range(9)] + ["O" + str(x) for x in range(9) if x not in [6,7,8]]
},
"ttt_models/ttt_model_row-X6,X7,X8.pnml":{
    "X6,X7,X8": ['X6', 'X7', 'X8'],
    "-": ["X"+str(x) for x in range(9) if x not in [6,7,8]] + ["O" + str(x) for x in range(9)]
},
"ttt_models/ttt_model_row-O0,O3,O6.pnml":{
    "O0,O3,O6": ['O0', 'O3', 'O6'],
    "-": ["X"+str(x) for x in range(9)] + ["O" + str(x) for x in range(9) if x not in [0,3,6]]
},
"ttt_models/ttt_model_row-X0,X3,X6.pnml":{
    "X0,X3,X6": ['X0', 'X3', 'X6'],
    "-": ["X"+str(x) for x in range(9) if x not in [0,3,6]] + ["O" + str(x) for x in range(9)]
},
"ttt_models/ttt_model_row-O1,O4,O7.pnml":{
    "O1,O4,O7": ['O1', 'O4', 'O7'],
    "-": ["X"+str(x) for x in range(9)] + ["O" + str(x) for x in range(9) if x not in [1,4,7]]
},
"ttt_models/ttt_model_row-X1,X4,X7.pnml":{
    "X1,X4,X7": ['X1', 'X4', 'X7'],
    "-": ["X"+str(x) for x in range(9) if x not in [1,4,7]] + ["O" + str(x) for x in range(9)]
},
"ttt_models/ttt_model_row-O2,O5,O8.pnml":{
    "O2,O5,O8": ['O2', 'O5', 'O8'],
    "-": ["X"+str(x) for x in range(9)] + ["O" + str(x) for x in range(9) if x not in [2,5,8]]
},
"ttt_models/ttt_model_row-X2,X5,X8.pnml":{
    "X2,X5,X8": ['X2', 'X5', 'X8'],
    "-": ["X"+str(x) for x in range(9) if x not in [2,5,8]] + ["O" + str(x) for x in range(9)]
},
"ttt_models/ttt_model_row-O0,O4,O8.pnml":{
    "O0,O4,O8": ['O0', 'O4', 'O8'],
    "-": ["X"+str(x) for x in range(9)] + ["O" + str(x) for x in range(9) if x not in [0,4,8]]
},
"ttt_models/ttt_model_row-X0,X4,X8.pnml":{
    "X0,X4,X8": ['X0', 'X4', 'X8'],
    "-": ["X"+str(x) for x in range(9) if x not in [0,4,8]] + ["O" + str(x) for x in range(9)]
},
"ttt_models/ttt_model_row-O2,O4,O6.pnml":{
    "O2,O4,O6": ['O2', 'O4', 'O6'],
    "-": ["X"+str(x) for x in range(9)] + ["O" + str(x) for x in range(9) if x not in [2,4,6]]
},
"ttt_models/ttt_model_row-X2,X4,X6.pnml":{
    "X2,X4,X6": ['X2', 'X4', 'X6'],
    "-": ["X"+str(x) for x in range(9) if x not in [2,4,6]] + ["O" + str(x) for x in range(9)]
}

}
log_sets = {}

for file_name in events_map:
    net, initial_marking, final_marking = pm4py.read_pnml(file_name)
    mod_net, mod_initial_marking, mod_final_marking = get_modified_pn(net, events_map[file_name])
    #pm4py.view_petri_net(mod_net, mod_initial_marking, mod_final_marking)
    simulated_log = simulator.apply(mod_net, mod_initial_marking, variant=simulator.Variants.EXTENSIVE,
                                parameters={simulator.Variants.EXTENSIVE.value.Parameters.MAX_TRACE_LENGTH: MAX_TRACE_LENGTH})
    log_sets[file_name] = set_from_log(simulated_log)

intersected_set = log_sets["ttt_models/ttt_model_player.pnml"]
for file_name, s in log_sets.items():
    intersected_set = intersected_set.intersection(s)

import csv
with open("ttt_our_model_traces.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerows(intersected_set)

net, initial_marking, final_marking = pm4py.read_pnml("ttt_models/ttt_model.pnml")
simulated_log = simulator.apply(net, initial_marking, variant=simulator.Variants.BASIC_PLAYOUT,
                                parameters={simulator.Variants.BASIC_PLAYOUT.value.Parameters.NO_TRACES: NO_TRACES,
                                            simulator.Variants.BASIC_PLAYOUT.value.Parameters.MAX_TRACE_LENGTH: MAX_TRACE_LENGTH})
main_model_set = set_from_log(simulated_log)
import csv
with open("ttt_current_model_traces.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerows(main_model_set)