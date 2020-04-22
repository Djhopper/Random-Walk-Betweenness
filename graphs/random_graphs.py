from networkx.generators.random_graphs import erdos_renyi_graph
from networkx.generators.random_graphs import powerlaw_cluster_graph
from networkx.generators.random_graphs import watts_strogatz_graph
from graphs.read_write import write_graph


def generate_erdos_renyi(n, p, graph_name):
    g = erdos_renyi_graph(n, p)
    write_graph(g, graph_name)


def get_erdos_renyi(n, average_degree):
    g = erdos_renyi_graph(n, average_degree/n)
    return g


def get_holme_kim(n, p, average_degree):
    assert average_degree % 2 == 0
    g = powerlaw_cluster_graph(n, average_degree//2, p)
    return g


def get_watts_strogatz_graph(n, p, average_degree):
    assert average_degree % 2 == 0
    g = watts_strogatz_graph(n, average_degree, p)
    return g
