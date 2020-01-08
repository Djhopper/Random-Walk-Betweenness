from algorithms.random_walk_centrality.nx_implementation import random_walk_centrality as nx_implementation
from algorithms.random_walk_centrality.newman_implementation import random_walk_centrality as newman_implementation
from algorithms.random_walk_centrality.brandes_implementation import random_walk_centrality as brandes_implementation
from graphs.read_write import read_graph


method_names = ["nx", "newman", "brandes", "brandes_dense", "brandes_sparse"]


def random_walk_centrality(g, method="nx"):
    assert method in method_names

    if method == "nx":
        return nx_implementation(g)
    if method == "newman":
        return newman_implementation(g)
    if method == "brandes":
        return brandes_implementation(g)
    if method == "brandes_sparse":
        return brandes_implementation(g, sparse=True)
    if method == "brandes_dense":
        return brandes_implementation(g, sparse=False)


if __name__ == '__main__':
    g = read_graph("bull_graph")
    print(random_walk_centrality(g))
