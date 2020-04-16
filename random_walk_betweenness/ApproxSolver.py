import numpy as np
import networkx as nx
from random_walk_betweenness.helper_functions import construct_diag_node_degrees, remove_row_and_column
from random_walk_betweenness.RandomWalkBetweennessSolver import RandomWalkBetweennessSolver
import random
import scipy


def source_sink_array(i, j, n):
    a = np.zeros(n)
    a[i] = 1
    a[j] = -1
    return a


class ApproxSolver(RandomWalkBetweennessSolver):
    def __init__(self, epsilon=0.05, p=None):
        self.epsilon = epsilon
        self.p = p

    # Algorithm as described in 'Centrality Measures Based on Current Flow',
    # Ulrik Brandes and Daniel Fleischer (2005)
    def calculate_on_connected_graph(self, g):
        n = g.number_of_nodes()
        b = np.zeros(n)

        if self.p is None:
            l = 1
        else:
            l = np.log(2/self.p) / (2 * np.log(n))

        c_star = n / (n - 2)
        k = int(l * np.ceil(((c_star / self.epsilon)**2) * np.log(n)))

        L = remove_row_and_column(construct_diag_node_degrees(g) - nx.adjacency_matrix(g), 0)
        spilu = scipy.sparse.linalg.spilu(scipy.sparse.csc_matrix(L))
        edges = np.array(list(g.edges)).transpose()

        for _ in range(k):
            s = random.randint(0, n-1)
            t = random.randint(0, n-2)
            t += 1 if t >= s else 0

            p = spilu.solve(source_sink_array(s, t, n)[1:])
            p = np.insert(p, 0, 0)

            val = np.abs(p[edges[0]] - p[edges[1]])
            b[edges[0]] += np.where((edges[0] == s) | (edges[0] == t), 0, val)
            b[edges[1]] += np.where((edges[1] == s) | (edges[1] == t), 0, val)

        b *= c_star / (2 * k)
        # Return the result as a dictionary mapping (node)->(random walk betweenness centrality)
        return dict(zip(range(n), b))





if __name__ == '__main__':
    from scripts.vis.draw_graph import draw_graph
    import matplotlib.pyplot as plt
    from random_walk_betweenness.RandomWalkBetweennessSolver import RandomWalkBetweennessSolver
    from random_walk_betweenness.NXApproxSolver import NXApproxSolver
    g = nx.Graph()
    g.add_nodes_from(['A', 'B', 'C', 'D', 'E'])
    g.add_edges_from([['A', 'B'], ['A', 'D'], ['B', 'C'], ['C', 'D'], ['B', 'E'], ['D', 'E']])

    res = NXApproxSolver().calculate(g)
    print(res)
    print(RandomWalkBetweennessSolver().calculate(g))
    draw_graph(g, labels=True)
    plt.show()
