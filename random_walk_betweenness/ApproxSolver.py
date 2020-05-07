import numpy as np
import networkx as nx
from random_walk_betweenness.RandomWalkBetweennessSolver import RandomWalkBetweennessSolver
import random
import scipy.sparse.linalg


def source_sink_array(i, j, n):
    a = np.zeros(n)
    a[i] = 1
    a[j] = -1
    return a


class ApproxSolver(RandomWalkBetweennessSolver):
    def __init__(self, epsilon=0.05):
        self.epsilon = epsilon

    # Algorithm as described in 'Centrality Measures Based on Current Flow',
    # Ulrik Brandes and Daniel Fleischer (2005)
    def calculate_on_connected_graph(self, g):
        n = g.number_of_nodes()

        # Initialise constants
        l = 1
        c_star = n / (n - 2)
        k = int(l * np.ceil(((c_star / self.epsilon)**2) * np.log(n)))

        L = nx.linalg.laplacian_matrix(g)[1:, 1:]  # Laplacian of g without first row and column
        spilu = scipy.sparse.linalg.spilu(scipy.sparse.csc_matrix(L))
        v, w = np.array(list(g.edges)).transpose()

        B = np.zeros(n)  # initialise betweennesses to 0
        for _ in range(k):
            # Select s != t uniformly at random
            s, t = random.sample(range(n), 2)

            # Solve Lp = b
            b = source_sink_array(s, t, n)
            p = np.zeros(n)
            p[1:] = spilu.solve(b[1:])

            # Increment betweennesses
            val = np.abs(p[v] - p[w])
            B += np.bincount(v, np.where((v != s) & (v != t), val, 0), minlength=B.size)
            B += np.bincount(w, np.where((w != s) & (w != t), val, 0), minlength=B.size)

        B *= c_star / (2 * k)

        # Return the result as a dictionary mapping
        # [node]->[random walk betweenness centrality]
        return dict(zip(range(n), B))
