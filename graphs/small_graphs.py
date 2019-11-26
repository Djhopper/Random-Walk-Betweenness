from networkx.generators.small import bull_graph, house_graph
from networkx.generators.classic import star_graph
from graphs.read_write import write_graph


def generate_bull_graph():
    g = bull_graph()
    write_graph(g, "bull_graph")


def generate_star_graph():
    g = star_graph(6)
    write_graph(g, "star_graph")


def generate_house_graph():
    g = house_graph()
    write_graph(g, "house_graph")


if __name__ == '__main__':
    generate_bull_graph()
    generate_star_graph()
    generate_house_graph()
