from networkx.algorithms.centrality.current_flow_betweenness import approximate_current_flow_betweenness_centrality
from random_walk_betweenness.RandomWalkBetweennessSolver import RandomWalkBetweennessSolver


class NXApproxSolver(RandomWalkBetweennessSolver):
    def calculate_on_connected_graph(self, g, epsilon=0.05):
        return approximate_current_flow_betweenness_centrality(g, epsilon=0.05)

