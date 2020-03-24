import networkx as nx
from scipy.sparse import linalg
import numpy as np
from scripts.timing_bench import TimeMachine
from graphs.random_graphs import get_erdos_renyi


'''
This shows that partial LU decomposition method, as implemented in the scipy.sparse.linalg.spilu is about 3 times slower
than the builtin numpy method of inverting the matrix, even for very large n. Therefore it is unsuitable for speeding up 
matrix inversion.
'''
if __name__ == '__main__':
    # Create graph
    g = get_erdos_renyi(n=10000, average_degree=10)
    # Setup (create matrix that needs to be inverted)
    n = g.number_of_nodes()
    M = nx.linalg.laplacianmatrix.laplacian_matrix(g).tolil()
    M = M[list(range(1, n)), :]
    M = M[:, list(range(1, n))].tocsc()

    tm = TimeMachine()
    # Do partial LU decomposition method
    inverse = linalg.spilu(M).solve(np.identity(n - 1))
    tm.time("fancy method")

    M = M.todense()
    tm.time("_")

    # Do standard inversion
    inverse = M.I
    tm.time("normal method")

    print(tm.get_data())
