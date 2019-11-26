from networkx.generators.random_graphs import erdos_renyi_graph
from graphs.read_write import write_graph


def generate_erdos_renyi(n, p, graph_name):
    g = erdos_renyi_graph(n, p)
    write_graph(g, graph_name)


if __name__ == '__main__':
    generate_erdos_renyi(10, 0.5, "erdos_renyi")
