'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/population.py
Path: /home/shapedsundew9/Projects/Erasmus/src
Created Date: Friday, January 17th 2020, 4:38:35 pm
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''

from genetics.agent import agent
from numpy import zeros, float32
from cull_policies import random_cull


class population():

    def __init__(self, fitness_function, initial_size=100, size_limit=1000, cull_policy=None):
        self._agents = [agent() for i in range(initial_size)]
        self._fitness_score = zeros((size_limit), dtype=float32)
        self._cull_policy = cull_policy
        self._size_limit = size_limit
        self._fitness_function = fitness_function


    def next_generation(self, attempts=100):
        for a in self._agents:
            offspring = a.reproduce()
            if not offspring is None:
                if len(self._agents) >= self._size_limit: self.cull()
                self._add_agent(offspring)


    def _add_agent(self, offspring):
        self._agents.append(offspring)
        self._fitness_score[len(self._agents) - 1] = self._fitness_function(offspring)
    

    def cull(self, num=1):
        if self._cull_policy is None:
            random_cull(self, num)
        else:
            self._cull_policy(self, num)





