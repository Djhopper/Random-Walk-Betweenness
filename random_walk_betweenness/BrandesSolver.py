import numpy as np
import networkx as nx
from scipy.stats import rankdata
from scipy.sparse import linalg
from random_walk_betweenness.helper_functions import construct_diag_node_degrees, remove_row_and_column
from random_walk_betweenness.RandomWalkBetweennessSolver import RandomWalkBetweennessSolver


# B(v,e) = 1 if e = (v,w), -1 if e = (w, v), 0 otherwise
def construct_B(g, n):
    # Helper function defines a single row of the matrix
    def edge_array(i, j):
        a = np.zeros(n)
        a[i] = 1
        a[j] = -1
        return a

    return np.vstack((edge_array(i, j) for (i, j) in g.edges))


# C as given in equation (1)
def construct_C(g, n, sparse):
    # TODO try incomplete cholesky decomposition
    if sparse:  # Make use of sparse matrix methods
        # Get Laplacian
        M = nx.linalg.laplacianmatrix.laplacian_matrix(g).tolil()
        # Remove first row and column
        M = M[list(range(1, n)), :]
        M = M[:, list(range(1, n))].tocsc()
        # Invert matrix
        I = linalg.spilu(M).solve(np.identity(n-1))
        # Add back column and row with all 0s
        T = np.hstack((np.zeros((n - 1, 1)), I))
        T = np.vstack((np.zeros((1, n)), T))
        # Convert from matrix to array
        T = np.squeeze(np.asarray(T))
        return T

    else:
        # Get Laplacian
        M = construct_diag_node_degrees(g) - nx.adjacency_matrix(g)
        # Remove first row and column
        M = remove_row_and_column(M, 0)
        # Invert matrix
        I = M.I
        # Add back first column and row with all 0s
        T = np.hstack((np.zeros((n - 1, 1)), I))
        T = np.vstack((np.zeros((1, n)), T))
        # Convert from matrix to array
        T = np.squeeze(np.asarray(T))
        return T


class BrandesSolver(RandomWalkBetweennessSolver):
    def __init__(self):
        self.sparse = False

    # Algorithm as described in 'Centrality Measures Based on Current Flow',
    # Ulrik Brandes and Daniel Fleischer (2005)
    def calculate_on_connected_graph(self, g):
        n = g.number_of_nodes()
        nrange = np.arange(1, n + 1)

        # B(v,e) = 1 if e = (v,w), -1 if e = (w, v), 0 otherwise
        B = construct_B(g, n)

        # C as given in equation (1)
        C = construct_C(g, n, sparse=self.sparse)

        BC = np.matmul(B, C)

        b = np.zeros(n)  # Initialise array of betweennesses
        for edge_number, e in enumerate(g.edges):
            v, w = e
            row = BC[edge_number, :]  # row = Fe● in the paper
            pos = rankdata(-row, method="ordinal")

            # Do summation using numpy rather than a for loop - faster
            b[v] += np.sum((nrange - pos).dot(row))
            b[w] += np.sum((n + 1 - nrange - pos).dot(row))

        b = (b - nrange + 1) * (2 / ((n-1) * (n-2)))

        # Return the result as a dictionary mapping (node)->(random walk betweenness centrality)
        return dict(zip(range(n), b))


class BrandesSolverSparse(BrandesSolver):
    def __init__(self):
        super(BrandesSolverSparse, self).__init__()
        self.sparse = True


class BrandesSolverDense(BrandesSolver):
    def __init__(self):
        super(BrandesSolverDense, self).__init__()
        self.sparse = False
