from networkx.algorithms.centrality.current_flow_betweenness import current_flow_betweenness_centrality


class RandomWalkBetweennessCentralitySolver:
    def calculate(self, g):
        return current_flow_betweenness_centrality(g)
