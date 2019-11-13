from algorithms.random_walk_centrality.nx_implementation import random_walk_centrality as nx_implementation
from networkx.readwrite.adjlist import read_adjlist


def random_walk_centrality(g, method="nx"):
    if method == "nx":
        return nx_implementation(g)


if __name__ == '__main__':
    path = r"C:\Users\Dan\PycharmProjects\Random-Walk-Betweenness\graphs\resources\bull_graph"
    g = read_adjlist(path, delimiter=",")
    print(random_walk_centrality(g))
