from graphs.read_write import read_graph
from scripts.timing.time_algorithm_execution import time_random_walk_centrality_algorithm
import pandas as pd
from scipy.stats import sem


def get_data():
    g = read_graph("facebook_combined.txt")

    N = 1
    data = []
    for _ in range(N):
        brandes = time_random_walk_centrality_algorithm(g, strategy="brandes")
        networkx = time_random_walk_centrality_algorithm(g, strategy="nx")
        data.append({
            "brandes_time": brandes["time"],
            "nx_time": networkx["time"]
        })

    df = pd.DataFrame(data)
    df.to_csv("brandes_vs_networkx/brandes_vs_networkx_data.csv", index=False)


def get_analysis():
    df = pd.read_csv("brandes_vs_networkx/brandes_vs_networkx_data.csv")
    print(
        df.brandes_time.mean(),
        df.nx_time.mean(),
        df.nx_time.mean() / df.brandes_time.mean(),
        2 * sem(df.brandes_time),
        2 * sem(df.nx_time),
    )


if __name__ == '__main__':
    #get_data()
    get_analysis()
