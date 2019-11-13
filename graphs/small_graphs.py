from networkx.generators.small import bull_graph
from graphs.read_write import write_graph


def generate_bull_graph():
    g = bull_graph()
    write_graph(g, "bull_graph")


if __name__ == '__main__':
    generate_bull_graph()
