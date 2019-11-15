from networkx.drawing import nx_pylab as pylab
from graphs.read_write import read_graph
import matplotlib.pyplot as plt


def draw_graph(graph_name, metric=None):
    g = read_graph(graph_name)

    if metric is None:
        pylab.draw(g)
    else:
        raise NotImplementedError


if __name__ == '__main__':
    draw_graph("erdos_renyi")
    plt.show()
