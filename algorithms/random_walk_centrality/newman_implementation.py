import numpy as np
import networkx as nx


# Construct diagonal matrix where D(i,i) = degree of node i
def get_diagonal_matrix_of_node_degrees(g):
    degrees = list(g.degree())  # Get degrees of nodes
    degrees.sort(key=lambda x: int(x[0]))  # Sort by node_id
    degrees = [x[1] for x in degrees]  # Toss away the ids

    D = np.diag(degrees)
    return D


# Remove i-th row and column from a matrix
def remove_row_and_column(matrix, i):
    m = np.delete(matrix, i, axis=0)
    m = np.delete(m, i, axis=1)
    return m


# Algorithm as described in 'A measure of betweenness centrality based on random walks',
# M.E.J. Newman (2004)
def random_walk_centrality(g):
    n = g.number_of_nodes()

    # Calculate Laplacian matrix

    D = get_diagonal_matrix_of_node_degrees(g)
    A = nx.adjacency_matrix(g)
    L = D - A

    # Calculate matrix T

    # Remove last row and column
    M = remove_row_and_column(L, n-1)
    # Invert remaining matrix
    M = M.I
    # Add back the last row and column with all 0s
    M = np.hstack((M, np.zeros((n-1, 1))))
    M = np.vstack((M, np.zeros((1, n))))
    # Convert from matrix to array
    T = np.squeeze(np.asarray(M))

    # Sum up betweenness for each node
    b = [0 for _ in range(n)]  # Betweenness

    for i, j in g.edges:

        # Vi(s,t) = T(i,s) - T(i,t)
        temp = np.array([T[i] for _ in range(n)])  # temp(_,s) = T(i,s)
        Vi = temp.transpose() - temp
        # Vj(s,t) = T(j,s) - T(j,t)
        temp = np.array([T[j] for _ in range(n)])  # temp(_,s) = T(j,s)
        Vj = temp.transpose() - temp

        # B(s,t) = |T(i,s) - T(i,t) - T(j,s) + T(j,t)|
        B = np.abs(Vi - Vj)

        # Remove rows/columns to allow for the condition (i =/= s,t) in equation (9)
        b[i] += np.sum(remove_row_and_column(B, i))
        b[j] += np.sum(remove_row_and_column(B, j))

    b = [x / (2 * (n-1)*(n-2)) for x in b]

    # Return the result as a dictionary mapping (node)->(random walk betweenness centrality)
    return dict(zip(range(n), b))

