from random_walk_betweenness.calculate import random_walk_betweenness
from graphs.read_write import read_graph
import pandas as pd
import numpy as np


real_world_graphs = ["CA-GrQc.txt", "Email-Enron.txt", "email-Eu-core.txt", "facebook_combined.txt", "p2p-Gnutella04.txt"]


def get_residuals(graph_name, epsilon=0.05):
    g = read_graph(graph_name)

    exact_solution = random_walk_betweenness(g, strategy="brandes")
    approximate_solution = random_walk_betweenness(g, strategy="approx", epsilon=epsilon)

    df = pd.DataFrame({"n": n, "exact": exact_solution[n], "approx": approximate_solution[n]} for n in exact_solution)
    df["residual"] = df.approx - df.exact
    df["abs_error"] = np.abs(df.residual)
    df["sqr_error"] = df.residual ** 2

    return df


def get_data():
    df = get_residuals(real_world_graphs[0])
    df.to_csv("accuracy/GRQC_Collab_Data.csv", index=False)
    df = get_residuals(real_world_graphs[2])
    df.to_csv("accuracy/EU_Email_Data.csv", index=False)
    df = get_residuals(real_world_graphs[3])
    df.to_csv("accuracy/Facebook_Data.csv", index=False)
    df = get_residuals(real_world_graphs[4])
    df.to_csv("accuracy/Gnutella_P2P_Data.csv", index=False)


def get_analysis():
    data = []
    for x,y in zip(["EU_Email", "Facebook", "GRQC_Collab", "Gnutella_P2P"], [1005, 4039, 5242, 10876]):
        df = pd.read_csv("accuracy/"+x+"_Data.csv")
        data.append({
            "dataset": x.replace("_", "-"),
            "n": y,
            "mean_abs_error": round(df.abs_error.mean(), 4),
            "99_quantile": round(df.abs_error.quantile(0.99), 4),
            "999_quantile": round(df.abs_error.quantile(0.999), 4),
            "max_abs_error": round(df.abs_error.max(), 4),
        })
    df = pd.DataFrame(data)
    df.to_csv("accuracy/accuracy_on_real_world_graphs.csv", index=False)
    print(df)


if __name__ == '__main__':
    #get_data()
    get_analysis()
