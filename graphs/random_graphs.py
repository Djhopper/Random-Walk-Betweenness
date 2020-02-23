from networkx.generators.random_graphs import erdos_renyi_graph
from graphs.read_write import write_graph
import networkx as nx


def generate_erdos_renyi(n, p, graph_name):
    g = erdos_renyi_graph(n, p)
    write_graph(g, graph_name)


def get_erdos_renyi(n, average_degree):
    g = erdos_renyi_graph(n, average_degree/n)
    g = g.subgraph(sorted(nx.connected_components(g), key=len, reverse=True)[0])  # select largest connected component
    g = nx.relabel.convert_node_labels_to_integers(g)
    return g


if __name__ == '__main__':
    generate_erdos_renyi(500, 0.1, "erdos_renyi")
