"""In evolutionary computation, DE finds a solution by iterative improvement
of a candidate solution with regard to a given measure of quality. It is
one of the most powerful optimization tools that operate on the basis of the
same  developmental  process  in  evolutionary  algorithms.  Nevertheless,
different  from  traditional  evolutionary algorithms, DE uses the scaled
differences of vectors to produce new candidate solutions in the population.
Hence, no separate probability distribution should be used to perturb the population
members. The DE is also characterized by the advantages of having few parameters and
ease of implementation. The application of DE on engineering and biomedical studies
has attracted a high level of interest, concerning its potential. Basically, DE algorithm
works through a particular sequence of stages. First, it creates an initial population
sampled uniformly at random within the search bounds. Thereafter, three components namely
mutation, crossover and  selection  are  adopted  to  evolve  the  initial  population.
The  mutation  and  crossover  are  used  to  create  new solutions, while selection
determines the solutions that will breed a new generation.  The algorithm remains
inside loop until stopping criteria are met. We implemented the original version of the algorithm[1-3].

References

    [1] Storn, R and Price, K, Differential Evolution - a Simple and\
               Efficient Heuristic for Global Optimization over Continuous Spaces,\
               Journal of Global Optimization, 1997, 11, 341 - 359.\


    [2] http://www1.icsi.berkeley.edu/~storn/code.html\


    [3] http://en.wikipedia.org/wiki/Differential_evolution\

"""

import random
import numpy as np

from uhaopt.util import check_bounds
from uhaopt.util import dump_results

__author__ = "Hojjat Rakhshani"
__license__ = "MIT"
__email__ = "hojjat.rakhshani@uha.fr"
__status__ = "Development"

