from utils.training import train_solver
from solvers.encoding import ProblemInstanceEncoding
from solvers.solvers import SolverWithIndividualMutationControl
from solvers.solvers import SolverWithGeneMutationControl
from solvers.solvers import SolverWithFitnessShapingCrossover
from solvers.solvers import SolverWithFitnessShapingSelection

import torch
import random
import os.path
import sys


torch.manual_seed(0)
torch.cuda.manual_seed(0)
random.seed(0)

encoder = ProblemInstanceEncoding()

print(sys.argv)

##############################################################
##                  Possible Arguments                      ##
##############################################################

solver_arg = sys.argv[1]
outdir = sys.argv[2]

# directory for baseline file
weightsdir = None
# e.g. pre:INDEX to start with a specific task
start_at = None

if len(sys.argv) > 3:
    weightsdir = sys.argv[3]
if len(sys.argv) > 4:
    start_at = sys.argv[4]


population_size = 100

solverMap = {
    'gene': SolverWithGeneMutationControl,
    'individual': SolverWithIndividualMutationControl,
    'crossover': SolverWithFitnessShapingCrossover,
    'selection': SolverWithFitnessShapingSelection
}

solver = solverMap.get(solver_arg, None)(encoder, population_size, num_hidden_layers=(1,0), learning_rate=5e-6)
if solver is not None:
    if weightsdir is not None and os.path.isfile(weightsdir + "baseline"):
        print("loading baseline")
        solver.load_weights(weightsdir + "baseline")
    solver.set_evaluation_function(lambda population : population.evaluate(get_unsatisfied=True))
    if start_at is not None:
            train_solver(solver, outdir, int(start_at))
    else:
        train_solver(solver, outdir)
