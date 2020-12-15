import random
"""
You'll want to implement a smarter decision logic. This is skeleton code that you should copy and replace in your repository.
"""
class PercolationPlayer:
    # `graph` is an instance of a Graph, `player` is an integer (0 or 1).
    # Should return a vertex `v` from graph.V where v.color == -1
    def ChooseVertexToColor(graph, player):
        degree = dict()
        current_greatest = 0
        current_greatest_vertex = next(iter(graph.V)
        for v in graph.V:
            degree = len(IncidentEdges())
            if degree>current_greatest:
                current_greatest 

            if IncidentEdges(graph,v) >

    # `graph` is an instance of a Graph, `player` is an integer (0 or 1).
    # Should return a vertex `v` from graph.V where v.color == player
    def ChooseVertexToRemove(graph, player):
        for v in graph.V:
            if v.color == player:
                return v

# Feel free to put any personal driver code here.
def main():
    pass

def IncidentEdges(graph, v):
    return [e for e in graph.E if (e.a == v or e.b == v)]

if __name__ == "__main__":
    main()
