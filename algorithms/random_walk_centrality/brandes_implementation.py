import numpy as np
import networkx as nx
from scipy.stats import rankdata


def get_diagonal_matrix_of_node_degrees(g):
    degrees = list(g.degree())  # Get degrees of nodes
    degrees.sort(key=lambda x: int(x[0]))  # Sort by node_id
    degrees = [x[1] for x in degrees]  # Toss away the ids

    D = np.diag(degrees)
    return D


# Matrix is known to be symmetric & positive definite
def invert_matrix(M, method="default"):
    if method == "default":
        return M.I
    else:
        raise NotImplementedError


def remove_row_and_column(matrix, i):
    m = np.delete(matrix, i, axis=0)
    m = np.delete(m, i, axis=1)
    return m


def calc_C(g, n):
    D = get_diagonal_matrix_of_node_degrees(g)
    A = nx.adjacency_matrix(g)

    M = D - A  # Laplacian matrix

    M_2 = remove_row_and_column(M, 0)
    M_3 = invert_matrix(M_2, method="default")

    # Add back column and row with all 0s
    T = np.hstack((np.zeros((n - 1, 1)), M_3))
    T = np.vstack((np.zeros((1, n)), T))

    T = np.squeeze(np.asarray(T))  # Convert matrix to array
    return T


# Algorithm as described in 'Centrality Measures Based on Current Flow',
# Ulrik Brandes and Daniel Fleischer (2005)
def random_walk_centrality(g):
    n = g.number_of_nodes()
    b = [0 for _ in range(n)]

    B = [[1 if i == v else -1 if j == v else 0
         for (i, j) in g.edges]
         for v in g.nodes]
    B = np.array(B)

    C = calc_C(g, n)

    BC = np.matmul(B.transpose(), C.transpose())

    for edge_number, e in enumerate(g.edges):
        v, w = e
        row = BC[edge_number, :]
        pos = rankdata(-row, method="ordinal")

        for i in range(1, n+1):
            posevi = pos[i-1]
            fevi = row[i-1]
            b[v] += (i - posevi) * fevi
            b[w] += (n + 1 - i - posevi) * fevi

    for i in range(1, n+1):
        b[i-1] = (b[i-1] - i + 1) * (2 / ((n-1) * (n-2)))

    return dict(zip(range(n), b))


# TODO speed up the matrix inversion by using the alternative method given by Brande et al (2005)


if __name__ == '__main__':
    from graphs.read_write import read_graph
    from algorithms.random_walk_centrality.nx_implementation import random_walk_centrality as nx_impl

    g = read_graph("bull_graph")

    print(random_walk_centrality(g))

    print(nx_impl(g))