class DE:
    """
    :param cost_func:  a cost/loss function is a function that maps an event or values of one or more variables onto\
    a real number intuitively representing some "cost" associated with the event. For NAS, a cost function is used to\
    summarise, as a single figure of merit, how close a given design architecture is to achieving the set aims.\

    :param bounds: sequence of (min, max) pairs for each individual. None is used to specify no bound.\

    :param pop_size: algorithm optimizes a problem by maintaining a population of candidate solutions\
    and creating new candidate solutions by combining existing ones according to its simple formulae,\
    and then keeping whichever candidate solution has the best cost on the problem at hand. Simply, pop_size\
    denotes the number of population members.\

    :param dimension: number of decision variables of the cost function\

    :param F: mutation factor F is a constant from interval [0, 2]. Algorithm is also somewhat sensitive to\
    the choice of the step size F. A good initial guess is to choose F from interval [0.5, 1].\

    :param CR:  crossover probability constant from interval [0, 1]. CR, the crossover probability constant\
    from interval [0, 1] helps to maintain the diversity of the population and is rather uncritical. If the\
    parameters are correlated, high values of CR work better; and vice versa.\

    :param strategy: different search strategies to evolve the solutions.


    :param max_evaluations: the number of evaluations for evolving the\
    solutions (i.e., computational budgets)\

    :param tol: tolerance for termination.
    :param population: an initial population of individuals.
    :param cost: the initial cost array for the associated individuals in the population.
    :param display: whether display the results on the output or not.
    :param save_directory: the configurations are saved into a file named 'configs.json', while 'results.json' is used\
    to save the metrics. the results also contain initial population, final population and their associated\
    metrics. Here, the output formats are json and CSV, which let's the user to do post_processing\
    using an arbitrary tool.
    :param save_results: you can save all the valid generated configurations and their associated metrics\
    to the output.
    """

    def __init__(self, cost_func=None, bounds=None, pop_size=50, dimension=2, F=0.9,
                 CR=0.5, strategy=1, max_evaluations=100, tol=0.0, population=None, cost=None, display=True,
                 save_directory=None,
                 save_results=False):

        assert cost_func is not None, "Please pass a valid cost function for your optimization problems"
        assert len(bounds) == dimension, "The bounds and dimension parameters should have equal dimensions."

        # population initialization using uniform distribution
        if population is None:
            population = []
            for i in range(pop_size):
                for j in range(dimension):
                    if bounds[j][0] is None:
                        population.append(random.uniform(0, bounds[j][1]))
                    elif bounds[j][1] is None:
                        population.append(random.uniform(bounds[j][0], 1.0))
                    else:
                        population.append(random.uniform(bounds[j][0], bounds[j][1]))

            population = np.array(population).reshape((pop_size, dimension))

        # evaluate the individuals after initialization
        function_evaluations = 0

        if cost is None:
            cost = []
            for individual in population:
                cost_p = cost_func(individual)

                # only valid solutions will be saved
                if type(cost_p) is not float:

                    function_evaluations = function_evaluations + 1
                    if save_results:
                        dump_results(save_directory=save_directory, solution=individual, cost_dic=cost_p,
                                     current_evaluation=function_evaluations, initial_population=True)
                else:
                    if save_results:
                        dump_results(save_directory=save_directory, solution=individual, cost_dic=cost_p,
                                     current_evaluation=function_evaluations, initial_population=True)
                cost.append(cost_p)

                if (min(cost) < tol) or (function_evaluations >= max_evaluations):
                    return

            cost = np.array(cost)

        # cycle through each generation
        while True:

            index_min = np.argmin(cost)  # best individual so far
            best_individual = population[index_min]  # best member of current iteration

            bm = np.tile(best_individual, (pop_size, 1))

            mpo = np.random.rand(pop_size, len(bounds)) < CR  # all random numbers < CR are 1, 0 otherwise
            mui = 1 - mpo  # inverse mask

            if strategy == 1:
                pm1 = population.copy()
                pm2 = population.copy()

                random.shuffle(pm1)  # shuffled population 1
                random.shuffle(pm2)  # shuffled population 2

                ui = bm + F * (np.array(pm1) - np.array(pm2))  # DE/best/1
                ui = np.array(population) * mpo + ui * mui
            elif strategy == 2:
                pm1 = population.copy()
                pm2 = population.copy()
                pm3 = population.copy()

                random.shuffle(pm1)  # shuffled population 1
                random.shuffle(pm2)  # shuffled population 2
                random.shuffle(pm3)  # shuffled population 3

                ui = np.array(pm3) + F * (np.array(pm1) - np.array(pm2))  # DE/rand/1
                ui = np.array(population) * mpo + ui * mui
            elif strategy == 3:
                pm1 = population.copy()
                pm2 = population.copy()

                random.shuffle(pm1)  # shuffled population 1
                random.shuffle(pm2)  # shuffled population 2
                ui = np.array(population) + F * (bm - np.array(population)) + F * (
                        np.array(pm1) - np.array(pm2))  # DE/rand-to-best/1
                ui = np.array(population) * mpo + ui * mui
            elif strategy == 4:
                pm1 = population.copy()  # shuffled population 1
                pm2 = population.copy()  # shuffled population 2
                pm3 = population.copy()  # shuffled population 3
                pm4 = population.copy()  # shuffled population 4

                random.shuffle(pm1)
                random.shuffle(pm2)
                random.shuffle(pm3)
                random.shuffle(pm4)

                ui = bm + F * (np.array(pm1) - np.array(pm2) + np.array(pm3) - np.array(pm4))  # DE/best/2
                ui = np.array(population) * mpo + ui * mui
            elif strategy == 5:

                pm1 = population.copy()  # shuffled population 1
                pm2 = population.copy()  # shuffled population 2
                pm3 = population.copy()  # shuffled population 3
                pm4 = population.copy()  # shuffled population 4
                pm5 = population.copy()  # shuffled population 5

                random.shuffle(pm1)
                random.shuffle(pm2)
                random.shuffle(pm3)
                random.shuffle(pm4)
                random.shuffle(pm5)

                ui = np.array(pm5) + F * (np.array(pm1) - np.array(pm2) + np.array(pm3) - np.array(pm4))  # DE/rand/2
                ui = np.array(population) * mpo + ui * mui

            # cycle through each individual in the population
            for j in range(0, pop_size):

                trial_individual = check_bounds(solution=ui[j, :], bounds=bounds)

                trial_cost = cost_func(trial_individual)

                # only valid solutions will be saved
                if type(trial_cost) is not float:

                    function_evaluations = function_evaluations + 1
                    if save_results:
                        dump_results(save_directory=save_directory, solution=trial_individual,cost_dic=trial_cost,
                                     current_evaluation=function_evaluations, initial_population=False)
                    else:
                        if save_results:
                            dump_results(save_directory=save_directory, solution=trial_individual, cost_dic=trial_cost,
                                         current_evaluation=function_evaluations, initial_population=True)

                #  select which vectors are allowed to enter the new population
                if trial_cost < cost[j]:
                    population[j] = trial_individual
                    cost[j] = trial_cost

                # At the end, we will save all the results for the population
                if (np.min(cost) < tol) or (function_evaluations >= max_evaluations):
                    return
                if display:
                    print(['The best solution after ', function_evaluations, 'evaluations is: ', min(cost)])
