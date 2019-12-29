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


def edge_array(i, j, n):
    a = np.zeros(n)
    a[i] = 1
    a[j] = -1
    return a


# Algorithm as described in 'Centrality Measures Based on Current Flow',
# Ulrik Brandes and Daniel Fleischer (2005)
def random_walk_centrality(g):
    n = g.number_of_nodes()
    nrange = np.arange(1, n+1)
    betweenness = np.zeros(n)

    B = np.vstack((edge_array(i, j, n) for (i, j) in g.edges))

    C = calc_C(g, n)

    BC = B @ C

    for edge_number, e in enumerate(g.edges):
        v, w = e
        row = BC[edge_number, :]
        pos = rankdata(-row, method="ordinal")

        betweenness[v] += np.sum((nrange - pos).dot(row))
        betweenness[w] += np.sum((n + 1 - nrange - pos).dot(row))

    betweenness = (betweenness - nrange + 1) * (2 / ((n-1) * (n-2)))

    return dict(zip(range(n), betweenness))


# TODO speed up the matrix inversion by using the alternative method given by Brande et al (2005)


if __name__ == '__main__':
    from graphs.read_write import read_graph
    from algorithms.random_walk_centrality.nx_implementation import random_walk_centrality as nx_impl

    g = read_graph("bull_graph")

    print(random_walk_centrality(g))

    print(nx_impl(g))
