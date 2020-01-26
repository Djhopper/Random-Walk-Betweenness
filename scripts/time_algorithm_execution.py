from random_walk_centrality import calculate
from timeit import default_timer as timer
from graphs.read_write import read_graph
from graphs.random_graphs import get_erdos_renyi
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


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
    result = calculate(g, method=method_name)

    end_calculation = timer()

    return {
        "graph_name": graph,
        "method_name": method_name,
        "time": end_calculation - start_calculation,
        "edges": g.number_of_edges(),
        "nodes": g.number_of_nodes(),
    }


# Times given implementations on erdos-renyi graphs of gradually increasing sizes,
# stopping when runtime exceeds max_time
def time_on_erdos_renyi_graphs(methods, repeats=10, max_time=0.1, node_interval=50, average_degree=10, debug=False):
    data = []

    nodes = 0
    while len(methods) > 0:
        nodes += node_interval
        if debug:
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


def plot_brande_on_erdos_renyi():
    df = time_on_erdos_renyi_graphs(["nx"], 1, 80, 250, 10, False)[["nodes", "edges", "time"]]
    sns.scatterplot(x="nodes", y="time", data=df)
    plt.show()


if __name__ == '__main__':
    plot_brande_on_erdos_renyi()
    quit()

    df = time_on_erdos_renyi_graphs(["nx", "brandes", "newman"], debug=True)
    df.to_csv("betweenness_algorithm_speeds_on_sparse_erdos_renyi_graphs.csv", index=False)
    print(df)
