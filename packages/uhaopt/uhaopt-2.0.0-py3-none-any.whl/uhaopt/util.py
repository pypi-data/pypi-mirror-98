from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import os
import numpy as np


def dump_results(save_directory, solution, cost_dic, current_evaluation, initial_population):
    """
    The configurations are saved into a file named 'configs.json', while 'results.json' is used\
    to save the metrics. The results also contain initial population, final population and their associated\
    metrics. Here, the output formats are json and CSV, which let's the user to do post_processing\
    using an arbitrary tool.\


    :param save_directory: The output directory for each single run. If the 'configs.json' and 'results.json'\
    already exist, the algorithm will append the new results into these files. In the case of population and\
    their associated costs it will overwrite the results.\

    :param solution: A valid generated configuration. We don't save the invalid solutions because they don't\
    have any metric to measure.\

    :param cost_dic: The associated metrics for each solution. Here, test_accuracy, training_time, trainable_parameters,\
    validation_accuracy and train_accuracy are measured.\

    :param current_evaluation: The number of evaluations that is already passed. We are interested to verify the\
    convergence rate of our proposed algorithm and this parameyer will help us to do so.\

    :param initial_population: This flag denotes whether the generated configurations belong to the initial population\
    or not.

    """
    configs = [0, 0, current_evaluation]

    particle_dic = {}
    for i in range(len(solution)):
        particle_dic['p' + str(i)] = solution[i]

    configs.append(particle_dic)
    configs.append({"model_based_pick": not initial_population})

    data = []
    path = os.path.join(save_directory, 'configs.json')
    if os.path.isfile(path):
        with open(path) as f:
            for line in f:
                data.append(json.loads(line))
    else:
        os.makedirs(save_directory, exist_ok=True)

    with open(path, 'w') as fp:
        for item in data:
            json.dump(item, fp)
            fp.write('\n')
        json.dump(configs, fp)

    results = [current_evaluation, cost_dic]

    data = []
    path = os.path.join(save_directory, 'results.json')
    if os.path.isfile(path):
        with open(path) as f:
            for line in f:
                data.append(json.loads(line))
    else:
        os.makedirs(save_directory, exist_ok=True)

    with open(path, 'w') as fp:
        for item in data:
            json.dump(item, fp)
            fp.write('\n')
        json.dump(results, fp)


def check_bounds(solution, bounds):
    """
    Bound constrained optimization problems consider the problem\
    of optimizing an objective function subject to bound constraints\
    on the values of the variables.\


    :param solution: A new generated configuration in the form of a 1-D array\


    :param bounds: Bounds for variables.  ``(min, max)`` pairs for each element in ``x``,\
    defining the lower and upper bounds for the optimizing argument of\
    `func`. It is required to have ``len(bounds) == len(x)``.\
    """
    if bounds is None:
        return solution

    # check for constraint violations
    for d in range(len(solution)):
        if bounds[d][0] is not None and solution[d] < bounds[d][0]:
            solution[d] = bounds[d][0]
        elif bounds[d][1] is not None and solution[d] > bounds[d][1]:
            solution[d] = bounds[d][1]

    return solution


def area_sphere(dimension, radius):
    """*  ******* Random point in a hypersphere ********
    Put  a random point inside the hypersphere S(0,radius) (center 0, radius 1).

    Developed by: Maurice Clerc (May 2011)"""
    x = []
    for i in range(dimension):
        x.append(gaussian_random_number(mean=0, std_dev=1.0))

    l = np.linalg.norm(x, 2)

    return np.random.rand() * radius * np.array(x) / l


def gaussian_random_number(mean, std_dev):
    """Use the polar form of the Box-Muller transformation to obtain a pseudo
    random number from a Gaussian distribution

    Developed by: Maurice Clerc (May 2011)"""

    w = 2
    while w >= 1:
        x1 = 2.0 * np.random.rand() - 1.0
        x2 = 2.0 * np.random.rand() - 1.0
        w = x1 * x1 + x2 * x2

    w = np.sqrt(-2.0 * np.log(w) / w)
    y1 = x1 * w

    if np.random.rand() < 0.5:
        y1 = y1 * -1

    return y1 * std_dev + mean


def calculate_cost_abc(cost):
    if cost >= 0:
        cost = 1 / (cost + 1)
    else:
        cost = 1 + np.abs(cost)

    return cost


def mu_inv(y, mu):
    x = (((1 + mu) ** abs(y) - 1) / mu) * np.sign(y)
    return x
