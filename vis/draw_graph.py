import networkx as nx
from graphs.read_write import read_graph
import matplotlib.pyplot as plt
from algorithms.random_walk_centrality.random_walk_centrality import random_walk_centrality


def draw_graph(graph_name, metric=None):
    g = read_graph(graph_name)

    if metric is None:
        nx.draw(g, with_labels=True)
    else:
        if metric == "random_walk_centrality":
            color_by = random_walk_centrality(g)
            node_color = [color_by[node] for node in g.nodes()]
            nx.draw(g, with_labels=True, node_color=node_color, cmap=plt.cm.Blues)
        else:
            raise NotImplementedError


if __name__ == '__main__':
    draw_graph("erdos_renyi", metric="random_walk_centrality")
    plt.show()
