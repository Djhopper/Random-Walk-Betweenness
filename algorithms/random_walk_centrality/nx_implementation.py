from networkx.algorithms.centrality.current_flow_betweenness import current_flow_betweenness_centrality
from networkx.readwrite.adjlist import read_adjlist


def random_walk_centrality(g):
    return current_flow_betweenness_centrality(g)


if __name__ == '__main__':
    path = r"C:\Users\Dan\PycharmProjects\Random-Walk-Betweenness\graphs\resources\bull_graph"
    g = read_adjlist(path, delimiter=",")
    print(random_walk_centrality(g))
