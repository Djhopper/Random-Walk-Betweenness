import numpy as np
import networkx as nx


# Remove i-th row and column from a matrix
def remove_row_and_column(matrix, i):
    m = np.delete(matrix, i, axis=0)
    m = np.delete(m, i, axis=1)
    return m


# Construct the matrix T from 'A measure of betweenness centrality based on random walks' by # M.E.J. Newman (2004).
# It is referred to as C in 'Centrality Measures Based on Current Flow' by Ulrik Brandes and Daniel Fleischer (2005).
def construct_newman_T_matrix(g):
    n = g.number_of_nodes()
    # Get laplacian of g
    L = nx.linalg.laplacian_matrix(g).todense()
    # Remove last row and column
    M = remove_row_and_column(L, n - 1)
    # Invert remaining matrix
    M = M.I
    # Add back the last row and column with all 0s
    M = np.hstack((M, np.zeros((n - 1, 1))))
    M = np.vstack((M, np.zeros((1, n))))
    # Convert from matrix to array
    T = np.asarray(M)

    return T
