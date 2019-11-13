from networkx.generators.random_graphs import erdos_renyi_graph
from networkx.readwrite.adjlist import write_adjlist


def generate_erdos_renyi(n, p, file_path):
    g = erdos_renyi_graph(n, p)
    write_adjlist(g, file_path, delimiter=",", comments="#")


if __name__ == '__main__':
    path = r'C:\Users\Dan\PycharmProjects\Random-Walk-Betweenness\graphs\resources'

    generate_erdos_renyi(500, 0.05, path + r"\erdos_renyi")
