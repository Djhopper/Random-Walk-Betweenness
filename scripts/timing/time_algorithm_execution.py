from random_walk_betweenness.calculate import random_walk_betweenness
from timeit import default_timer as timer
from graphs.read_write import read_graph


# Runs a random walk centrality algorithm on a graph and returns a dictionary with information about how long it took
# graph - can be a networkx graph, or can be a string which is the name of a graph that has been stored previously
# method_name - string, dictates which implementation will be used
def time_random_walk_centrality_algorithm(graph, method_name):
    # Setup graph
    if type(graph) == str:
        g = read_graph(graph)
    else:
        g = graph
        graph = "_"

    start_calculation = timer()

    # Execute algorithm
    result = random_walk_betweenness(g, strategy=method_name)

    end_calculation = timer()

    return {
        "graph_name": graph,
        "method_name": method_name,
        "time": end_calculation - start_calculation,
        "edges": g.number_of_edges(),
        "nodes": g.number_of_nodes(),
    }
