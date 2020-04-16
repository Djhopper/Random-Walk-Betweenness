import networkx as nx
from scipy.sparse import linalg
import numpy as np
from scripts.timing.timing_bench import TimeMachine
from graphs.random_graphs import get_erdos_renyi
import pandas as pd
from scipy.stats import sem
import scipy


def do_test(n):
    # Create graph
    g = get_erdos_renyi(n=n, average_degree=n/4)
    # Setup
    n = g.number_of_nodes()
    A = nx.linalg.laplacianmatrix.laplacian_matrix(g).tolil()
    A = A[list(range(1, n)), :]
    A = A[:, list(range(1, n))].tocsc()

    b = np.ones(n-1)

    tm = TimeMachine()

    preconditioner = linalg.spilu(A)
    tm.time("spilu_preconditioner")

    for k in range(10):
        x = preconditioner.solve(b)
    tm.time("spilu_solve")

    A = np.matrix(A.todense())
    tm.time("_")

    A_inv = A.I
    tm.time("inversion")

    for k in range(10):
        x = np.matmul(A_inv, b)
    tm.time("multiplication")

    data = tm.get_data()
    data["n"] = n
    return data


def get_data():
    data = []
    for n in range(2000, 10001, 2000):
        for _ in range(1):
            data.append(do_test(n))
    df = pd.DataFrame(data)
    df.drop(columns="_", inplace=True)
    df.to_csv("spilu_inversion/data3.csv", index=False)


def get_analysis():
    df = pd.read_csv("spilu_inversion/data3.csv").dropna()
    df["n"] = df["n"].round(decimals=-3)

    data = []
    for n in df["n"].unique():
        df_f = df[df["n"] == n]

        spilu_fixed_mean = np.mean(df_f.spilu_preconditioner)
        spilu_fixed_err = sem(df_f.spilu_preconditioner)
        spilu_variable_mean = np.mean(df_f.spilu_solve)
        spilu_variable_err = sem(df_f.spilu_solve)
        inv_fixed_mean = np.mean(df_f.inversion)
        inv_fixed_err = sem(df_f.inversion)
        inv_variable_mean = np.mean(df_f.multiplication)
        inv_variable_err = sem(df_f.multiplication)

        data.append({
            "n": n,
            "spilu_fixed_mean": spilu_fixed_mean,
            "spilu_fixed_err": spilu_fixed_err * 2,
            "spilu_variable_mean": spilu_variable_mean,
            "spilu_variable_err": spilu_variable_err * 2,
            "inv_fixed_mean": inv_fixed_mean,
            "inv_fixed_err": inv_fixed_err * 2,
            "inv_variable_mean": inv_variable_mean,
            "inv_variable_err": inv_variable_err * 2,
        })

    df_out = pd.DataFrame(data)
    df_out.to_csv("spilu_inversion/spilu_analysis3.csv", index=False)


if __name__ == '__main__':
    get_data()
    get_analysis()
