import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from graphs.read_write import get_all_existing_graph_names, read_graph
from random_walk_betweenness.calculate import random_walk_betweenness_strategies
from scripts.timing.time_algorithm_execution import time_random_walk_centrality_algorithm
from random_walk_betweenness.calculate import random_walk_betweenness
from scripts.vis.draw_graph import draw_graph
import pandas
import matplotlib.pyplot as plt
import argparse


def input_graph_name():
    graph_names = get_all_existing_graph_names()

    print("Select a graph by inputting a number:")
    for i, name in enumerate(graph_names):
        print(i, "-", name, )
        # "(", read_graph(name).number_of_nodes(), "nodes,", read_graph(name).number_of_edges(), "edges )")

    graph_name = graph_names[int(input())]
    return graph_name


def input_method_name():
    method_names = list(random_walk_betweenness_strategies.keys())

    print("Select a method by inputting a number:")
    for i, name in enumerate(method_names):
        print(i, "-", name)

    method_name = method_names[int(input())]
    return method_name


def input_output_format():
    output_format_names = ["time", "csv", "vis"]

    print("Select an output format by inputting a number:")
    for i, name in enumerate(output_format_names):
        print(i, "-", name)

    output_format = output_format_names[int(input())]
    return output_format


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph_name", choices=get_all_existing_graph_names())
    parser.add_argument("--method_name", choices=list(random_walk_betweenness_strategies.keys()))
    parser.add_argument("--output", choices=["csv", "vis", "time"])
    args = parser.parse_args()

    graph_name = args.graph_name if args.graph_name else input_graph_name()
    method_name = args.method_name if args.method_name else input_method_name()
    output_format = args.output if args.output else input_output_format()

    if output_format == "time":
        print(time_random_walk_centrality_algorithm(graph=graph_name, method_name=method_name))

    elif output_format == "csv":
        output_file_name = input("Please enter a name for your output file:")
        # Get full path of output file
        cwd = os.getcwd()
        folder_name = "Random-Walk-Betweenness"
        base_directory = cwd[:cwd.find(folder_name)] + folder_name
        output_path = os.path.join(base_directory, "data", "random_walk_betweenness_data", output_file_name+".csv")

        rw_dict = random_walk_betweenness(read_graph(graph_name), strategy=method_name)
        data = [{"node": node, "betweenness": betweenness} for node, betweenness in rw_dict.items()]
        df = pandas.DataFrame(data)
        df.to_csv(output_path, index=False)

    elif output_format == "vis":
        draw_graph(graph=graph_name, strategy=method_name)
        plt.show()


if __name__ == '__main__':
    main()
