from graphs.random_graphs import get_erdos_renyi
from scripts.timing.time_algorithm_execution import time_random_walk_centrality_algorithm
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def get_data():
    repeats = 5
    ns = range(2000, 10001, 2000)
    epsilons = [0.4, 0.2, 0.1, 0.05, 0.025]

    data = []
    for _ in range(repeats):
        print("repeat", _)
        for n in ns:
            g = get_erdos_renyi(n, 10)
            print("n=",n)
            brandes_data = time_random_walk_centrality_algorithm(graph=g, strategy="brandes")
            for epsilon in epsilons:
                print("n=",n,", epsilon=",epsilon)
                approx_data = time_random_walk_centrality_algorithm(graph=g, strategy="approx", epsilon=epsilon)
                data.append({
                    "brandes_time": brandes_data["time"],
                    "approx_time": approx_data["time"],
                    "nodes": n,
                    "epsilon": epsilon
                })

    df = pd.DataFrame(data)
    df.to_csv("approx_vs_exact/heatmap_data.csv", index=False)


def get_analysis():
    df = pd.read_csv("approx_vs_exact/heatmap_data.csv").dropna()

    data = []
    for n in df.nodes.unique():
        brandes_mean = df[df.nodes == n].brandes_time.unique().mean()
        for epsilon in df.epsilon.unique():
            df_f = df[(df.nodes == n) & (df.epsilon == epsilon)]
            approx_mean = df_f.approx_time.mean()
            approx_over_brandes = approx_mean / brandes_mean
            data.append({
                "n": n,
                "epsilon": epsilon,
                "approx/brandes": np.log2(approx_over_brandes),
            })

    df = pd.DataFrame(data)
    df.to_csv("approx_vs_exact/heatmap_analysis.csv", index=False)


def do_plot():
    df = pd.read_csv("approx_vs_exact/heatmap_analysis.csv")
    pivot = df.pivot(index="epsilon", columns="n", values="approx/brandes")
    sns.heatmap(pivot, cbar_kws={"ticks": range(-8, 3, 1)}, center=0, cmap="bwr")
    plt.savefig("approx_vs_exact/heatmap.png")


if __name__ == '__main__':
    #get_data()
    get_analysis()
    do_plot()
