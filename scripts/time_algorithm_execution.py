from algorithms.random_walk_centrality.random_walk_centrality import random_walk_centrality
from timeit import default_timer as timer
from graphs.read_write import read_graph


def time_random_walk_centality_algorithm(graph_name, method_name):
    start_setup = timer()
    g = read_graph(graph_name)
    end_setup = timer()

    start_calculation = timer()
    result = random_walk_centrality(g, method=method_name)
    end_calculation = timer()

    return {
        "graph_name": graph_name,
        "method_name": method_name,
        "setup_time": end_setup - start_setup,
        "calculation_time": end_calculation - start_calculation,
    }


if __name__ == '__main__':
    print(time_random_walk_centality_algorithm("erdos_renyi", "nx"))
