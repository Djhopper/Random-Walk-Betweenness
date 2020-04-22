import networkx as nx
from scipy.sparse import linalg
import numpy as np
from scripts.timing.Profiler import Profiler
from graphs.random_graphs import get_erdos_renyi
import pandas as pd
from scipy.stats import sem


'''
This shows that partial LU decomposition method, as implemented in the scipy.sparse.linalg.spilu is about 3 times slower
than the builtin numpy method of inverting the matrix, even for very large n. Therefore it is unsuitable for speeding up 
matrix inversion.
'''


def do_test(n):
    # Create graph
    g = get_erdos_renyi(n=n, average_degree=10)
    # Setup (create matrix that needs to be inverted)
    n = g.number_of_nodes()
    M = nx.linalg.laplacianmatrix.laplacian_matrix(g).tolil()
    M = M[list(range(1, n)), :]
    M = M[:, list(range(1, n))]

    tm = Profiler()

    N = np.array(M)
    tm.mark("matrix_to_array")
    K = np.asmatrix(N)
    tm.mark("array_to_matrix")

    data = tm.get_data()
    data["n"] = n
    print(data)
    return data


def get_data():
    data = []
    for n in range(2000, 10001, 2000):
        for _ in range(5):
            data.append(do_test(n))
    df = pd.DataFrame(data)
    df.drop(columns="_", inplace=True)
    df.to_csv("inversion_methods/data.csv", index=False)


def get_analysis():
    df = pd.read_csv("inversion_methods/data.csv")
    df["n"] = df["n"].round(decimals=-3)

    data = []
    for n in df["n"].unique():
        df_filtered = df[df["n"] == n]
        err1 = sem(df_filtered["matrix"])
        err2 = sem(df_filtered["array"])
        err3 = sem(df_filtered["spilu"])
        mean1 = df_filtered["matrix"].mean()
        mean2 = df_filtered["array"].mean()
        mean3 = df_filtered["spilu"].mean()

        data.append({
            "n": n,
            "matrix_mean": mean1,
            "matrix_err": err1*2,
            "array_mean": mean2,
            "array_err": err2*2,
            "spilu_mean": mean3,
            "spilu_err": err3*2,
        })

    df_out = pd.DataFrame(data)
    df_out.to_csv("inversion_methods/inversion_methods_analysis.csv", index=False)


if __name__ == '__main__':
    do_test(10000)
    quit()
    #get_data()
    get_analysis()
