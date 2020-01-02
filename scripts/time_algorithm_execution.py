import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.random_walk_centrality.random_walk_centrality import random_walk_centrality
from timeit import default_timer as timer
from graphs.read_write import read_graph
from graphs.random_graphs import get_erdos_renyi
import numpy as np
import pandas as pd


def time_random_walk_centrality_algorithm(graph, method_name):
    start_setup = timer()

    if type(graph) == str:
        g = read_graph(graph)
    else:
        g = graph
        graph = "_"

    end_setup = timer()

    start_calculation = timer()

    result = random_walk_centrality(g, method=method_name)

    end_calculation = timer()

    return {
        "graph_name": graph,
        "method_name": method_name,
        "setup_time": end_setup - start_setup,
        "time": end_calculation - start_calculation,
        "edges": g.number_of_edges(),
        "nodes": g.number_of_nodes(),
    }


def time_on_erdos_renyi_graphs(methods):
    repeats = 10
    max_time = 5
    node_interval = 50
    average_degree = 10

    data = []

    nodes = 0
    while len(methods) > 0:
        nodes += node_interval
        print("Doing " + str(nodes) + " node graph using methods: ", methods)

        g = get_erdos_renyi(nodes, average_degree)

        for method in list(methods):
            new_data = []
            for i in range(repeats):
                new_data.append(time_random_walk_centrality_algorithm(g, method))

            avg_time = np.mean([x["time"] for x in new_data])
            if avg_time > max_time:
                methods.remove(method)

            data += new_data

    df = pd.DataFrame(data)
    return df


if __name__ == '__main__':
    df = time_on_erdos_renyi_graphs(["nx", "brandes_dense", "newman"])
    df.to_csv("betweenness_algorithm_speeds_on_sparse_erdos_renyi_graphs.csv", index=False)
    print(df)

    quit()

    from graphs.random_graphs import generate_erdos_renyi
    data = []
    for n in range(500, 1001, 100):
        generate_erdos_renyi(n, 10/n, "erdos_renyi_temp")
        data.append(time_random_walk_centrality_algorithm("erdos_renyi_temp", "brandes_sparse"))
        data.append(time_random_walk_centrality_algorithm("erdos_renyi_temp", "brandes_dense"))

    df = pd.DataFrame(data)
    print(df)
    df.to_csv("dat.csv", index=False)
