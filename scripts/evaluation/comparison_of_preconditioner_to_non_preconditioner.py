import networkx as nx
from scipy.sparse import linalg
import numpy as np
from scripts.timing.Profiler import Profiler
from graphs.random_graphs import get_erdos_renyi
import pandas as pd
from scipy.stats import sem
import scipy


def do_test(n):
    # Create graph
    g = get_erdos_renyi(n=n, average_degree=10)
    # Setup
    n = g.number_of_nodes()
    A = nx.linalg.laplacianmatrix.laplacian_matrix(g).tolil()
    A = A[list(range(1, n)), :]
    A = A[:, list(range(1, n))].tocsc()

    b = np.ones(n-1)

    tm = Profiler()

    preconditioner = linalg.spilu(A)
    tm.mark("spilu_preconditioner")
    for k in range(10):
        x = preconditioner.solve(b)
    tm.mark("spilu_solve")

    A = A.todense()
    tm.mark("_")

    for k in range(10):
        x = scipy.linalg.solve(A, b)
    tm.mark("scipy")

    A = np.array(A)
    tm.mark("_")

    for k in range(10):
        x = np.linalg.solve(A, b)
    tm.mark("numpy")

    data = tm.get_data()
    data["n"] = n
    return data


def get_data():
    data = []
    for n in range(1000, 5001, 1000):
        for _ in range(5):
            data.append(do_test(n))
    df = pd.DataFrame(data)
    df.drop(columns="_", inplace=True)
    df.to_csv("preconditioner/data.csv", index=False)


def get_analysis():
    df = pd.read_csv("preconditioner/data.csv").dropna()
    df["n"] = df["n"].round(decimals=-3)

    data = []
    for n in df["n"].unique():
        df_f = df[df["n"] == n]

        numpy_mean = np.mean((df_f["numpy"]/10))
        numpy_err = sem((df_f["numpy"]/10))
        scipy_mean = np.mean((df_f["scipy"]/10))
        scipy_err = sem((df_f["scipy"] / 10))
        spilu_setup_mean = np.mean(df_f["spilu_preconditioner"])
        spilu_setup_err = sem(df_f["spilu_preconditioner"])
        spilu_variable_mean = np.mean((df_f["spilu_solve"] / 10))
        spilu_variable_err = sem((df_f["spilu_solve"] / 10))

        data.append({
            "n": n,
            "numpy_mean": numpy_mean,
            "numpy_err": 2 * numpy_err,
            "scipy_mean": scipy_mean,
            "scipy_err": 2 * scipy_err,
            "spilu_preconditioner_mean": spilu_setup_mean,
            "spilu_preconditioner_err": 2 * spilu_setup_err,
            "spilu_variable_mean": spilu_variable_mean,
            "spilu_variable_err": 2 * spilu_variable_err,
        })

    df_out = pd.DataFrame(data)
    df_out.to_csv("preconditioner/preconditioner_analysis.csv", index=False)


if __name__ == '__main__':
    #get_data()
    get_analysis()
