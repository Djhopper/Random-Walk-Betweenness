from timeit import default_timer as timer
import numpy as np
import networkx as nx


# Used for timing sections of a function
class TimeMachine:
    def __init__(self):
        self.times = []
        self.current_time = timer()

    def time(self, name):
        new_time = timer()
        self.times.append((name, new_time - self.current_time))
        self.current_time = new_time

    def get_data(self):
        return dict(self.times)


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


def newman_implementation(g):
    tm = TimeMachine()
    n = g.number_of_nodes()

    D = get_diagonal_matrix_of_node_degrees(g)
    A = nx.adjacency_matrix(g)

    M = D - A

    # Remove last column and row
    M_2 = np.delete(M, n - 1, axis=0)
    M_2 = np.delete(M_2, n - 1, axis=1)

    # Invert matrix
    M_3 = invert_matrix(M_2, method="default")

    # Add back column and row with all 0s
    T = np.hstack((M_3, np.zeros((n - 1, 1))))
    T = np.vstack((T, np.zeros((1, n))))

    tm.time("Calculate T")

    b = [0 for _ in range(n)]
    T = np.squeeze(np.asarray(T))

    tm.time("Squeeze")
    for i, j in g.edges:
        temp = np.array([T[i] for _ in range(n)])
        Vi = temp.transpose() - temp
        temp = np.array([T[j] for _ in range(n)])
        Vj = temp.transpose() - temp
        tm.time("Edge " + str(i) + "->" + str(j) + " setup")
        for s in range(n):
            for t in range(s+1, n):
                val = abs(Vi[s, t] - Vj[s, t])
                if i not in (s, t):
                    b[i] += val
                if j not in (s, t):
                    b[j] += val
        tm.time("Edge " + str(i) + "->" + str(j) + " summation")
    b = [x / ((n - 1) * (n - 2)) for x in b]

    ret = dict(zip(range(n), b))

    tm.time("Tidy up")
    return tm.get_data()


if __name__ == '__main__':
    from graphs.read_write import read_graph
    import pandas as pd
    g = read_graph("erdos_renyi")

    data = pd.DataFrame([newman_implementation(g) for _ in range(1)])
    data.to_csv("results.csv", index=False)
    print(data)
