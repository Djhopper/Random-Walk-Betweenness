from networkx.generators.small import bull_graph
from networkx.readwrite.adjlist import write_adjlist


def generate_bull_graph(file_path):
    g = bull_graph()
    write_adjlist(g, file_path, delimiter=",", comments="#")


if __name__ == '__main__':
    path = r"C:\Users\Dan\PycharmProjects\Random-Walk-Betweenness\graphs\resources"

    generate_bull_graph(path + r"\bull_graph")
