from networkx.generators.random_graphs import erdos_renyi_graph
from networkx.generators.random_graphs import powerlaw_cluster_graph
from networkx.generators.random_graphs import watts_strogatz_graph
from graphs.read_write import write_graph


def get_erdos_renyi(n, average_degree):
    g = erdos_renyi_graph(n, average_degree/n)
    return g


def add_erdos_renyi_to_library(n, average_degree, graph_name):
    g = get_erdos_renyi(n, average_degree)
    write_graph(g, graph_name)


def get_holme_kim(n, p, average_degree):
    assert average_degree % 2 == 0
    g = powerlaw_cluster_graph(n, average_degree//2, p)
    return g


def add_holme_kim_to_library(n, p, average_degree, graph_name):
    g = get_holme_kim(n, p, average_degree)
    write_graph(g, graph_name)


def get_watts_strogatz_graph(n, p, average_degree):
    assert average_degree % 2 == 0
    g = watts_strogatz_graph(n, average_degree, p)
    return g


def add_watts_strogatz_to_library(n, p, average_degree, graph_name):
    g = get_watts_strogatz_graph(n, p, average_degree)
    write_graph(g, graph_name)


if __name__ == '__main__':
    add_erdos_renyi_to_library(100, 10, "erdos_renyi")
    add_holme_kim_to_library(50, 0.2, 16, "holme_kim")
    add_watts_strogatz_to_library(150, 0.1, 20, "watts_strogatz")
