"""
The Artificial Bee Colony (ABC) algorithm is a swarm based meta-heuristic algorithm that was
introduced by Karaboga in 2005 [1-2] for optimizing numerical problems. It was inspired
by the intelligent foraging behavior of honey bees. The algorithm consists of three essential
components: employed and unemployed foraging bees, and food sources. The first two components,
employed and unemployed foraging bees, search for rich food sources, which is the third component,
close to their hive. The model also defines two leading modes of behaviour which are necessary
for self-organizing and collective intelligence: recruitment of foragers to rich food sources
resulting in positive feedback and abandonment of poor sources by foragers causing negative feedback.

References

 [1] Karaboga, Dervis, and Bahriye Akay. "A comparative study of artificial bee colony algorithm."
 Applied mathematics and computation 214.1 (2009): 108-132.

 [2] http://www.scholarpedia.org/article/Artificial_bee_colony_algorithm

"""

import numpy as np
import random

from uhaopt.util import check_bounds
from uhaopt.util import dump_results
from uhaopt.util import calculate_cost_abc


class ABC:
    """

    :param cost_func: in ABC, a colony of artificial forager bees (agents) search for rich artificial food sources \
    (good solutions for a given problem). To apply ABC, the considered optimization problem is \
    first converted to the problem of finding the best parameter vector which minimizes a \
    cost function.\

    :param bounds: sequence of (min, max) pairs for each agent. None is used to specify no bound.\
    The search area for the agents is limited by their lower and upper bounds.\

    :param food_number: the artificial bees of the colony  are  categorized  into  three  main\
    groups:  employed  bees,  onlooker  bees,  and  scout  bees.  The number  of  employed  and\
    onlooker bees are equal to the population size and each bee is associated with each food source.\

    :param dimension: number of decision variables of the cost function.\

    :param limit: it  is  possible that the employed and onlooker  bees visit a  food source which\
    they cannot  improve. Therefore,  if  for  a predetermined  number  of cycles  (which  is\
    defined  by  a limit parameter)  a  food  source  cannot  be improved, then that food source\
    is abandoned and the employed bee associated with it becomes a scout bee. Thereafter, this\
    scout bee produces a new solution and again it transforms into an employed bee.\

    :param max_evaluations: the number of evaluations for evolving the\
    solutions (i.e., computational budgets)\
    :param tol: tolerance for termination.
    :param foods: an initial population of food sources.
    :param cost: the initial cost array for the associated individuals in the population.
    :param display: whether display the results on the output or not.
    :param save_directory: the configurations are saved into a file named 'configs.json', while 'results.json' is used\
    to save the metrics. the results also contain initial population, final population and their associated\
    metrics. Here, the output formats are json and CSV, which let's the user to do post_processing\
    using an arbitrary tool.
    :param save_results: you can save all the valid generated configurations and their associated metrics\
    to the output.
    """

    def __init__(self, cost_func=None, bounds=None, food_number=10, dimension=2, limit=100, max_evaluations=100,
                 tol=1.0e-4, foods=None, cost=None, display=True, save_directory=None, save_results=False):

        assert cost_func is not None, "Please pass a valid cost function for your optimization problems"

        assert len(bounds) == dimension, "The bounds and dimension parameters should have equal dimensions."

        if foods is None:

            foods = []
            for i in range(food_number):
                for j in range(dimension):
                    foods.append(random.uniform(bounds[j][0], bounds[j][1]))

            foods = np.array(foods).reshape((food_number, dimension))

        function_evaluations = 0
        cost_real = []
        if cost is None:
            cost = []
            for food in foods:
                cost_p = cost_func(food)

                if type(cost_p) is not float:

                    function_evaluations = function_evaluations + 1
                    if save_results:
                        dump_results(save_directory=save_directory, solution=food, cost_dic=cost_p,
                                     current_evaluation=function_evaluations, initial_population=True)
                else:
                    dump_results(save_directory=save_directory, solution=food, cost_dic=cost_p,
                                 current_evaluation=function_evaluations, initial_population=True)
                cost_real.append(cost_p)

                cost.append(calculate_cost_abc(cost_p))

                if (min(cost_real) < tol) or (function_evaluations >= max_evaluations):
                    return
            cost = np.array(cost)
        trial = np.zeros(food_number)

        while True:
            for i in range(food_number):
                param2change = np.random.randint(low=0, high=dimension)
                neighbour = np.random.randint(low=0, high=food_number)

                while neighbour == i:
                    neighbour = np.random.randint(low=0, high=food_number)

                sol = foods[i, :].copy()

                sol[param2change] = foods[i, param2change] + (
                        foods[i, param2change] - foods[neighbour, param2change]) * (np.random.rand() - 0.5) * 2

                sol = check_bounds(solution=sol, bounds=bounds)

                cost_sol = cost_func(sol)

                if type(cost_sol) is not float:

                    function_evaluations = function_evaluations + 1
                    if save_results:
                        dump_results(save_directory=save_directory, solution=sol, cost_dic=cost_sol,
                                     current_evaluation=function_evaluations, initial_population=True)
                else:
                    dump_results(save_directory=save_directory, solution=sol, cost_dic=cost_sol,
                                 current_evaluation=function_evaluations, initial_population=True)

                cost_real.append(cost_sol)
                if (min(cost_real) < tol) or (function_evaluations >= max_evaluations):
                    return
                if display:
                    print(['The best solution after ', function_evaluations, 'evaluations is: ', min(cost_real)])

                cost_sol = calculate_cost_abc(cost_sol)

                if cost_sol > cost[i]:
                    foods[i, :] = sol
                    cost[i] = cost_sol
                    trial[i] = 0
                else:
                    trial[i] = trial[i] + 1

            prob = (0.9 * cost / np.max(cost)) + 0.1

            i = 0
            t = 0

            while t < food_number:
                if np.random.rand() < prob[i]:
                    t = t + 1
                    param2change = np.random.randint(low=0, high=dimension)
                    neighbour = np.random.randint(low=0, high=food_number)

                    while neighbour == i:
                        neighbour = np.random.randint(low=0, high=food_number)

                    sol = foods[i, :].copy()

                    sol[param2change] = foods[i, param2change] + (
                            foods[i, param2change] - foods[neighbour, param2change]) * (np.random.rand() - 0.5) * 2

                    sol = check_bounds(solution=sol, bounds=bounds)

                    cost_sol = cost_func(sol)

                    if type(cost_sol) is not float:

                        function_evaluations = function_evaluations + 1
                        if save_results:
                            dump_results(save_directory=save_directory, solution=sol, cost_dic=cost_sol,
                                         current_evaluation=function_evaluations, initial_population=True)
                    else:
                        dump_results(save_directory=save_directory, solution=sol, cost_dic=cost_sol,
                                     current_evaluation=function_evaluations, initial_population=True)

                    cost_real.append(cost_sol)

                    if (min(cost_real) < tol) or (function_evaluations >= max_evaluations):
                        return
                    if display:
                        print(['The best solution after ', function_evaluations, 'evaluations is: ', min(cost_real)])

                    cost_sol = calculate_cost_abc(cost_sol)

                    if cost_sol > cost[i]:
                        foods[i, :] = sol
                        cost[i] = cost_sol
                        trial[i] = 0
                    else:
                        trial[i] = trial[i] + 1
                i = i + 1

                if i == food_number:
                    i = 0

            ind = np.argmax(trial)

            if trial[ind] > limit:
                trial[ind] = 0
                sol = []
                for j in range(dimension):
                    sol.append(random.uniform(bounds[j][0], bounds[j][1]))
                sol = np.array(sol)
                sol = check_bounds(solution=sol, bounds=bounds)

                cost_sol = cost_func(sol)

                if type(cost_sol) is not float:

                    function_evaluations = function_evaluations + 1
                    del cost_sol['module_adjacency']
                    del cost_sol['module_operations']
                    if save_results:
                        dump_results(save_directory=save_directory, solution=sol, cost_dic=cost_sol,
                                     current_evaluation=function_evaluations, initial_population=True)
                    cost_sol = cost_sol['validation_accuracy'] * -1
                else:
                    dump_results(save_directory=save_directory, solution=sol, cost_dic=cost_sol,
                                 current_evaluation=function_evaluations, initial_population=True)
                cost_real.append(cost_sol)

                if (min(cost_real) < tol) or (function_evaluations >= max_evaluations):
                    return
                if display:
                    print(['The best solution after ', function_evaluations, 'evaluations is: ', min(cost_real)])

                foods[ind, :] = sol
                cost[ind] = calculate_cost_abc(cost_sol)
