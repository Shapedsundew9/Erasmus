'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/locales/io.py
Path: /home/shapedsundew9/Projects/Erasmus/src/locales
Created Date: Tuesday, January 21st 2020, 6:13:41 pm
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''

from random import choice
from numpy.random import randint, shuffle
from numpy import array, finfo, iinfo, int32, prod, isclose, absolute, sqrt, float32, mean, arange
_MIN_SCALAR = iinfo(int32).min
_MAX_SCALAR = iinfo(int32).max
_MIN_FLOAT32 = finfo(float32).min
_MAX_FLOAT32 = finfo(float32).max
_MIN_VECTOR = 1
_MAX_VECTOR = 128
TESTS_IN_SET = 10


def scalar_identity():
    ret_val = []
    for _ in range(TESTS_IN_SET):
        i = array([randint(_MIN_SCALAR, _MAX_SCALAR)])
        ret_val.append((array(i, dtype=float32), array(i, dtype=float32)))
    return ret_val


def identity_fitness(agent, environment, attempts=1, small_set=None):
    indices = arange(len(environment), dtype=int32)
    shuffle(indices)
    inputs, target = environment[indices[0]]
    output = agent.exec(inputs)

    # If nothing was returned fitness = 0.0
    if output is None or not output.shape[0]: return 0.0

    # Fitness 0.0 < fitness < 1.0 is when the shape of the output is not the same as the target
    fitness = prod(target.shape) / prod(output.shape)
    if fitness > 1.0: fitness = 1.0 / fitness
    if not isclose(fitness, 1.0): return fitness

    # Fitness 1.0 < fitness < 2.0 is when the shape is right but the values expected
    # for the first target sample are not the same
    fitness = mean(sqrt(absolute(target - output)))
    if not isclose(fitness, 0.0): return 1.0 + 1.0 / fitness

    # Fitness 2.0 < fitness < 3.0 is when the shape and first target values are as expected
    # but the second, randomly chosen, target values are not as expected. If this target
    # is an outlier that may be unfair so 'attempts' can be set to choose other
    # random samples 
    if len(environment) > 1:
        best_fitness = _MAX_FLOAT32
        for i in indices[1:1 + attempts]:
            inputs, target = environment[i]
            output = agent.exec(inputs)
            fitness = float32(mean(sqrt(absolute(target - output))))
            if fitness < best_fitness: best_fitness = fitness
            if isclose(fitness, 0.0): break
        if not isclose(fitness, 0.0): return 2.0 + 1.0 / fitness
    
    # If small_set is defined a random subset of the environment will
    # be assessed to give 3.0 < fitness < 4.0
    if len(environment) > (1 + attempts) and not small_set is None:
        fitness = float32(0.0)
        end_small_set = min(len(environment), 1 + attempts + small_set)
        for i in indices[1 + attempts: end_small_set]:
            inputs, target = environment[i]
            output = agent.exec(inputs)
            fitness += float32(mean(sqrt(absolute(target - output))))
            if isclose(fitness, 0.0): break
        if not isclose(fitness, 0.0): return 3.0 + 1.0 / fitness

    # All remaining samples in the environment are assessed to give
    # 4.0 < fitness <= 5.0
    start = 1 + attempts + small_set if not small_set is None else 1 + attempts
    if start < len(environment):
        fitness = float32(0.0)
        for i in indices[start:]:
            inputs, target = environment[i]
            output = agent.exec(inputs)
            fitness += float32(mean(sqrt(absolute(target - output))))
            if isclose(fitness, 0.0): break
        if not isclose(fitness, 0.0): return 4.0 + 1.0 / fitness

    return 5.0


def _D_identity(num=1):
    ret_val = []
    for _ in range(TESTS_IN_SET):
        i = array(randint(_MIN_SCALAR, _MAX_SCALAR, size=(randint(_MIN_VECTOR, _MAX_VECTOR, size=num))), dtype=float32)
        ret_val.append((i, i))
    return ret_val


def oneD_identity():
    return _D_identity(1)
   

def twoD_identity():
    return _D_identity(2)


def threeD_identity():
    return _D_identity(3)


#TODO: Add n-dimensionsal version