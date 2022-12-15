from snakes.nets import *
import graphviz
class DFSNode:
    def __init__(self, _id):
        self.id = _id
        self.transitions = {}

    def __key(self):
        return self.id

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return self.__key() == other.__key()

class DFSPN:

    @staticmethod
    def run(g: StateGraph):
        total_events = set()
        g.goto(g.current())
        init_s = DFSNode(g.current())
        visited = {}
        stack = []
        stack.append(init_s)

        while (len(stack)):
            s = stack.pop()
            if not visited.get(s):
                visited[s] = True
            g.goto(s.id)
            l = list(g.successors())
            for new_s, t, _ in l:
                total_events.add(t)
                s.transitions[t] = new_s
                if not visited.get(DFSNode(new_s)):
                    stack.append(DFSNode(new_s))
        return init_s, visited, total_events

    @staticmethod
    def save_graph(init, states, name):
        g = graphviz.Digraph()
        for s in states:
            g.node(str(s.id), shape='doublecircle' if s == init else 'circle')
        for s in states:
            for t, s_new in s.transitions.items():
                g.edge(str(s.id), str(s_new), label=t.name)
        g.save(name)
        return g





