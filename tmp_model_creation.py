# import pm4py
#
# from pm4py.objects.petri_net.obj import PetriNet, Marking
# from pm4py.objects.petri_net.utils import petri_utils
#
#
# net = PetriNet("new_petri_net")
# p1 = PetriNet.Place("p1")
# net.places.add(p1)
# p2 = PetriNet.Place("p2")
# net.places.add(p2)
# p3 = PetriNet.Place("p3")
# net.places.add(p3)
# A = PetriNet.Transition("A", "A")
# net.transitions.add(A)
# B = PetriNet.Transition("B", "B")
# net.transitions.add(B)
# C = PetriNet.Transition("C", "C")
# net.transitions.add(C)
# petri_utils.add_arc_from_to(p1, A, net)
# petri_utils.add_arc_from_to(A, p2, net)
# petri_utils.add_arc_from_to(p2, B, net)
# petri_utils.add_arc_from_to(p2, C, net)
# petri_utils.add_arc_from_to(B, p3, net)
# petri_utils.add_arc_from_to(C, p3, net)
#
# initial_marking = Marking()
# initial_marking[p1] = 1
# final_marking = Marking()
# final_marking[p3] = 1
#
# pm4py.view_petri_net(net, initial_marking, final_marking)
# tree = pm4py.convert_to_process_tree(net, initial_marking, final_marking)
# pm4py.view_process_tree(tree)
#
#
import pm4py
from pm4py.objects.process_tree.obj import ProcessTree, Operator


tree = ProcessTree(Operator.SEQUENCE,None, None, None)
a = ProcessTree(None,tree,None,"A")

p2 = ProcessTree(Operator.LOOP,tree, None, None)

p1 = ProcessTree(Operator.PARALLEL,p2, None, None)
b = ProcessTree(None,p1,None,"B")
c = ProcessTree(None,p1,None,"C")
p1._set_children([b,c])

d = ProcessTree(None,p2,None,"D")
p2._set_children([p1,d])

p3 = ProcessTree(Operator.XOR,tree, None, None)
e = ProcessTree(None,p3,None,"E")
f = ProcessTree(None,p3,None,None)
p3._set_children([e,f])

tree._set_children([a,p2,p3])

#pm4py.view_process_tree(tree)
from pm4py.algo.simulation.playout.petri_net import algorithm as simulator
net, initial_marking, final_marking = pm4py.convert_to_petri_net(tree)

simulated_log = simulator.apply(net, initial_marking, variant=simulator.Variants.EXTENSIVE,
                                parameters={simulator.Variants.EXTENSIVE.value.Parameters.MAX_TRACE_LENGTH: 10})
df = pm4py.convert_to_dataframe(simulated_log)
d = {}
for i,r in df.iterrows():
    d[r["case:concept:name"]] = d.get(r["case:concept:name"], []) + [r["concept:name"]]
print([",".join(x)  for x in d.values()])

dfg, s, e = pm4py.discover_directly_follows_graph(simulated_log)
pm4py.view_dfg(dfg, s, e)
# tree= pm4py.discover_process_tree_inductive(simulated_log)
# pm4py.view_process_tree(tree)


