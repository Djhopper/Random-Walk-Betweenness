import networkx as nx
from graphs.read_write import read_graph
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from algorithms.random_walk_centrality.random_walk_centrality import random_walk_centrality
import numpy as np


def draw_graph(graph_name, metric=None):
    g = read_graph(graph_name)

    if metric == "random_walk_centrality":
        color_by = random_walk_centrality(g)
    else:
        raise NotImplementedError

    # Get colours and positions of nodes
    node_color = [color_by[node] for node in g.nodes()]
    cmap = cm.Blues
    pos = nx.drawing.layout.spring_layout(g)
    # Plot nodes
    nodes = nx.draw_networkx_nodes(g, node_color=node_color, cmap=cmap, pos=pos)
    nodes.set_edgecolor("grey")
    # Plot edges
    nx.draw_networkx_edges(g, pos=pos, edge_color="gray")
    # Add legend (colour scale)
    sm = cm.ScalarMappable(cmap=cmap)
    sm.set_array(np.array([0, 1]))
    cbar = plt.colorbar(sm)
    cbar.ax.set_ylabel('Random Walk Betweenness Centrality', rotation=270)
    cbar.set_ticks(np.array([0, 1]))
    # Disable axis, add title
    plt.axis('off')
    plt.title("Plot showing random walk betweenness\ncentrality of nodes in the " + graph_name)


if __name__ == '__main__':
    draw_graph("kite_graph", metric="random_walk_centrality")
    plt.show()
