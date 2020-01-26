from random_walk_centrality.RandomWalkBetweennessCentralitySolver import RandomWalkBetweennessCentralitySolver
from random_walk_centrality.NewmanSolver import NewmanSolver
from random_walk_centrality.BrandesSolver import BrandesSolver, BrandesSolverSparse, BrandesSolverDense
from graphs.read_write import read_graph


method_names = ["nx", "newman", "brandes", "brandes_dense", "brandes_sparse"]


def random_walk_centrality(g, method="nx"):
    assert method in method_names

    if method == "nx":
        solver = RandomWalkBetweennessCentralitySolver()
    if method == "newman":
        solver = NewmanSolver()
    if method == "brandes":
        solver = BrandesSolver()
    if method == "brandes_sparse":
        solver = BrandesSolverSparse()
    if method == "brandes_dense":
        solver = BrandesSolverDense()

    return solver.calculate(g)


if __name__ == '__main__':
    g = read_graph("bull_graph")
    print(random_walk_centrality(g))
