import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from graphs.read_write import get_all_existing_graph_names, read_graph
from algorithms.random_walk_centrality.random_walk_centrality import method_names
from scripts.time_algorithm_execution import time_random_walk_centrality_algorithm


def main():
    while True:
        graph_names = get_all_existing_graph_names()

        print("Select a graph by inputting a number:")
        for i, name in enumerate(graph_names):
            print(i, "-", name)

        graph_name = graph_names[int(input())]

        print("Select a method by inputting a number:")
        for i, name in enumerate(method_names):
            print(i, "-", name)

        method_name = method_names[int(input())]

        data = time_random_walk_centrality_algorithm(graph=graph_name, method_name=method_name)

        print("Results:", data)

        if input("Continue by pressing enter... (enter q to quit)").upper() in ["Q", "QUIT"]:
            return


if __name__ == '__main__':
    main()
