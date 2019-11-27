import numpy as np
import networkx as nx


def get_diagonal_matrix_of_node_degrees(g):
    degrees = list(g.degree())  # Get degrees of nodes
    degrees.sort(key=lambda x: int(x[0]))  # Sort by node_id
    degrees = [x[1] for x in degrees]  # Pull out just the degrees without the ids

    D = np.diag(degrees)
    return D


def invert_matrix(M, method="default"):
    if method == "default":
        return M.I
    else:
        raise NotImplementedError


# Algorithm as described in 'A measure of betweenness centrality based on random walks',
# M.E.J. Newman (2004)
def random_walk_centrality(g):
    n = g.number_of_nodes()

    D = get_diagonal_matrix_of_node_degrees(g)
    A = nx.adjacency_matrix(g)
    M = D - A

    # Remove last column and row
    M_2 = np.delete(M, n-1, axis=0)
    M_2 = np.delete(M_2, n-1, axis=1)

    # Invert matrix
    inverse = invert_matrix(M_2, method="default")

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
