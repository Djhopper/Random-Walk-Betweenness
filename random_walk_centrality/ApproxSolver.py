import numpy as np
import networkx as nx
from random_walk_centrality.helper_functions import construct_diag_node_degrees, remove_row_and_column
from random_walk_centrality.RandomWalkBetweennessCentralitySolver import RandomWalkBetweennessCentralitySolver
from networkx.algorithms.centrality import approximate_current_flow_betweenness_centrality
import random
import scipy


def source_sink_array(i, j, n):
    a = np.zeros(n)
    a[i] = 1
    a[j] = -1
    return a


class ApproxSolver(RandomWalkBetweennessCentralitySolver):
    def __init__(self, epsilon=0.05, p=0.05):
        self.epsilon = epsilon
        self.p = p

    # Algorithm as described in 'Centrality Measures Based on Current Flow',
    # Ulrik Brandes and Daniel Fleischer (2005)
    def calculate_on_connected_graph(self, g):
        n = g.number_of_nodes()
        b = np.zeros(n)

        l = np.log(2/self.p) / (2 * np.log(n))
        c_star = n / (n - 2)
        k = int(l * np.ceil(((c_star / self.epsilon)**2) * np.log(n)))

        L = remove_row_and_column(construct_diag_node_degrees(g) - nx.adjacency_matrix(g), 0)
        spilu = scipy.sparse.linalg.spilu(scipy.sparse.csc_matrix(L))

        for _ in range(k):
            s = random.randint(0, n-1)
            t = random.randint(0, n-2)
            t += 1 if t >= s else 0

            p = spilu.solve(source_sink_array(s, t, n)[1:])
            p = np.insert(p, 0, 0)

            for (v, w) in g.edges:
                val = abs(p[v] - p[w])
                if v not in (s, t):
                    b[v] += val
                if w not in (s, t):
                    b[w] += val

        b *= c_star / (2 * k)
        # Return the result as a dictionary mapping (node)->(random walk betweenness centrality)
        return dict(zip(range(n), b))
