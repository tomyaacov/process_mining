# # import pm4py
# #
# # from pm4py.objects.petri_net.obj import PetriNet, Marking
# # from pm4py.objects.petri_net.utils import petri_utils
# #
# #
# # net = PetriNet("new_petri_net")
# # p1 = PetriNet.Place("p1")
# # net.places.add(p1)
# # p2 = PetriNet.Place("p2")
# # net.places.add(p2)
# # p3 = PetriNet.Place("p3")
# # net.places.add(p3)
# # A = PetriNet.Transition("A", "A")
# # net.transitions.add(A)
# # B = PetriNet.Transition("B", "B")
# # net.transitions.add(B)
# # C = PetriNet.Transition("C", "C")
# # net.transitions.add(C)
# # petri_utils.add_arc_from_to(p1, A, net)
# # petri_utils.add_arc_from_to(A, p2, net)
# # petri_utils.add_arc_from_to(p2, B, net)
# # petri_utils.add_arc_from_to(p2, C, net)
# # petri_utils.add_arc_from_to(B, p3, net)
# # petri_utils.add_arc_from_to(C, p3, net)
# #
# # initial_marking = Marking()
# # initial_marking[p1] = 1
# # final_marking = Marking()
# # final_marking[p3] = 1
# #
# # pm4py.view_petri_net(net, initial_marking, final_marking)
# # tree = pm4py.convert_to_process_tree(net, initial_marking, final_marking)
# # pm4py.view_process_tree(tree)
# #
# #
# import pm4py
# from pm4py.objects.process_tree.obj import ProcessTree, Operator
#
#
# tree = ProcessTree(Operator.SEQUENCE,None, None, None)
# a = ProcessTree(None,tree,None,"A")
#
# p2 = ProcessTree(Operator.LOOP,tree, None, None)
#
# p1 = ProcessTree(Operator.PARALLEL,p2, None, None)
# b = ProcessTree(None,p1,None,"B")
# c = ProcessTree(None,p1,None,"C")
# p1._set_children([b,c])
#
# d = ProcessTree(None,p2,None,"D")
# p2._set_children([p1,d])
#
# p3 = ProcessTree(Operator.XOR,tree, None, None)
# e = ProcessTree(None,p3,None,"E")
# f = ProcessTree(None,p3,None,None)
# p3._set_children([e,f])
#
# tree._set_children([a,p2,p3])
#
# from project_utils import *
# from pm4py.visualization.process_tree import visualizer as pt_visualizer
# parameters = pt_visualizer.Variants.WO_DECORATION.value.Parameters
# gviz = pt_visualizer.apply(tree, parameters={parameters.FORMAT: "png", "bgcolor": "white"})
#
# pt_visualizer.view(gviz)
# #pm4py.view_process_tree(tree)
# save_process_tree_to_dot(tree, "tom.dot")

#pm4py.view_process_tree(tree)
# from pm4py.algo.simulation.playout.petri_net import algorithm as simulator
# net, initial_marking, final_marking = pm4py.convert_to_petri_net(tree)
#
# simulated_log = simulator.apply(net, initial_marking, variant=simulator.Variants.EXTENSIVE,
#                                 parameters={simulator.Variants.EXTENSIVE.value.Parameters.MAX_TRACE_LENGTH: 10})
# df = pm4py.convert_to_dataframe(simulated_log)
# d = {}
# for i,r in df.iterrows():
#     d[r["case:concept:name"]] = d.get(r["case:concept:name"], []) + [r["concept:name"]]
# print([",".join(x)  for x in d.values()])
#
# dfg, s, e = pm4py.discover_directly_follows_graph(simulated_log)
# pm4py.view_dfg(dfg, s, e)
# tree= pm4py.discover_process_tree_inductive(simulated_log)
# pm4py.view_process_tree(tree)


# from pm4py.objects.process_tree.obj import ProcessTree, Operator
# tree = ProcessTree(Operator.PARALLEL,None, None, None)
# cd = ProcessTree(Operator.SEQUENCE,tree, None, None)
# ab = ProcessTree(Operator.SEQUENCE,tree, None, None)
# c = ProcessTree(Operator.XOR,cd, None, None)
# d = ProcessTree(Operator.XOR,cd, None, None)
# a = ProcessTree(Operator.XOR,ab, None, None)
# b = ProcessTree(Operator.XOR,ab, None, None)
# c1 =  ProcessTree(None,a,None,"C1")
# c2 =  ProcessTree(None,b,None,"C2")
# c3 =  ProcessTree(None,c,None,"C3")
# c4 =  ProcessTree(None,d,None,"C4")
# d1 =  ProcessTree(None,a,None,"D1")
# d2 =  ProcessTree(None,b,None,"D2")
# d3 =  ProcessTree(None,c,None,"D3")
# d4 =  ProcessTree(None,d,None,"D4")
# a1 =  ProcessTree(None,a,None,"A1")
# a2 =  ProcessTree(None,b,None,"A2")
# a3 =  ProcessTree(None,c,None,"A3")
# a4 =  ProcessTree(None,d,None,"A4")
# b1 =  ProcessTree(None,a,None,"B1")
# b2 =  ProcessTree(None,b,None,"B2")
# b3 =  ProcessTree(None,c,None,"B3")
# b4 =  ProcessTree(None,d,None,"B4")
# # a._set_children([a1,a2,a3,a4])
# # c._set_children([c1,c2,c3,c4])
# # b._set_children([b1,b2,b3,b4])
# # d._set_children([d1,d2,d3,d4])
#
# a._set_children([a1,b1,c1,d1])
# b._set_children([a2,b2,c2,d2])
# c._set_children([a3,b3,c3,d3])
# d._set_children([a4,b4,c4,d4])
#
# ab._set_children([a, b])
# cd._set_children([c, d])
#
# tree._set_children([ab, cd])
# pm4py.write_ptml(tree, "AD14_models/AD14_model_number_converted.ptml")
# save_process_tree_to_dot(tree, "AD14_models/AD14_model_number_converted.dot")
# pm4py.view_process_tree(tree)


import pm4py
net, initial_marking, final_marking = pm4py.read_pnml("AD14_models/ad14_model_letter.pnml")
from project_utils import *
save_pn_to_dot(net, initial_marking, final_marking, "AD14_models/ad14_model_letter_converted.dot")
