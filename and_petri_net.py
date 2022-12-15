from snakes.pnml import loads
from snakes.nets import *
from dfs.dfs_bprogram import DFSPN
import xml.etree.ElementTree as ET

def rename_transitions(pnml_file, output_file):
    d = {}
    tree = ET.parse(pnml_file)
    root = tree.getroot()
    for child in root[0][1].findall('transition'):
        d[child.get("id")] = child.find("name").find("text").text
    print(d)


rename_transitions("output/ttt_model_player.pnml", "output/ttt_model_player_updated.pnml")



# model = loads("/Users/tomyaacov/Downloads/ttt_model_player.pnml")
# g = StateGraph(model)
# init_s, visited, total_events = DFSPN.run(g)
# DFSPN.save_graph(init_s, visited, "test.dot")
