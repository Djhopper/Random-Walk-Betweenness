from graphs.random_graphs import get_erdos_renyi
from graphs.random_graphs import get_watts_strogatz_graph
from graphs.random_graphs import get_holme_kim
from scripts.timing.time_algorithm_execution import time_random_walk_betweenness_algorithm
import pandas as pd
from scipy.stats import sem
import numpy as np


# Times given implementations on erdos-renyi graphs of gradually increasing sizes,
# stopping when runtime exceeds max_time
def time_until_failure(strategies, graph_generator, graph_type, repeats=10, timeout=None,
                       max_nodes=None, node_interval=50):
    assert timeout is not None or max_nodes is not None

    df = []

    nodes = 0
    while len(strategies) > 0 and (max_nodes is None or nodes < max_nodes):
        nodes += node_interval

        print("Doing " + str(nodes) + " node " + graph_type + " graph using methods: ", strategies)

        for i in range(repeats):
            g = graph_generator(nodes)
            for strategy in list(strategies):
                data = time_random_walk_betweenness_algorithm(g, strategy)
                if data["time"] >= timeout:
                    strategies.remove(strategy)
                    data["time"] = "timeout"
                data["graph_type"] = graph_type
                df.append(data)

    df = pd.DataFrame(df)
    return df


def get_data():
    graph_generators = {
        "erdos_renyi": lambda n: get_erdos_renyi(n, 10),
        "watts_strogatz": lambda n: get_watts_strogatz_graph(n, 0.1, 10),
        "holme_kim": lambda n: get_holme_kim(n, 0.1, 10),
    }

    dfs = []
    for graph_type in graph_generators:
        df = time_until_failure(
            strategies=["nx", "newman", "brandes"],
            graph_generator=graph_generators[graph_type],
            graph_type=graph_type,
            repeats=5,
            timeout=300,
            max_nodes=5000,
            node_interval=500)
        dfs.append(df)

    df = pd.concat(dfs)
    df.to_csv("random_graph_benchmarking/random_graph_benchmarking_data.csv", index=False)


def get_analysis_(approx):
    if approx:
        df = pd.read_csv("random_graph_benchmarking_approx/random_graph_benchmarking_approx_data.csv")
    else:
        df = pd.read_csv("random_graph_benchmarking/random_graph_benchmarking_data.csv")

    df = df.dropna().rename(columns={"nodes": "n"})
    df = df[~(df["time"] == "timeout")]
    df = df.astype({"time": float})

    for graph_type in df["graph_type"].unique():
        for method_name in df["method_name"].unique():
            data = []
            for n in df[(df["graph_type"] == graph_type) & (df["method_name"] == method_name)]["n"].unique():
                df_f = df[(df["graph_type"] == graph_type) & (df["method_name"] == method_name) & (df["n"] == n)]
                mean = np.mean(np.array(df_f["time"]))
                err = sem(df_f["time"])

                data.append({
                    "n": n,
                    "graph_type": graph_type,
                    "method_name": method_name,
                    "mean": mean,
                    "err": 2 * err,
                })

            new_df = pd.DataFrame(data)
            if approx:
                new_df.to_csv("random_graph_benchmarking_approx/"+graph_type+"_"+method_name+"_analysis.csv", index=False)
            else:
                new_df.to_csv("random_graph_benchmarking/"+graph_type+"_"+method_name+"_analysis.csv", index=False)


def get_analysis():
    get_analysis_(True)
    get_analysis_(False)


def get_data_approx():
    graph_generators = {
        "erdos_renyi": lambda n: get_erdos_renyi(n, 10),
        "watts_strogatz": lambda n: get_watts_strogatz_graph(n, 0.1, 10),
        "holme_kim": lambda n: get_holme_kim(n, 0.1, 10),
    }

    dfs = []
    for graph_type in graph_generators:
        df = time_until_failure(
            strategies=["nxapprox", "approx"],
            graph_generator=graph_generators[graph_type],
            graph_type=graph_type,
            repeats=5,
            timeout=300,
            max_nodes=5000,
            node_interval=500)
        dfs.append(df)

    df = pd.concat(dfs)
    df.to_csv("random_graph_benchmarking_approx/random_graph_benchmarking_approx_data.csv", index=False)


if __name__ == '__main__':
    #get_data()
    #get_data_approx()
    get_analysis()
