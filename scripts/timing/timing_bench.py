from timeit import default_timer as timer
import numpy as np
import networkx as nx
from random_walk_betweenness.helper_functions import construct_diag_node_degrees, remove_row_and_column
from random_walk_betweenness.RandomWalkBetweennessSolver import RandomWalkBetweennessSolver
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


def calculate_on_connected_graph(self, g):
    tm = TimeMachine()
    n = g.number_of_nodes()

    # Initialise constants
    l = 1
    c_star = n / (n - 2)
    k = int(l * np.ceil(((c_star / self.epsilon) ** 2) * np.log(n)))
    tm.time("_")

    L = nx.linalg.laplacian_matrix(g)[1:, 1:].todense()  # Laplacian of g without first row and column
    tm.time("laplacian")
    spilu = scipy.sparse.linalg.spilu(scipy.sparse.csc_matrix(L))
    v, w = np.array(list(g.edges)).transpose()

    B = np.zeros(n)  # initialise betweennesses to 0
    for _ in range(k):
        # Select s != t uniformly at random
        s = random.randint(0, n - 1)
        t = random.randint(0, n - 2)
        t += 1 if t >= s else 0

        # Solve Lp = b
        b = source_sink_array(s, t, n)
        p = np.zeros(n)
        p[1:] = spilu.solve(b[1:])

        # Increment betweennesses
        val = np.abs(p[v] - p[w])
        np.add.at(B, v, np.where((v != s) & (v != t), val, 0))
        np.add.at(B, w, np.where((w != s) & (w != t), val, 0))

    B *= c_star / (2 * k)
    # Return the result as a dictionary mapping (node)->(random walk betweenness centrality)
    return dict(zip(range(n), B))


if __name__ == '__main__':
    from graphs.random_graphs import get_erdos_renyi
    g = get_erdos_renyi(10000, 10)
    start = timer()
    print(calculate_on_connected_graph(g, 0.05))
    end = timer()
    print(end-start)
