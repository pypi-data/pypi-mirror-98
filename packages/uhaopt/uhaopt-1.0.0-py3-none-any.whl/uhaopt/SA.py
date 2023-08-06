"""Simulated annealing (SA) is a probabilistic technique for approximating the
global optimum of a given function. Specifically, it is a metaheuristic to
approximate global optimization in a large search space for an optimization
problem. It is often used when the search space is discrete (e.g., all tours
that visit a given set of cities). For problems where finding an approximate
global optimum is more important than finding a precise local optimum in a
fixed amount of time, simulated annealing may be preferable to alternatives
such as gradient descent.

The name and inspiration come from annealing in metallurgy, a technique involving
heating and controlled cooling of a material to increase the size of its crystals
and reduce their defects. Both are attributes of the material that depend on
its thermodynamic free energy. Heating and cooling the material affects both
the temperature and the thermodynamic free energy. The simulation of annealing
can be used to find an approximation of a global minimum for a function with
a large number of variables.

References

    [1] Das, A., & Chakrabarti, B. K. (Eds.). (2005). Quantum annealing\
    and related optimization methods (Vol. 679). Springer Science & Business Media.\


    [2] Weinberger, E. (1990). Correlated and uncorrelated fitness landscapes and how\
    to tell the difference. Biological cybernetics, 63(5), 325-336.\


    [3] https://en.wikipedia.org/wiki/Simulated_annealing\

    [4] Aarts, E., & Korst, J. (1988). Simulated annealing and Boltzmann machines.

    [5] Kirkpatrick, S., Gelatt, C. D., & Vecchi, M. P. (1983). Optimization by
    simulated annealing. science, 220(4598), 671-680.

"""

import numpy as np
import random

from uhaopt.util import check_bounds
from uhaopt.util import dump_results
from uhaopt.util import mu_inv


class SA:

    """

    :param cost_func: a cost/loss function is a function that maps an event or values of one or more variables onto\
    a real number intuitively representing some "cost" associated with the event.\

    :param bounds: sequence of (min, max) pairs for each solution. None is used to specify no bound.\

    :param repeat_num: a decrement criteria for temperature.\

    :param dimension: number of decision variables of the cost function\

    :param max_evaluations: the number of evaluations for evolving the\
    solutions (i.e., computational budgets)\

    :param tol: tolerance for termination.\

    :param x0: an initial solution vector in the form of a 1-D array.\

    :param cost: the initial cost array for the associated solutions in the population.\

    :param display: whether display the results on the output or not.\

    :param save_directory: the configurations are saved into a file named 'configs.json', while 'results.json' is used\
    to save the metrics. the results also contain initial population, final population and their associated\
    metrics. Here, the output formats are json and CSV, which let's the user to do post_processing\
    using an arbitrary tool.

    :param save_results: you can save all the valid generated configurations and their associated metrics\
    to the output.
    """

    def __init__(self, cost_func=None, bounds=None, repeat_num=10, dimension=2, max_evaluations=100,
                 tol=1.0e-4, x0=None, cost=None, display=True, save_directory=None, save_results=False):

        assert cost_func is not None, "Please pass a valid cost function for your optimization problems"
        assert len(bounds) == dimension, "The bounds and dimension parameters should have equal dimensions."

        Mmax = int(max_evaluations * 2 / repeat_num)

        if x0 is None:

            x0 = []

            for j in range(dimension):
                x0.append(random.uniform(bounds[j][0], bounds[j][1]))

            x0 = np.array(x0).reshape(dimension)

        function_evaluations = 0

        if cost is None:
            cost = []
            cost_p = cost_func(x0)

            if type(cost_p) is not float:

                function_evaluations = function_evaluations + 1
                if save_results:
                    dump_results(save_directory=save_directory, solution=x0, cost_dic=cost_p,
                                 current_evaluation=function_evaluations, initial_population=True)
            else:
                if save_results:
                    dump_results(save_directory=save_directory, solution=x0, cost_dic=cost_p,
                                 current_evaluation=function_evaluations, initial_population=True)
            cost.append(cost_p)

            if (min(cost) < tol) or (function_evaluations >= max_evaluations):
                return
            cost = np.array(cost)

        x = x0.copy()
        fx = cost
        f0 = fx
        for m in range(Mmax):
            T = m / Mmax
            mu = 10 ** (T * 100)

            for k in range(repeat_num):
                dx = mu_inv(2 * np.random.rand(x.size) - 1, mu)
                for i in range(len(x)):
                    dx[i] = dx[i] * (bounds[i][1] - bounds[i][0])

                trial_x = x.copy() + dx

                trial_x = check_bounds(solution=trial_x, bounds=bounds)
                trial_cost = cost_func(trial_x)

                if type(trial_cost) is not float:

                    function_evaluations = function_evaluations + 1
                    if save_results:
                        dump_results(save_directory=save_directory, solution=trial_x, cost_dic=trial_cost,
                                     current_evaluation=function_evaluations, initial_population=False)
                else:
                    if save_results:
                        dump_results(save_directory=save_directory, solution=trial_x, cost_dic=trial_cost,
                                     current_evaluation=function_evaluations, initial_population=False)

                df = trial_cost - fx

                if (df < 0) or (np.random.rand() < np.exp(-T * df / (np.abs(fx) + np.finfo(float).eps) / tol)):
                    x = trial_x.copy()
                    fx = trial_cost

                if fx < f0:
                    f0 = fx

                if (f0 < tol) or (function_evaluations >= max_evaluations):
                    return

                if display:
                    print(['The best solution after ', function_evaluations, 'evaluations is: ', f0])
