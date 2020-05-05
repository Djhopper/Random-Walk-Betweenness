from graphs.read_write import read_graph
from scripts.timing.time_algorithm_execution import time_random_walk_centrality_algorithm
import pandas as pd
from scipy.stats import sem
from math import log10, floor


def get_data():
    real_world_graphs = [
        "p2p-Gnutella04.txt", "CA-GrQc.txt", "email-Eu-core.txt", "facebook_combined.txt"]

    data = []
    for graph_name in real_world_graphs:
        g = read_graph(graph_name)

        for _ in range(5):
            print(graph_name, g.number_of_nodes(), _)
            brandes = time_random_walk_centrality_algorithm(g, strategy="brandes")
            approx = time_random_walk_centrality_algorithm(g, strategy="approx")
            data.append({
                "dataset": graph_name,
                "n": g.number_of_nodes(),
                "m": g.number_of_edges(),
                "brandes": brandes["time"],
                "approx": approx["time"]
            })

    df = pd.DataFrame(data)
    df.to_csv("real_world_brandes_vs_approx/brandes_vs_approx_data.csv", index=False)


def get_analysis():
    def round_sig(x, sig=2):
        return round(x, sig - int(floor(log10(abs(x)))) - 1)

    dataset_name = {
        "p2p-Gnutella04.txt": "Gnutella-P2P",
        "CA-GrQc.txt": "GRQC-Collab",
        "email-Eu-core.txt": "Email-EU",
        "facebook_combined.txt": "Facebook",
    }

    df = pd.read_csv("real_world_brandes_vs_approx/brandes_vs_approx_data.csv")

    data = []
    for dataset in df.dataset.unique():
        df_f = df[df.dataset == dataset]
        data.append({
            "dataset": dataset_name[dataset],
            "n": int(df_f.n.mean()),
            "m": int(df_f.m.mean()),
            "brandes_mean": round_sig(df_f.brandes.mean(), 3),
            "brandes_err": round_sig(sem(df_f.brandes), 3),
            "approx_mean": round_sig(df_f.approx.mean(), 3),
            "approx_err": round_sig(sem(df_f.approx), 3)
        })

    df = pd.DataFrame(data)
    df = df.sort_values("n")
    df.to_csv("real_world_brandes_vs_approx/brandes_vs_approx_analysis.csv", index=False)


if __name__ == '__main__':
    #get_data()
    get_analysis()
