import numpy as np
import networkx as nx


def get_diagonal_matrix_of_node_degrees(g):
    degrees = list(g.degree())  # Get degrees of nodes
    degrees.sort(key=lambda x: int(x[0]))  # Sort by node_id
    degrees = [x[1] for x in degrees]  # Pull out just the degrees without the ids

    D = np.diag(degrees)
    return D


def random_walk_centrality(g):
    D = get_diagonal_matrix_of_node_degrees(g)
    A = nx.adjacency_matrix(g)

    M = D - A

    # Remove last column and row
    n = M.shape[0]
    M_missing_a_row = np.delete(M, n-1, axis=0)
    M_missing_a_row = np.delete(M_missing_a_row, n-1, axis=1)

    # Invert matrix
    inverse = M_missing_a_row.I
    # Add back column and row with all 0s
    T = np.hstack((inverse, np.zeros((n-1, 1))))
    T = np.vstack((T, np.zeros((1, n))))

    b = [0 for _ in range(n)]
    for s in range(n):
        for t in range(s+1, n):
            V = [T[i, s] - T[i, t] for i in range(n)]

            I = [0.5 *
                 sum(A[i, j] * abs(V[i] - V[j]) for j in range(n))
                 for i in range(n)]

            I[s] = I[t] = 0

            for i in range(n):
                b[i] += I[i]

    for i in range(n):
        b[i] /= (0.5 * (n-1) * (n-2))

    return dict((i, x) for i, x in enumerate(b))


if __name__ == '__main__':
    from graphs.read_write import read_graph
    from networkx.generators.random_graphs import erdos_renyi_graph
    #g = read_graph("house_graph")
    g = erdos_renyi_graph(20, 0.1)
    g = read_graph("erdos_renyi")
    print("My version:", random_walk_centrality(g))

    from algorithms.random_walk_centrality.random_walk_centrality import random_walk_centrality as default_impl
    print("Other version:", dict((x, default_impl(g)[x]) for x in sorted(default_impl(g))))
