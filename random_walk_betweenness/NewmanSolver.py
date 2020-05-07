import numpy as np
from random_walk_betweenness.helper_functions import construct_newman_T_matrix
from random_walk_betweenness.RandomWalkBetweennessSolver \
    import RandomWalkBetweennessSolver
from itertools import combinations


class NewmanSolver(RandomWalkBetweennessSolver):
    # Implements algorithm described in 'A measure of betweenness
    # centrality based on random walks', M.E.J. Newman (2004)
    def calculate_on_connected_graph(self, g):
        n = g.number_of_nodes()

        T = construct_newman_T_matrix(g)
        b = np.zeros(n)  # Initialise array of betweennesses
        s, t = np.fromiter(
            combinations(np.arange(n), 2), dtype='i,i'
        ).view(np.int).reshape(-1, 2).transpose()  # Find all pairs s<t

        for v, w in g.edges:
            temp = np.abs(T[v, s] - T[v, t] - T[w, s] + T[w, t])

            # Exclude values where (v =/= s,t)
            b[v] += np.sum(temp[(s != v) & (t != v)])
            b[w] += np.sum(temp[(s != w) & (t != w)])

        b /= ((n-1)*(n-2))  # normalise

        # Return the result as a dictionary mapping
        # [node]->[random walk betweenness]
        return dict(zip(range(n), b))
