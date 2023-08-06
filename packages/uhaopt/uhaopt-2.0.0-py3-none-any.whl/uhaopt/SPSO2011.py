""" In computational science, particle swarm optimization (PSO)[1-2] is a computational method
that optimizes a problem by iteratively trying to improve a candidate solution with regard
to a given measure of quality. It solves a problem by having a population of candidate solutions,
here dubbed particles, and moving these particles around in the search-space according to simple
mathematical formulae over the particle's position and velocity. Each particle's movement is
influenced by its local best known position, but is also guided toward the best known positions
in the search-space, which are updated as better positions are found by other particles.
This is expected to move the swarm toward the best solutions.

PSO is originally attributed to Kennedy, Eberhart and Shi[1-3] and was first intended for
simulating social behaviour, as a stylized representation of the movement of organisms in
a bird flock or fish school. Currently, three very similar versions of PSO are available that could be called
“standard”. Here, we implemented the last version.\


References

    [1] Kennedy, J. (2010). Particle swarm optimization. Encyclopedia of machine learning, 760-766.


    [2] Eberhart, R., & Kennedy, J. (1995, October). A new optimizer using particle swarm theory.
    In MHS'95. Proceedings of the Sixth International Symposium on Micro Machine and Human Science (pp. 39-43). Ieee.


    [3] https://en.wikipedia.org/wiki/Particle_swarm_optimization\

"""
import numpy as np
import random

from uhaopt.util import check_bounds
from uhaopt.util import dump_results
from uhaopt.util import area_sphere

__author__ = "Hojjat Rakhshani"
__license__ = "MIT"
__email__ = "hojjat.rakhshani@uha.fr"
__status__ = "Development"

class PSO:

    """
    :param cost_func: A cost/loss function is a function that maps an event or values of one or more variables onto\
    a real number intuitively representing some "cost" associated with the event. SPSO seeks to minimize a loss function.

    :param bounds: Sequence of (min, max) pairs for each particle. None is used to specify no bound.
    :param swarm_size: The number of desired particles in the swarm
    :param dimension: Number of decision variables
    :param w: The inertia weigh parameter
    :param c1: Acceleration coefficient c1
    :param c2: Acceleration coefficient c2
    :param k: K neighbors for each particle -- based on Clerc description http://clerc.maurice.free.fr/pso/random_topology.pdf, P. 2 (Method 2)
    :param p: Probability to be an informant
    :param max_evaluations: The number of function evaluations for evolving the solutions
    :param tol: Tolerance for termination.
    :param swarm: An initial population of particles
    :param velocity: The particles move around in the search-space according to simple mathematical formulae over the particle's position using\
    it's velocity. For each particle, the velocity movement is influenced by its local best known position, but is also guided toward the best\
    known positions in the search-space, which are updated as better positions are found by other particles. This is expected to move the swarm\
    toward the best solutions.\

    :param cost: The initial cost array for the associated particles in the swarm.
    """

    def __init__(self, cost_func=None, bounds=None, swarm_size=40, dimension=2, w=1 / (2 * np.log(2)),
                 c1=0.5 + np.log(2), c2=0.5 + np.log(2), k=3, p=None, max_evaluations=100, tol=0.0, swarm=None,
                 velocity=None, cost=None, display=True, save_directory=None, save_results=False):

        assert cost_func is not None, "Please pass a valid cost function for your optimization problems"
        assert len(bounds) == dimension, "The bounds and dimension parameters should have equal dimensions."

        if swarm is None:

            swarm = []
            for i in range(swarm_size):
                for j in range(dimension):
                    swarm.append(random.uniform(bounds[j][0], bounds[j][1]))

            swarm = np.array(swarm).reshape((swarm_size, dimension))

        if velocity is None:
            velocity = []
            for i in range(swarm_size):
                for j in range(dimension):
                    velocity.append(random.uniform(bounds[j][0] - swarm[i, j], bounds[j][1] - swarm[i, j]))

            velocity = np.array(velocity).reshape((swarm_size, dimension))

        assert swarm.shape[0] == velocity.shape[0] and swarm.shape[1] == velocity.shape[
            1], "swarm and velocity should have equal dimensions"

        function_evaluations = 0

        if cost is None:
            cost = []
            for particle in swarm:

                cost_p = cost_func(particle)
                if type(cost_p) is not float:

                    function_evaluations = function_evaluations + 1
                    if save_results:
                        dump_results(save_directory=save_directory, solution=particle, cost_dic=cost_p,
                                     current_evaluation=function_evaluations, initial_population=True)
                else:
                    if save_results:
                        dump_results(save_directory=save_directory, solution=particle, cost_dic=cost_p,
                                     current_evaluation=function_evaluations, initial_population=True)
                cost.append(cost_p)

                if (min(cost) < tol) or (function_evaluations >= max_evaluations):
                    return

            cost = np.array(cost)

        p_x = swarm.copy()
        p_f = cost.copy()

        best_cost = np.min(p_f)

        if p is None:
            p = 1 - np.power(1 - (1 / swarm_size), k)  # probability to be an informant

        stag = True
        stop = False

        while not stop:

            if stag:
                L = np.eye(swarm_size, swarm_size)

                for s in range(swarm_size):
                    for r in range(swarm_size):
                        if r != s and np.random.rand() < p:
                            L[s, r] = 1
                stag = False

            for i in range(swarm_size):
                MIN = np.inf
                for s in range(swarm_size):
                    if L[s, i] == 1 and p_f[s] <= MIN:
                        MIN = p_f[s]
                        g_best = s

                p_x_p = swarm[i, :] + c1 * (p_x[i, :] - swarm[i, :])

                p_x_l = swarm[i, :] + c2 * (p_x[g_best, :] - swarm[i, :])

                if g_best == i:
                    G = 0.5 * (swarm[i, :] + p_x_p)
                else:
                    sw = 1 / 3
                    G = sw * (swarm[i, :] + p_x_p + p_x_l)

                rad = np.linalg.norm(G - swarm[i, :], 2)

                x_p = area_sphere(dimension, rad) + G

                velocity[i, :] = w * velocity[i, :] + x_p - swarm[i, :]

                swarm[i, :] = swarm[i, :] + velocity[i, :]

                swarm[i, :] = check_bounds(solution=swarm[i, :], bounds=bounds)
                velocity_bounds = velocity.copy() * -0.5
                velocity[i, :] = check_bounds(solution=velocity[i, :], bounds=velocity_bounds)

                cost_p = cost_func(swarm[i])

                if type(cost_p) is not float:

                    function_evaluations = function_evaluations + 1
                    if save_results:
                        dump_results(save_directory=save_directory, solution=swarm[i], cost_dic=cost_p,
                                     current_evaluation=function_evaluations, initial_population=True)
                else:
                    if save_results:
                        dump_results(save_directory=save_directory, solution=swarm[i], cost_dic=cost_p,
                                     current_evaluation=function_evaluations, initial_population=True)

                cost[i] = cost_p
                if (best_cost < tol) or (function_evaluations >= max_evaluations):
                    break
                if display:
                    print(['The best solution after ', function_evaluations, 'evaluations is: ', min(cost)])

            for i in range(swarm_size):
                if cost[i] <= p_f[i]:
                    p_x[i, :] = swarm[i, :]
                    p_f[i] = cost[i]

            b_f = np.min(p_f)

            if b_f < best_cost:
                best_cost = b_f
                stag = False
            else:
                stag = True

            if (best_cost < tol) or (function_evaluations >= max_evaluations):
                stop = True
