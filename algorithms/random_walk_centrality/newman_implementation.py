import numpy as np
import networkx as nx


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


# Algorithm as described in 'A measure of betweenness centrality based on random walks',
# M.E.J. Newman (2004)
def random_walk_centrality(g):
    n = g.number_of_nodes()

    D = get_diagonal_matrix_of_node_degrees(g)
    A = nx.adjacency_matrix(g)

    M = D - A

    M_2 = remove_row_and_column(M, n-1)
    M_3 = invert_matrix(M_2, method="default")

    # Add back column and row with all 0s
    T = np.hstack((M_3, np.zeros((n-1, 1))))
    T = np.vstack((T, np.zeros((1, n))))

    T = np.squeeze(np.asarray(T))  # Convert matrix to array

    b = [0 for _ in range(n)]
    for i, j in g.edges:
        temp = np.array([T[i] for _ in range(n)])
        Vi = temp.transpose() - temp
        temp = np.array([T[j] for _ in range(n)])
        Vj = temp.transpose() - temp

        B = np.abs(Vi - Vj)
        b[i] += np.sum(remove_row_and_column(B, i))
        b[j] += np.sum(remove_row_and_column(B, j))

    b = [x / (2 * (n-1)*(n-2)) for x in b]

    return dict(zip(range(n), b))


# TODO speed up the matrix inversion by using the alternative method given by Brande et al (2005)


if __name__ == '__main__':
    from graphs.read_write import read_graph
    from algorithms.random_walk_centrality.nx_implementation import random_walk_centrality as nx_impl

    g = read_graph("bull_graph")

    print(random_walk_centrality(g))

    print(nx_impl(g))
