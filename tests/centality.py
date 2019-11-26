def are_close(centrality1, centrality2):
    centrality1 = dict((int(key), value) for key, value in centrality1.items())
    centrality2 = dict((int(key), value) for key, value in centrality2.items())
    #print(centrality1)
    #print(centrality2)

    if centrality1.keys() != centrality2.keys():
        print(centrality1.keys(), centrality2.keys())
        return False

    acceptable_error = 0.01
    for node in centrality1.keys():
        x = centrality1[node]
        y = centrality2[node]
        if x < y - acceptable_error or x > y + acceptable_error:
            return False

    return True


def print_test(g, graph_name):
    print(graph_name,
          are_close(
              random_walk_centrality(g, method="nx"),
              random_walk_centrality(g, method="newman"))
          )


if __name__ == '__main__':
    from algorithms.random_walk_centrality.random_walk_centrality import random_walk_centrality
    from networkx.generators.random_graphs import connected_watts_strogatz_graph, random_lobster, erdos_renyi_graph
    from graphs.read_write import read_graph
    import networkx as nx

    for graph_name in ["bull_graph", "erdos_renyi", "house_graph", "star_graph"]:
        g = read_graph(graph_name)
        print_test(g, graph_name)

    #print_test(connected_watts_strogatz_graph(50, 2, 0.02), "watts_strogatz")

    print_test(random_lobster(15, 0.5, 0.1), "lobster")

    print_test(max(nx.connected_component_subgraphs(erdos_renyi_graph(20, 0.2)), key=len), "erdos_renyi_round_2")


