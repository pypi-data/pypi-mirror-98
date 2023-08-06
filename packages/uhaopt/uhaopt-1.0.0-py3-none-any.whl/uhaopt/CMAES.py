"""
CMA-ES stands for covariance matrix adaptation evolution strategy. Evolution strategies (ES)
are stochastic, derivative-free methods for numerical optimization of non-linear or non-convex
continuous optimization problems [1-2]. They belong to the class of evolutionary algorithms
and evolutionary computation.

References

    [1] Hansen, N., & Kern, S. (2004, September). Evaluating the CMA evolution strategy on multimodal\
     test functions. In International Conference on Parallel Problem Solving from Nature (pp. 282-291).\
      Springer, Berlin, Heidelberg.\


    [2] https://en.wikipedia.org/wiki/CMA-ES\

"""

from cma import purecma as pcma
import numpy as np
import random

from uhaopt.util import check_bounds
from uhaopt.util import dump_results


class CMAES:

    """

    :param cost_func: a cost/loss function is a function that maps an event or values of one or more variables onto\
    a real number intuitively representing some "cost" associated with the event.\

    :param bounds: sequence of (min, max) pairs for each particle. None is used to specify no bound.\

    :param sigma: sigma determines the initial coordinate wise standard deviations for the search.\

    :param dimension: number of decision variables of the cost function\

    :param max_evaluations: the number of evaluations for evolving the\
    solutions (i.e., computational budgets)\
    :param tol: tolerance for termination.\

    :param x0: an initial solution vector in the form of a 1-D array.\

    :param display: whether display the results on the output or not.\

    :param save_directory: the configurations are saved into a file named 'configs.json', while 'results.json' is used\
    to save the metrics. the results also contain initial population, final population and their associated\
    metrics. Here, the output formats are json and CSV, which let's the user to do post_processing\
    using an arbitrary tool.\

    :param save_results:  you can save all the valid generated configurations and their associated metrics\
    to the output.\
    """

    def __init__(self, cost_func=None, bounds=None, sigma=0.5, dimension=2, max_evaluations=100,
                 tol=1.0e-4, x0=None, display=True, save_directory=None, save_results=False):

        assert cost_func is not None, "Please pass a valid cost function for your optimization problems"
        assert len(bounds) == dimension, "The bounds and dimension parameters should have equal dimensions."

        if x0 is None:

            x0 = []

            for j in range(dimension):
                x0.append(random.uniform(bounds[j][0], bounds[j][1]))

            x0 = np.array(x0).reshape(dimension)

        function_evaluations = 0
        es = pcma.CMAES(x0, sigma, maxfevals=max_evaluations * 1000)
        f0 = np.inf

        # this loop resembles the method optimize
        while function_evaluations <= max_evaluations:  # iterate
            x = es.ask()  # get candidate solutions
            fs = []
            for solutions in x:
                solutions = check_bounds(solution=solutions, bounds=bounds)
                f = cost_func(solutions)

                if type(f) is not float:

                    function_evaluations = function_evaluations + 1
                    if save_results:
                        dump_results(save_directory=save_directory, solution=solutions, cost_dic=f,
                                     current_evaluation=function_evaluations, initial_population=False)
                else:
                    if save_results:
                        dump_results(save_directory=save_directory, solution=solutions, cost_dic=f,
                                     current_evaluation=function_evaluations, initial_population=False)

                fs.append(f)
                if f < f0:
                    f0 = f

                if (f0 < tol) or (function_evaluations >= max_evaluations):
                    return

                if display:
                    print(['The best solution after ', function_evaluations, 'evaluations is: ', f0])

            es.tell(x, fs)  # do all the real work
