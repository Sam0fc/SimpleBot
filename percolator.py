import sys
"""
You'll want to implement a smarter decision logic. This is skeleton code that you should copy and replace in your repository.
"""
class PercolationPlayer:
    # `graph` is an instance of a Graph, `player` is an integer (0 or 1).
    # Should return a vertex `v` from graph.V where v.color == -1
    def ChooseVertexToColor(graph, player):
            degree = dict()
            current_greatest = -1
            current_greatest_vertex = next(iter(graph.V))
            for v in graph.V:
                if v.color == -1:
                    degree = len(IncidentEdges(graph,v))
                    if degree>current_greatest:
                        current_greatest = degree
                        current_greatest_vertex = v
            return current_greatest_vertex

    # `graph` is an instance of a Graph, `player` is an integer (0 or 1).
    # Should return a vertex `v` from graph.V where v.color == player
    def ChooseVertexToRemove(graph, player):
        degree = dict()
        current_least = sys.maxsize
        current_least_vertex = next(iter(graph.V))
        for v in graph.V:
            if v.color==player:
                degree = len(IncidentEdges(graph,v))
                if degree<current_least:
                    current_least = degree
                    current_least_vertex = v
        return current_least_vertex

# Feel free to put any personal driver code here.
def main():
    pass

def IncidentEdges(graph, v):
    return [e for e in graph.E if (e.a == v or e.b == v)]

if __name__ == "__main__":
    main()
