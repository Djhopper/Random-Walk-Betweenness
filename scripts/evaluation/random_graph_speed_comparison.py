from graphs.random_graphs import get_erdos_renyi
from scripts.timing.time_algorithm_execution import time_random_walk_centrality_algorithm
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Times given implementations on erdos-renyi graphs of gradually increasing sizes,
# stopping when runtime exceeds max_time
def time_on_erdos_renyi_graphs(methods, repeats=10, max_time=None, max_nodes=None,
                               node_interval=50, average_degree=10, debug=False):
    assert max_time is not None or max_nodes is not None

    data = []

    nodes = 0
    while len(methods) > 0 and (max_nodes is None or nodes < max_nodes):
        nodes += node_interval
        if debug:
            print("Doing " + str(nodes) + " node graph using methods: ", methods)

        new_data = []
        for i in range(repeats):
            g = get_erdos_renyi(nodes, average_degree)
            for method in list(methods):
                new_data.append(time_random_walk_centrality_algorithm(g, method))

        new_data = pd.DataFrame(new_data)

        for method in list(methods):
            avg_time = new_data[new_data["method_name"] == method]["time"].mean()
            if max_time is not None and avg_time > max_time:
                methods.remove(method)

        data.append(new_data)

    df = pd.concat(data)
    return df


if __name__ == '__main__':
    g = get_erdos_renyi(300, 10)
    print(time_random_walk_centrality_algorithm(g, "nx"))
    print(time_random_walk_centrality_algorithm(g, "newman"))
    '''
    df = time_on_erdos_renyi_graphs(
        methods=["nx", "brandes"],
        repeats=100,
        max_time=None,
        max_nodes=1000,
        node_interval=100,
        average_degree=10,
        debug=False
    )
    df.to_csv("presentation_fig2_data.csv", index=False)
    print(df)
    '''
