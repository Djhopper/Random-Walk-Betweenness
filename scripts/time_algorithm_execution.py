import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from algorithms.random_walk_centrality.random_walk_centrality import random_walk_centrality
from timeit import default_timer as timer
from graphs.read_write import read_graph


def time_random_walk_centrality_algorithm(graph_name, method_name):
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
        "edges": g.number_of_edges(),
        "nodes": g.number_of_nodes(),
    }


if __name__ == '__main__':
    from graphs.random_graphs import generate_erdos_renyi
    import pandas as pd
    data = []
    for n in range(2000, 2001, 100):
        generate_erdos_renyi(n, 10/n, "erdos_renyi_temp")
        data.append(time_random_walk_centrality_algorithm("erdos_renyi_temp", "nx"))
        data.append(time_random_walk_centrality_algorithm("erdos_renyi_temp", "brandes"))

    df = pd.DataFrame(data)

    df.to_csv("dat.csv", index=False)
