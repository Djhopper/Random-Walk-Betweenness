from random_walk_betweenness.RandomWalkBetweennessSolver import RandomWalkBetweennessSolver
from random_walk_betweenness.NewmanSolver import NewmanSolver
from random_walk_betweenness.BrandesSolver import BrandesSolver
from random_walk_betweenness.ApproxSolver import ApproxSolver
from random_walk_betweenness.NXApproxSolver import NXApproxSolver


random_walk_betweenness_strategies = {
    "nx": RandomWalkBetweennessSolver(),
    "newman": NewmanSolver(),
    "brandes": BrandesSolver(),
    "approx": ApproxSolver(),
    "nxapprox": NXApproxSolver(),
}


def random_walk_centrality(g, strategy="nx"):
    if strategy not in random_walk_betweenness_strategies:
        raise ValueError("You must pick one of the following strategies: "
                         + str(list(random_walk_betweenness_strategies.keys())))

    solver = random_walk_betweenness_strategies[strategy]
    return solver.calculate(g)
