from graphs.random_graphs import get_erdos_renyi
from random_walk_betweenness.calculate import random_walk_betweenness
from scripts.timing.time_algorithm_execution import time_random_walk_centrality_algorithm
import pandas as pd
from scipy.stats import sem


def try_brandes(n):
    g = get_erdos_renyi(n, 10)
    try:
        random_walk_betweenness(g, strategy="brandes")
        return True
    except MemoryError:
        return False


def try_approx(n):
    g = get_erdos_renyi(n, 10)
    print("graph generated with", n, "nodes")
    try:
        random_walk_betweenness(g, strategy="approx", epsilon=0.5)
        return True
    except MemoryError:
        return False


def time_big_graph():
    data = [time_random_walk_centrality_algorithm("Email-Enron.txt", strategy="approx", epsilon=0.5) for _ in range(5)]
    df = pd.DataFrame(data)
    df.to_csv("maximum_graph_size/data.csv", index=False)


def big_graph_results():
    df = pd.read_csv("maximum_graph_size/data.csv")
    print(df.time.mean())
    print(sem(df.time))


def time_max_graphs():
    data = []
    g = get_erdos_renyi(12000, 10)
    data.append(time_random_walk_centrality_algorithm(g, strategy="brandes"))
    print(data[-1])
    g = get_erdos_renyi(200000, 10)
    data.append(time_random_walk_centrality_algorithm(g, strategy="approx", epsilon=0.5))
    print(data[-1])

    df = pd.DataFrame(data)
    df.to_csv("maximum_graph_size/max_graph_data.csv", index=False)


if __name__ == '__main__':
    from scripts.evaluation.approx_vs_exact import get_data2 as doit
    time_max_graphs()
    print("max graphs timed")
    doit()
    print("gooooo team")
