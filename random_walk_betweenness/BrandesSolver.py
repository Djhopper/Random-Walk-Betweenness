import numpy as np
from scipy.stats import rankdata
from random_walk_betweenness.helper_functions import construct_newman_T_matrix
from random_walk_betweenness.RandomWalkBetweennessSolver import RandomWalkBetweennessSolver


# Constructs the (n by m) matrix B where:
# B(v,e) =  1, if e = (v,w)
#          -1, if e = (w,v)
#           0, otherwise
def construct_B(g, n):
    # Helper function defines a single row of the matrix
    def row(i, j):
        a = np.zeros(n)
        a[i] = 1
        a[j] = -1
        return a

    return np.vstack((row(i, j) for (i, j) in g.edges))


class BrandesSolver(RandomWalkBetweennessSolver):
    # Algorithm as described in 'Centrality Measures Based on Current Flow',
    # Ulrik Brandes and Daniel Fleischer (2005)
    def calculate_on_connected_graph(self, g):
        n = g.number_of_nodes()
        v = np.arange(n)

        B = construct_B(g, n)
        C = construct_newman_T_matrix(g)  # Construct C as given in equation (1)
        BC = np.matmul(B, C)

        b = np.zeros(n)  # Initialise array of betweennesses
        for edge_number, e in enumerate(g.edges):
            source, target = e
            row = BC[edge_number, :]  # row is notated Fe● in the paper
            pos = rankdata(-row, method="ordinal")

            b[source] += np.sum((v + 1 - pos).dot(row))
            b[target] += np.sum((n - v - pos).dot(row))

        b = (b - v) * (2 / ((n-1) * (n-2)))

        # Return the result as a dictionary mapping (node)->(random walk betweenness centrality)
        return dict(zip(range(n), b))
