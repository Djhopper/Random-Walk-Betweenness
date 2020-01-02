from timeit import default_timer as timer
import numpy as np
import networkx as nx
from scipy.stats import rankdata
from scipy.sparse import linalg, csc_matrix


# Used for timing sections of a function
class TimeMachine:
    def __init__(self):
        self.times = {}
        self.current_time = timer()

    def time(self, name):
        new_time = timer()

        if name in self.times:
            self.times[name] += new_time - self.current_time
        else:
            self.times[name] = new_time - self.current_time

        self.current_time = timer()

    def get_data(self):
        return self.times


def get_diagonal_matrix_of_node_degrees(g):
    degrees = list(g.degree())  # Get degrees of nodes
    degrees.sort(key=lambda x: int(x[0]))  # Sort by node_id
    degrees = [x[1] for x in degrees]  # Toss away the ids

    D = np.diag(degrees)
    return D


# Matrix is known to be symmetric & positive definite
def invert_matrix(M, method="default", new=False):
    if new:
        if method == "default":
            inverse = np.linalg.inv(M.todense())
            return inverse
        elif method == "fancy":
            quit(69)
            n = M.shape[0]
            preconditioner = linalg.spilu(M)
            inverse = np.array([])
            for i in range(n):
                b = np.zeros(n)
                b[i] = 1
                inverse[i] = linalg.cg(A=M, b=b, M=preconditioner)
            return inverse
        else:
            raise NotImplementedError
    else:
        if method == "default":
            return M.I
        else:
            raise NotImplementedError


def remove_row_and_column(matrix, i):
    m = np.delete(matrix, i, axis=0)
    m = np.delete(m, i, axis=1)
    return m

def calc_C(g, n, sparse, new=False):
    if new:
        # Get Laplacian
        tm = TimeMachine()
        M = nx.linalg.laplacianmatrix.laplacian_matrix(g)
        tm.time("0")
        # Remove first row and column
        M = M[list(range(1, n)), :]
        M = M[:, list(range(1, n))]
        tm.time("1")
        # Invert matrix
        M = invert_matrix(M, method="fancy" if sparse else "default")
        tm.time("2")
        # Add back first row and column with all 0s
        M = M.todense() if sparse else M
        tm.time("3")
        T = np.hstack((np.zeros((n - 1, 1)), M))
        T = np.vstack((np.zeros((1, n)), T))
        tm.time("4")
        # Convert from matrix to array
        T = np.squeeze(np.asarray(T))
        tm.time("5")
        import pandas as pd
        print(pd.DataFrame([tm.get_data()]))
        quit()
        return T
    else:
        tm = TimeMachine()
        M = get_diagonal_matrix_of_node_degrees(g) - nx.adjacency_matrix(g)  # Laplacian matrix
        tm.time("1")
        M_2 = remove_row_and_column(M, 0)
        tm.time("2")
        M_3 = invert_matrix(M_2, method="default")
        tm.time("3")
        # Add back column and row with all 0s
        T = np.hstack((np.zeros((n - 1, 1)), M_3))
        T = np.vstack((np.zeros((1, n)), T))
        tm.time("4")
        T = np.squeeze(np.asarray(T))  # Convert matrix to array
        tm.time("5")
        import pandas as pd
        print(pd.DataFrame([tm.get_data()]))
        quit()
        return T


def edge_array(i, j, n):
    a = np.zeros(n)
    a[i] = 1
    a[j] = -1
    return a


def implementation(g):
    tm = TimeMachine()

    n = g.number_of_nodes()
    nrange = np.arange(1, n + 1)
    betweenness = np.zeros(n)

    tm.time("_")

    B = np.vstack((edge_array(i, j, n) for (i, j) in g.edges))

    tm.time("B")

    C = calc_C(g, n, sparse=False)

    tm.time("C")

    BC = B @ C

    tm.time("BC")

    for edge_number, e in enumerate(g.edges):
        v, w = e
        tm.time("1")
        row = BC[edge_number, :]
        tm.time("2")
        pos = rankdata(-row, method="ordinal")
        tm.time("3")

        betweenness[v] += np.sum((nrange - pos).dot(row))
        betweenness[w] += np.sum((n + 1 - nrange - pos).dot(row))
        tm.time("4")

    betweenness = (betweenness - nrange + 1) * (2 / ((n - 1) * (n - 2)))
    ret = dict(zip(range(n), betweenness))
    tm.time("tidy")

    return tm.get_data()


if __name__ == '__main__':
    from graphs.read_write import read_graph
    import pandas as pd
    g = read_graph("erdos_renyi")

    data = pd.DataFrame([implementation(g) for _ in range(1)])
    data.to_csv("results.csv", index=False)
    print(data)
