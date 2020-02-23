from timeit import default_timer as timer
import numpy as np
import networkx as nx
from random_walk_centrality.helper_functions import construct_diag_node_degrees, remove_row_and_column
from random_walk_centrality.RandomWalkBetweennessCentralitySolver import RandomWalkBetweennessCentralitySolver
import random
import scipy
import pandas as pd


def source_sink_array(i, j, n):
    a = np.zeros(n)
    a[i] = 1
    a[j] = -1
    return a


# Used for timing sections of a function
class TimeMachine:
    def __init__(self):
        self.times = {}
        self.current_time = timer()

    def time(self, name):
        new_time = timer()

        if name in self.times:
            self.times[name] += new_time - self.current_time
        else:
            self.times[name] = new_time - self.current_time

        self.current_time = timer()

    def get_data(self):
        return self.times


def calculate_on_connected_graph(g, p, epsilon):
    tm = TimeMachine()
    n = g.number_of_nodes()
    b = np.zeros(n)

    l = np.log(2/p) / (2 * np.log(n))
    c_star = n / (n - 2)
    k = int(l * np.ceil(((c_star / epsilon)**2) * np.log(n)))
    tm.time("_")
    L = remove_row_and_column(construct_diag_node_degrees(g) - nx.adjacency_matrix(g), 0)
    tm.time("_")
    spilu = scipy.sparse.linalg.spilu(scipy.sparse.csc_matrix(L))
    tm.time("_")

    for _ in range(k):
        s = random.randint(0, n-1)
        t = random.randint(0, n-2)
        t += 1 if t >= s else 0
        tm.time("_")

        p = spilu.solve(source_sink_array(s, t, n)[1:])
        p = np.insert(p, 0, 0)

        tm.time("_")

        for (v, w) in g.edges:
            val = abs(p[v] - p[w])
            tm.time("abs(a-b)")
            if v != s and v != t:
                b[v] += val
            tm.time("1")
            if w not in (s, t):
                b[w] += val
            tm.time("2")

    b *= c_star / (2 * k)
    result = dict(zip(range(n), b))
    tm.time("_")
    return tm.get_data()


if __name__ == '__main__':
    from graphs.read_write import read_graph

    n = 10000


    g = read_graph("erdos_renyi")
    start = timer()
    print(calculate_on_connected_graph(g, 0.05, 0.05))
    end = timer()
    print(end-start)
