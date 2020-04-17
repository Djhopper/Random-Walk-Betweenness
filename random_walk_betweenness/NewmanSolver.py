import numpy as np
from random_walk_betweenness.helper_functions import construct_newman_T_matrix
from random_walk_betweenness.RandomWalkBetweennessSolver import RandomWalkBetweennessSolver
from itertools import combinations


class NewmanSolver(RandomWalkBetweennessSolver):
    # Implements algorithm described in 'A measure of betweenness centrality based on random walks',
    # M.E.J. Newman (2004)
    def calculate_on_connected_graph(self, g):
        n = g.number_of_nodes()

        T = construct_newman_T_matrix(g)

        s, t = np.array(list(combinations(np.arange(n), 2))).transpose()  # Find all pairs s<t
        b = np.zeros(n)  # Initialise array of betweennesses
        for i, j in g.edges:

            B = np.abs(T[i, s] - T[i, t] - T[j, s] + T[j, t])

            # Exclude values where (i =/= s,t) in equation (9)
            b[i] += np.sum(B[(s != i) & (t != i)])
            b[j] += np.sum(B[(s != j) & (t != j)])

        b /= ((n-1)*(n-2))  # normalise

        # Return the result as a dictionary mapping (node)->(random walk betweenness centrality)
        return dict(zip(range(n), b))
