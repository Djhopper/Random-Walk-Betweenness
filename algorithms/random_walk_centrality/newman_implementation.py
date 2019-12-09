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


# V(i,s,t) = T(i,s) - T(i,t)
def calculate_V(T, n):
    R = np.array([T for _ in range(n)])  # R(z,x,y) = T(x,y)
    Y = np.swapaxes(R, 0, 1)             # Y(i,s,t) = T(i,t)
    X = np.swapaxes(Y, 1, 2)             # X(i,s,t) = T(i,s)

    V = X - Y
    return V


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
    M_3 = invert_matrix(M_2, method="default")

    # Add back column and row with all 0s
    T = np.hstack((M_3, np.zeros((n-1, 1))))
    T = np.vstack((T, np.zeros((1, n))))

    V = calculate_V(T, n)

    # Sum everything up
    b = [
        sum(
            abs(V[i, s, t] - V[j, s, t]) if i not in (s, t) else 0
            for j in g.neighbors(i)
            for s in range(n)
            for t in range(s+1, n)
        ) / ((n-1) * (n-2))
        for i in range(n)
    ]

    return dict(zip(np.arange(n), b))


# TODO turn calculation of b into a bunch of vector shit.
# TODO Add alternative method that uses less memory (storing all of V at once is O(n^3) = :((((
# TODO Make lots of improvements :))
# TODO speed up the matrix inversion by using the alternative method given by Brande et al (2005)
