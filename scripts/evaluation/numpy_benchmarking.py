import numpy as np
from scripts.timing.Profiler import Profiler
import pandas as pd
from scipy.stats import sem


def testAbs(n):
    x = [-10 for _ in range(n)]
    y = np.array(x)

    tm = Profiler()
    x1 = [abs(i) for i in x]
    tm.mark("builtin")
    y1 = np.abs(y)
    tm.mark("numpy")
    return tm


def testSum(n):
    x = [2 for _ in range(n)]
    y = np.array(x)

    tm = Profiler()
    x1 = sum(x)
    tm.mark("builtin")
    y1 = np.sum(y)
    tm.mark("numpy")
    return tm


def testWhere(n):
    x = [2 for _ in range(n)]
    y = np.array(x)

    tm = Profiler()
    x1 = [i*i if i > 0 else 0 for i in x]
    tm.mark("builtin")
    y1 = np.where(y > 0, y*y, 0)
    tm.mark("numpy")
    return tm


def getData(ns, trials):
    data = []
    for n in ns:
        for index in range(trials):
            abs_data = testAbs(n[0]).get_data()
            abs_data.update({"function": "abs", "n": n[0], "i": index})
            data.append(abs_data)
            sum_data = testSum(n[1]).get_data()
            sum_data.update({"function": "sum", "n": n[1], "i": index})
            data.append(sum_data)
            where_data = testSum(n[2]).get_data()
            where_data.update({"function": "where", "n": n[2], "i": index})
            data.append(where_data)

    df = pd.DataFrame(data)
    df.to_csv("numpy_benchmarking/numpy_benchmarking_data.csv", index=False)
    return df


def getAnalysis():
    df = pd.read_csv("numpy_benchmarking/numpy_benchmarking_data.csv")

    for function in df["function"].unique():
        data = []
        for n in df[df["function"] == function]["n"].unique():
            df_filtered = df[(df["function"] == function) & (df["n"] == n)]
            for version in ["builtin", "numpy"]:
                err = sem(df_filtered[version])
                mean = df_filtered[version].mean()
                data.append({
                    "version": version,
                    "n": n,
                    "mean": mean,
                    "err": 2*err,
                })
        df_out = pd.DataFrame(data)
        df_out.to_csv("numpy_benchmarking/numpy_benchmarking_analysis_"+function+".csv", index=False)


if __name__ == '__main__':
    ns = zip(
        range(10**6, 10**7 + 1, 10**6),
        range(10**7, 10**8 + 1, 10**7),
        range(10**7, 10**8 + 1, 10**7),
    )
    trials = 10

    getData(ns, trials)
    getAnalysis()
