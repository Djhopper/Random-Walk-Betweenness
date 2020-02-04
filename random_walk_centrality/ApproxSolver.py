import numpy as np
import networkx as nx
from random_walk_centrality.helper_functions import construct_diag_node_degrees, remove_row_and_column
from random_walk_centrality.RandomWalkBetweennessCentralitySolver import RandomWalkBetweennessCentralitySolver
import random


def source_sink_array(i, j, n):
    a = np.zeros(n)
    if i != n:
        a[i] = 1
    if j != n:
        a[j] = -1
    return a


class ApproxSolver(RandomWalkBetweennessCentralitySolver):
    def __init__(self, epsilon=0.01):
        self.epsilon = epsilon

    # Algorithm as described in 'Centrality Measures Based on Current Flow',
    # Ulrik Brandes and Daniel Fleischer (2005)
    def calculate_on_connected_graph(self, g):
        n = g.number_of_nodes()
        b = np.zeros(n)

        l = 1  # adjust to change probability of approximation being within epsilon
        print("p =", 2 / (n ** (2 * l)))
        c_star = n / (n - 2)
        k = int(l * ((c_star / self.epsilon) ** 2 * np.log(n)))

        L = remove_row_and_column(construct_diag_node_degrees(g) - nx.adjacency_matrix(g), 0)

        for _ in range(k):
            s = random.randint(0, n-1)
            t = random.randint(0, n-2)
            t += 1 if t >= s else 0
            s, t = random.choice([(x, y) for x in range(n) for y in range(n) if x != y])

            # TODO speed this up using CG method and a preconditioner
            p = np.linalg.solve(L, source_sink_array(s, t, n)[1:])
            p = np.insert(p, 0, 0)

            # TODO vectorise this
            for v in range(n):
                for (_, w) in g.edges(v):
                    if v not in (s, t):
                        b[v] += abs(p[v] - p[w])

        b *= c_star / (2 * k)
        # Return the result as a dictionary mapping (node)->(random walk betweenness centrality)
        return dict(zip(range(n), b))
