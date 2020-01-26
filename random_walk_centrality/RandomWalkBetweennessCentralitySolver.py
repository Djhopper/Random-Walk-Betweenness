from networkx.algorithms.centrality.current_flow_betweenness import current_flow_betweenness_centrality
import networkx as nx


class RandomWalkBetweennessCentralitySolver:
    def calculate_on_connected_graph(self, g):
        return current_flow_betweenness_centrality(g)

    def calculate(self, g):
        components = nx.connected_component_subgraphs(g)

        output = {}

        for component in components:
            if len(component.nodes) <= 2:
                output.update(dict((node, 0) for node in component.nodes))
            else:
                mapping = dict((node, i) for i, node in enumerate(component.nodes))
                inverse_mapping = dict((i, node) for i, node in enumerate(component.nodes))

                relabeled_component = nx.relabel.relabel_nodes(component, mapping)
                relabeled_result = self.calculate_on_connected_graph(relabeled_component)
                result = dict((inverse_mapping[i], relabeled_result[i]) for i in relabeled_result.keys())

                output.update(result)

        return output
