'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/population.py
Path: /home/shapedsundew9/Projects/Erasmus/src
Created Date: Friday, January 17th 2020, 4:38:35 pm
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''

from genetics.agent import agent
from numpy import zeros, float32
from cull_policies import cull_r000


class population():

    def __init__(self, fitness_function, initial_size=100, size_limit=1000, cull_policy=None):
        self.agents = [agent() for i in range(initial_size)]
        self.fitness_score = zeros((size_limit), dtype=float32)
        self._cull_policy = cull_policy
        self._size_limit = size_limit
        self._fitness_function = fitness_function


    def next_generation(self, attempts=100):
        for a in self.agents:
            offspring = a.reproduce()
            if not offspring is None:
                if len(self.agents) >= self._size_limit:
                    self._replaceagents(self.cull_list(), [offspring])
                else:    
                    self._add_agent(offspring)


    def _add_agent(self, offspring):
        self.agents.append(offspring)
        self.fitness_score[len(self.agents) - 1] = self._fitness_function(offspring)
    

    def _replaceagents(self, indexes, newagents):
        for i, a in zip(indexes, newagents):
            self.agents[i] = a
            self.fitness_score[i] = self._fitness_function(a) 


    def cull_list(self, num=1):
        return cull_r000.cull(self, num) if self._cull_policy is None else self._cull_policy.cull(self, num)




