from networkx.algorithms.centrality.current_flow_betweenness import current_flow_betweenness_centrality


def random_walk_centrality(g):
    centrality = current_flow_betweenness_centrality(g)
    return centrality
