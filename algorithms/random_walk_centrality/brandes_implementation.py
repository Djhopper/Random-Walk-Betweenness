import numpy as np
import networkx as nx
from scipy.stats import rankdata
from scipy.sparse import linalg, identity
from tests.timing_bench import TimeMachine


def get_diagonal_matrix_of_node_degrees(g):
    degrees = list(g.degree())  # Get degrees of nodes
    degrees.sort(key=lambda x: int(x[0]))  # Sort by node_id
    degrees = [x[1] for x in degrees]  # Toss away the ids

    D = np.diag(degrees)
    return D


def remove_row_and_column(matrix, i):
    m = np.delete(matrix, i, axis=0)
    m = np.delete(m, i, axis=1)
    return m


def calc_C(g, n, sparse):
    if sparse:
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
        M = get_diagonal_matrix_of_node_degrees(g) - nx.adjacency_matrix(g)
        # Remove first row and column
        M = remove_row_and_column(M, 0)
        # Invert matrix
        I = M.I
        # Add back column and row with all 0s
        T = np.hstack((np.zeros((n - 1, 1)), I))
        T = np.vstack((np.zeros((1, n)), T))
        # Convert from matrix to array
        T = np.squeeze(np.asarray(T))
        return T


def edge_array(i, j, n):
    a = np.zeros(n)
    a[i] = 1
    a[j] = -1
    return a


def matrix_multiplication(A, B):
    return np.matmul(A, B)
    # Alternatives (slightly slower?):
    # return A @ B
    # return np.dot(A, B)


# Algorithm as described in 'Centrality Measures Based on Current Flow',
# Ulrik Brandes and Daniel Fleischer (2005)
def random_walk_centrality(g, sparse=True):
    n = g.number_of_nodes()
    nrange = np.arange(1, n+1)
    betweenness = np.zeros(n)

    B = np.vstack((edge_array(i, j, n) for (i, j) in g.edges))

    C = calc_C(g, n, sparse=sparse)

    BC = matrix_multiplication(B, C)

    for edge_number, e in enumerate(g.edges):
        v, w = e
        row = BC[edge_number, :]
        pos = rankdata(-row, method="ordinal")

        betweenness[v] += np.sum((nrange - pos).dot(row))
        betweenness[w] += np.sum((n + 1 - nrange - pos).dot(row))

    betweenness = (betweenness - nrange + 1) * (2 / ((n-1) * (n-2)))

    return dict(zip(range(n), betweenness))


if __name__ == '__main__':
    from graphs.read_write import read_graph
    from algorithms.random_walk_centrality.nx_implementation import random_walk_centrality as nx_impl
    g = read_graph("erdos_renyi")

    tm = TimeMachine()
    print(random_walk_centrality(g, sparse=False))
    tm.time("old version")
    print(random_walk_centrality(g, sparse=True))
    tm.time("sparse version")

    print(tm.get_data())
    #print(nx_impl(g))
