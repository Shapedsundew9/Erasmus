'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/population.py
Path: /home/shapedsundew9/Projects/Erasmus/src
Created Date: Friday, January 17th 2020, 4:38:35 pm
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''

from numpy import zeros, float32, append
from .genetics.agent import agent
from .cull_policies import cull_r000
from logging import getLogger
from .genetics.genomic_library import genomic_library


class population():


    _logger = getLogger(__name__)
    _glib = genomic_library()


    def __init__(self, fitness_function, initial_size=100, size_limit=1000, cull_policy=None):
        self.agents = [agent() for _ in range(initial_size)]
        self.fitness_score = zeros((size_limit), dtype=float32)
        self.cull_policy = cull_r000() if cull_policy is None else cull_policy()
        self._size_limit = size_limit
        self.fitness_function = fitness_function
        self.generation = 0
        self.best_fitness = 0.0


    def __len__(self):
        return len(self.agents)


    def next_generation(self, attempts=100, min_fitness=None):
        population._logger.info("Breeding generation %d from population of %d", self.generation + 1, len(self.agents))
        # self.agents gets modified in the loop
        for i in range(len(self.agents)):
            a = self.agents[i]
            offspring = a.reproduce()
            if not offspring is None:
                if len(self.agents) >= self._size_limit:
                    self._replace_agents(self.cull_list(), [offspring])
                else:    
                    self._add_agent(offspring)
            self.best_fitness = self.fitness_score.max()

            # Early stopping
            if not min_fitness is None and self.best_fitness >= min_fitness: break
        self.generation += 1
        population._logger.info("Generation %d population is %d with a best fitness of %0.2f", self.generation, len(self.agents), self.best_fitness)
        self.add_population_to_library()
 

    def evolve_until(self, min_fitness=1.0, generation_limit=1000):
        while self.best_fitness < min_fitness and generation_limit:
            self.next_generation()
            generation_limit -= 1


    def add_population_to_library(self):
        added = 0
        for a in self.agents: added += a.add_code_to_library()
        population._logger.info("Added %d genetic_codes to library. Library now %d codes.", added, len(self._glib))


    def set_size_limit(self, size_limit):
        if size_limit > self._size_limit:
            delta = int(size_limit - self._size_limit)
            self.fitness_score = append(self.fitness_score, zeros((delta)))
            population._logger.info("Increased maximum population from %d to %d", self._size_limit, size_limit)
        if size_limit < self._size_limit:
            delta = int(self._size_limit - size_limit)
            agent_delta = int(len(self.agents - size_limit))
            if agent_delta > 0: cull_list = self.cull_policy(agent_delta)
            for index in sorted(cull_list, reverse=True): del self.agents[index]
            self.fitness_score = zeros((size_limit), dtype=float32)
            for i, a in enumerate(self.agents): self.fitness_score[i] = self.fitness_function(a)
            population._logger.info("Decreased maximum population from %d to %d", self._size_limit, size_limit)
        self._size_limit = size_limit


    def _add_agent(self, offspring):
        self.agents.append(offspring)
        self.fitness_score[len(self.agents) - 1] = self.fitness_function(offspring)
        population._logger.debug("Added new agent with fitness score %f", self.fitness_score[len(self.agents) - 1])
    

    def _replace_agents(self, indexes, newagents):
        for i, a in zip(indexes, newagents):
            self.agents[i] = a
            self.fitness_score[i] = self.fitness_function(a) 
            population._logger.debug("Replaced agent %d with new agent with fitness score %f", i, self.fitness_score[i])


    def cull_list(self, num=1):
        return self.cull_policy.cull(self, num)




