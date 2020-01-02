from networkx.generators.random_graphs import erdos_renyi_graph
import networkx as nx
from tests.timing_bench import TimeMachine
from scipy.sparse import linalg
import numpy as np


'''
This shows that partial LU decomposition method, as implemented in the scipy.sparse.linalg.spilu is about 3 times slower
than the builtin numpy method of inverting the matrix, even for very large n. Therefore it is unsuitable for speeding up 
matrix inversion.
'''
if __name__ == '__main__':
    # Create graph
    g = erdos_renyi_graph(10000, 10/10000)
    Gcc = g.subgraph(sorted(nx.connected_components(g), key=len, reverse=True)[0])
    # Setup (create matrix that needs to be inverted)
    n = g.number_of_nodes()
    M = nx.linalg.laplacianmatrix.laplacian_matrix(g).tolil()
    M = M[list(range(1, n)), :]
    M = M[:, list(range(1, n))].tocsc()

    tm = TimeMachine()
    # Do partial LU decomposition
    inverse = linalg.spilu(M).solve(np.identity(n - 1))
    tm.time("fancy method")
    print(tm.times)

    M = M.todense()
    tm.time("densify")

    # Do invert
    inverse = M.I
    tm.time("normal method")

    print(tm.get_data())
