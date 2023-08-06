"""In operations research, cuckoo search is an optimization algorithm developed
by Xin-she Yang and Suash Deb in 2009.[1][2] It was inspired by the obligate
brood parasitism of some cuckoo species by laying their eggs in the nests of
other host birds (of other species). Cuckoo search (CS) uses the following representations:

Each egg in a nest represents a solution, and a cuckoo egg represents a new solution.
The aim is to use the new and potentially better solutions (cuckoos) to replace a not-so-good
solution in the nests. In the simplest form, each nest has one egg. The algorithm can
be extended to more complicated cases in which each nest has multiple eggs representing a
set of solutions. CS is based on three idealized rules:

    1- Each cuckoo lays one egg at a time, and dumps its egg in a randomly chosen nest\


    2- The best nests with high quality of eggs will carry over to the next generation\


    3- The number of available hosts nests is fixed, and the egg laid by a cuckoo is\
    discovered by the host bird with a probability pa. Discovering operate on some set
    of worst nests, and discovered solutions dumped from farther calculations.\


In addition, Yang and Deb discovered that the random-walk style search is better\
performed by Lévy flights rather than simple random walk.\


References

    [1] Yang, X. S., & Deb, S. (2009, December). Cuckoo search via Lévy flights.\
    In 2009 World Congress on Nature & Biologically Inspired Computing (NaBIC)\
    (pp. 210-214). IEEE.\


    [2] https://en.wikipedia.org/wiki/Cuckoo_search\

"""

import numpy as np
import random
import math

from uhaopt.util import check_bounds
from uhaopt.util import dump_results

__author__ = "Hojjat Rakhshani"
__license__ = "MIT"
__email__ = "hojjat.rakhshani@uha.fr"
__status__ = "Development"

class CS:

    """
    :param cost_func: A d-dimensional cost function  that maps values of the design variables onto\
     a real number intuitively representing some "cost" associated with the event.
    :param bounds: sequence of (min, max) pairs for each particle. None is used to specify no bound.\
    :param n: Number of nests (or different solutions)
    :param dimension: number of decision variables of the cost function\
    :param pa: Discovery rate of alien eggs/solutions
    :param max_evaluations: the number of evaluations for evolving the\
    solutions (i.e., computational budgets)\
    :param tol: tolerance for termination.
    :param nest: an initial population nxdimension array of nests.
    :param cost: the initial cost array for the associated solutions in the population.
    :param display: whether display the results on the output or not.
    :param save_directory: the configurations are saved into a file named 'configs.json', while 'results.json' is used\
    to save the metrics. the results also contain initial population, final population and their associated\
    metrics. Here, the output formats are json and CSV, which let's the user to do post_processing\
    using an arbitrary tool.
    :param save_results:  you can save all the valid generated configurations and their associated metrics\
    to the output.
    """

    def __init__(self, cost_func=None, bounds=None, n=15, dimension=2, pa=0.25, max_evaluations=100,
                 tol=1.0e-4, nest=None, cost=None, display=True, save_directory=None, save_results=False):

        assert cost_func is not None, "Please pass a valid cost function for your optimization problems"
        assert len(bounds) == dimension, "The bounds and dimension parameters should have equal dimensions."

        if nest is None:

            nest = []
            for i in range(n):
                for j in range(dimension):
                    nest.append(random.uniform(bounds[j][0], bounds[j][1]))

            nest = np.array(nest).reshape((n, dimension))

        function_evaluations = 0

        if cost is None:
            cost = []
            for cuckoo in nest:
                cost_p = cost_func(cuckoo)

                if type(cost_p) is not float:

                    function_evaluations = function_evaluations + 1
                    if save_results:
                        dump_results(save_directory=save_directory, solution=cuckoo, cost_dic=cost_p,
                                     current_evaluation=function_evaluations, initial_population=True)
                else:
                    if save_results:
                        dump_results(save_directory=save_directory, solution=cuckoo, cost_dic=cost_p,
                                     current_evaluation=function_evaluations, initial_population=True)
                cost.append(cost_p)

                if (min(cost) < tol) or (function_evaluations >= max_evaluations):
                    return
            cost = np.array(cost)

        index_best = np.argmin(cost)
        best_nest = nest[index_best]

        while True:
            new_nest = self.get_cuckoos(nest, best_nest)

            # cycle through each individual in the population
            for j in range(0, n):

                trial_nest = check_bounds(solution=new_nest[j, :], bounds=bounds)

                trial_cost = cost_func(trial_nest)

                if type(trial_cost) is not float:

                    function_evaluations = function_evaluations + 1
                    if save_results:
                        dump_results(save_directory=save_directory, solution=trial_nest, cost_dic=trial_cost,
                                     current_evaluation=function_evaluations, initial_population=False)
                else:
                    if save_results:
                        dump_results(save_directory=save_directory, solution=trial_nest, cost_dic=trial_cost,
                                     current_evaluation=function_evaluations, initial_population=False)

                if trial_cost <= cost[j]:
                    nest[j] = trial_nest
                    cost[j] = trial_cost

                if (np.min(cost) < tol) or (function_evaluations >= max_evaluations):
                    return

                if display:
                    print(['The best solution after ', function_evaluations, 'evaluations is: ', min(cost)])

            new_nest = self.empty_nests(nest, pa)

            # cycle through each individual in the population
            for j in range(0, n):

                trial_nest = check_bounds(solution=new_nest[j, :], bounds=bounds)

                trial_cost = cost_func(trial_nest)

                if type(trial_cost) is not float:

                    function_evaluations = function_evaluations + 1
                    if save_results:
                        dump_results(save_directory=save_directory, solution=trial_nest, cost_dic=trial_cost,
                                     current_evaluation=function_evaluations, initial_population=False)
                else:
                    if save_results:
                        dump_results(save_directory=save_directory, solution=trial_nest, cost_dic=trial_cost,
                                     current_evaluation=function_evaluations, initial_population=False)

                if trial_cost <= cost[j]:
                    nest[j] = trial_nest
                    cost[j] = trial_cost

                if (np.min(cost) < tol) or (function_evaluations >= max_evaluations):
                    return

                if display:
                    print(['The best solution after ', function_evaluations, 'evaluations is: ', min(cost)])

            index_best = np.argmin(cost)
            best_nest = nest[index_best]

    @staticmethod
    def get_cuckoos(nest, best_nest):
        new_nest = nest.copy()
        beta = 3 / 2
        sigma = (math.gamma(1 + beta) * np.sin(np.pi * beta / 2) / (
                    math.gamma((1 + beta) / 2) * beta * 2 ** ((beta - 1) / 2))) ** (1 / beta)
        for j in range(len(nest)):
            s = nest[j, :].copy()
            u = np.random.randn(s.size) * sigma
            v = np.random.randn(s.size)
            step = u / np.abs(v) ** (1 / beta)
            step_size = 0.01 * step * (s - best_nest)

            s = s + step_size * np.random.randn(s.size)
            new_nest[j, :] = s
        return new_nest

    @staticmethod
    def empty_nests(nest, pa):

        pm1 = nest.copy()
        pm2 = nest.copy()

        random.shuffle(pm1)
        random.shuffle(pm2)

        K = np.random.uniform(low=0, high=1, size=nest.shape) > pa

        step_size = np.random.uniform(low=0, high=1) * (pm2 - pm1)

        new_nest = nest.copy() + step_size * K

        return new_nest
