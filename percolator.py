import sys
import benchmark
import time
import copy
import multiprocessing
import util
import random
INIT_PS_COEFF = -3
INIT_SUM_COEFF = 10
INIT_SIZE_COEFF = -0.5
INIT_EDGE_COEFF = -4
INIT_SELF_COEFF = 10
INIT_RATIO_COEFF = 10
#caching
def memoize(f):
    cache = {}
    def g(x):
        if x not in cache:
            cache[x] = f(x)
        return cache[x]
    return g

def time2(f):
    def g(x,y):
        tick = time.perf_counter()
        value = f(x,y)
        tock = time.perf_counter()
        print(tock-tick)
        return value
    return g


#caching
def memoize2(f):
    cache = {}
    def g(x,y):
        if (x,y) not in cache:
            cache[(x,y)] = f(x,y)
        return cache[(x,y)]
    return g


# Removes the given vertex v from the graph, as well as the edges attached to it.
# Removes all isolated vertices from the graph as well.
def Percolate(graph, v):
    # Get attached edges to this vertex, remove them.
    for e in IncidentEdges(graph, v):
        graph.E.remove(e)
    # Remove this vertex.
    graph.V.remove(v)
    # Remove all isolated vertices.
    to_remove = {u for u in graph.V if len(IncidentEdges(graph, u)) == 0}
    graph.V.difference_update(to_remove)


class PercolationPlayer:

    class look_ahead_iter:
        def __init__(self, graph,vertex,player):
            self.graph = graph
            self.player = player
            if vertex in self.graph.V:
                Percolate(self.graph,vertex)
            if self.graph != None:
                self.heur = PercolationPlayer.get_heur(self.graph,player,True)
            else:
                self.heur = sys.maxsize

        def __iter__(self):
            return self

        def __next__(self):
            self.heur, self.graph = PercolationPlayer.best_worst_possible(self.graph,False,not self.player)
            self.heur, self.graph = PercolationPlayer.best_worst_possible(self.graph,True,self.player)


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
        tick = time.perf_counter()
        best_vertex = None
        best_heur = -1 * sys.maxsize
        done = False
        look_ahead_dict = {}
        for vertex in list(graph.V):
            if vertex.color == player:
                new_graph = util.Graph(graph.V,graph.E)
                new_iter = PercolationPlayer.look_ahead_iter(new_graph,vertex,player)
                look_ahead_dict[vertex] = new_iter
                if new_iter.heur > best_heur:
                    best_heur = new_iter.heur
                    best_vertex = vertex
        while not done: #TIMEEe
            for vertex in graph.V:
                if vertex.color == player:
                    next(look_ahead_dict[vertex])
                    if new_iter.heur > best_heur:
                        best_heur = new_iter.heur
                        best_vertex = vertex
            if time.perf_counter()-tick > 0.35:
                done = True
        if best_vertex == None:
            return sim_random_player_remove(graph,player)
        return best_vertex



    def best_worst_possible(graph,best,player):
        best_heur = sys.maxsize * int(not best)
        best_graph = None
        if graph == None:
            return (sys.maxsize,graph)
        for vertex in graph.V:
            if vertex.color == player:
                new_graph = util.Graph(graph.V,graph.E)
                new_graph = Percolate(new_graph,vertex)
                if new_graph != None:
                    graph_heur = PercolationPlayer.get_heur(new_graph,player,best)
                    if best:
                        if graph_heur>best_heur:
                            best_heur = graph_heur
                            best_graph = new_graph
                    else:
                        if graph_heur<best_heur:
                            best_heur = graph_heur
                            best_graph = new_graph
        return (best_heur,best_graph)

    def get_heur(graph, player, me, sum_coeff =INIT_SUM_COEFF, self_coeff=INIT_SELF_COEFF, size_coeff=INIT_SIZE_COEFF, edge_coeff=INIT_EDGE_COEFF, player_size_coeff=INIT_PS_COEFF,ratio_coeff = INIT_RATIO_COEFF):
        if len(graph.V) == 0:
            if me:
                return sys.maxsize
            else:
                return -1 * sys.maxsize
        else:
            return (sum_coeff * sum_degree(graph,player) + self_coeff * self_degree(graph,player) + len(graph.V)*size_coeff + len(graph.E)*edge_coeff + player_size(graph,player) *player_size_coeff + ratio_coeff * player_size(graph,player)/len(graph.V))

def sum_degree(graph,player):
    running_total = 0
    for vertex in graph.V:
        if vertex.color == player:
            running_total+= len(IncidentEdges(graph,vertex))
    return running_total

def self_degree(graph,player):
    running_total = 0
    for vertex in graph.V:
        if vertex.color == player:
            running_total+=len(IncidentPlayerEdges(graph,vertex,player))
    return running_total

def player_size(graph,player):
    running_total=0
    for vertex in graph.V:
        if vertex.color==player:
            running_total+=1
    return running_total


def sim_random_player_remove(graph,player):
    return random.choice([v for v in graph.V if v.color == player])


# Feel free to put any personal driver code here.
def main():
    pass

@memoize2
def IncidentEdges(graph, v):
    return [e for e in graph.E if (e.a == v or e.b == v)]

def IncidentPlayerEdges(graph, v,player):
    return [e for e in graph.E if ((e.a == v or e.b == v) and (e.a.color==player and e.b.color==player))]

"""
Inputs to machine learning:
1. Whole Laplacian?
2. Graph2Vec
3. Size/Incident Edges/Links
"""
if __name__ == "__main__":
    main()
