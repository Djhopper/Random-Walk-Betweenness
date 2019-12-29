from algorithms.random_walk_centrality.random_walk_centrality import random_walk_centrality
from networkx.generators.random_graphs import random_lobster, erdos_renyi_graph
from graphs.read_write import read_graph


def do_accuracy_test(g):
    centrality1 = random_walk_centrality(g, method="nx")
    centrality2 = random_walk_centrality(g, method="brandes")

    centrality1 = dict((int(key), value) for key, value in centrality1.items())
    centrality2 = dict((int(key), value) for key, value in centrality2.items())

    assert centrality1.keys() == centrality2.keys()

    acceptable_error = 0.001
    for node in centrality1.keys():
        x = centrality1[node]
        y = centrality2[node]
        assert y - acceptable_error <= x <= y + acceptable_error


def test_bull_graph():
    do_accuracy_test(read_graph("bull_graph"))


def test_erdos_renyi():
    do_accuracy_test(read_graph("erdos_renyi"))


def test_random_graphs():
    for i in range(1):
        do_accuracy_test(random_lobster(20, 0.5, 0.1))
        do_accuracy_test(erdos_renyi_graph(30, 0.3))
