from random_walk_betweenness.RandomWalkBetweennessSolver import RandomWalkBetweennessSolver
from random_walk_betweenness.NewmanSolver import NewmanSolver
from random_walk_betweenness.BrandesSolver import BrandesSolver, BrandesSolverSparse, BrandesSolverDense
from random_walk_betweenness.ApproxSolver import ApproxSolver
from random_walk_betweenness.NXApproxSolver import NXApproxSolver
from graphs.read_write import read_graph


method_names = ["nx", "newman", "brandes", "brandes_dense", "brandes_sparse", "approx", "nxapprox"]


def random_walk_centrality(g, method="nx"):
    assert method in method_names

    if method == "nx":
        solver = RandomWalkBetweennessSolver()
    if method == "newman":
        solver = NewmanSolver()
    if method == "brandes":
        solver = BrandesSolver()
    if method == "brandes_sparse":
        solver = BrandesSolverSparse()
    if method == "brandes_dense":
        solver = BrandesSolverDense()
    if method == "approx":
        solver = ApproxSolver()
    if method == "nxapprox":
        solver = NXApproxSolver()

    return solver.calculate(g)


if __name__ == '__main__':
    g = read_graph("kite_graph")
    print(random_walk_centrality(g, method="nx"))
    print(random_walk_centrality(g, method="approx"))
