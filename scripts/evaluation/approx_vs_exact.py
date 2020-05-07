from graphs.random_graphs import get_erdos_renyi
from scripts.timing.time_algorithm_execution import time_random_walk_betweenness_algorithm
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
            print("n=", n)
            brandes_data = time_random_walk_betweenness_algorithm(graph=g, strategy="brandes")
            for epsilon in epsilons:
                print("n=",n,", epsilon=",epsilon)
                approx_data = time_random_walk_betweenness_algorithm(graph=g, strategy="approx", epsilon=epsilon)
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
                "nodes": n,
                "epsilon": epsilon,
                "approx/brandes": np.log2(approx_over_brandes),
            })

    df = pd.DataFrame(data)
    df.to_csv("approx_vs_exact/heatmap_analysis.csv", index=False)


def do_plot():
    df = pd.read_csv("approx_vs_exact/heatmap_analysis.csv")
    df.nodes = df.nodes.astype(int)
    pivot = df.pivot(index="epsilon", columns="nodes", values="approx/brandes")
    sns.heatmap(pivot, cbar_kws={"ticks": range(-8, 3, 1), "label": "score"}, center=0, cmap="bwr", annot=True)
    plt.savefig("approx_vs_exact/heatmap.png")
    plt.show()


def get_data2():
    p1 = lambda x: 10/x
    p2 = lambda x: (30000/(6000*np.log(6000)))*2*np.log(x)/x
    p3 = lambda x: 1/600
    repeats = 5
    ns = range(2000, 10001, 2000)
    epsilons = [0.4, 0.2, 0.1, 0.05, 0.025]

    data = []
    for _ in range(repeats):
        print("repeat", _)
        for p_func, p_name in zip([p1, p2, p3], ["n", "n_log_n", "n^2"]):
            print(p_name)

            for n in ns:
                p = p_func(n)
                g = get_erdos_renyi(n, n*p)
                print("n=", g.number_of_nodes(), "m=", g.number_of_edges())
                brandes_data = time_random_walk_betweenness_algorithm(graph=g, strategy="brandes")
                for epsilon in epsilons:
                    print("epsilon=", epsilon)
                    approx_data = time_random_walk_betweenness_algorithm(graph=g, strategy="approx", epsilon=epsilon)
                    data.append({
                        "p_name": p_name,
                        "brandes_time": brandes_data["time"],
                        "approx_time": approx_data["time"],
                        "nodes": n,
                        "epsilon": epsilon
                    })

        df2 = pd.DataFrame(data)
        df2.to_csv("approx_vs_exact/heatmap_data_2.csv", index=False)
        print("saved repeat", _)


def get_analysis_2():
    df = pd.read_csv("approx_vs_exact/heatmap_data_2.csv").dropna()

    data = []
    for p_name in df.p_name.unique():
        df_f = df[df.p_name == p_name]
        for n in df_f.nodes.unique():
            brandes_mean = df_f[df_f.nodes == n].brandes_time.unique().mean()
            for epsilon in df_f.epsilon.unique():
                df_f = df_f[(df_f.nodes == n) & (df_f.epsilon == epsilon)]
                approx_mean = df_f.approx_time.mean()
                approx_over_brandes = approx_mean / brandes_mean
                data.append({
                    "p_name"
                    "nodes": n,
                    "epsilon": epsilon,
                    "approx/brandes": np.log2(approx_over_brandes),
                })

    df = pd.DataFrame(data)
    df.to_csv("approx_vs_exact/heatmap_analysis_2.csv", index=False)


if __name__ == '__main__':
    #get_data2()
    #get_data()
    get_analysis()
    do_plot()
