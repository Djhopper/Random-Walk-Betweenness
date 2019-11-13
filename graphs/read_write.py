import os
from networkx.readwrite.adjlist import read_adjlist
from networkx.readwrite.adjlist import write_adjlist


resources_path = r"C:\Users\Dan\PycharmProjects\Random-Walk-Betweenness\graphs\resources"


def write_graph(g, graph_name):
    write_adjlist(g, os.path.join(resources_path, graph_name), delimiter=",", comments="#")


def read_graph(graph_name):
    return read_adjlist(os.path.join(resources_path, graph_name), delimiter=",", comments="#")
