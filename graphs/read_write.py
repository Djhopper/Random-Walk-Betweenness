import os
from networkx.readwrite.adjlist import read_adjlist
from networkx.readwrite.adjlist import write_adjlist
from networkx.relabel import convert_node_labels_to_integers


# Get path of the resources directory
cwd = os.getcwd()
folder_name = "Random-Walk-Betweenness"
base_directory = cwd[:cwd.find(folder_name)] + folder_name
resources_path = os.path.join(base_directory, "graphs", "resources")


def write_graph(g, graph_name):
    write_adjlist(g, os.path.join(resources_path, graph_name), delimiter="\t", comments="#")


def read_graph(graph_name):
    g = read_adjlist(
        os.path.join(resources_path, graph_name),
        delimiter="\t" if graph_name not in ["facebook_combined.txt", "email-Eu-core"] else " ",
        comments="#"
    )
    return convert_node_labels_to_integers(g)


def get_all_existing_graph_names():
    return os.listdir(resources_path)
