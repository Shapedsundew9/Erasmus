'''
Filename: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics/worker.py
Path: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics
Created Date: Tuesday, May 5th 2020, 6:00:39 pm
Author: Shapedsundew9

Copyright (c) 2020 Your Company
'''

import sys
from .genetics import mutations as gm
from .genetics.mutations import meta_data
from .platform_info import get_platform_info
from .config import get_config, update_config
from .database_table import database_table
from .genetics.gene_pool import gene_pool
from .worker_registry_validator import worker_registry_validator
from .work_log_validator import work_log_validator
from .genetics.genomic_library_entry_validator import NULL_GC
from copy import deepcopy
from logging import getLogger
from math import isclose
from random import choice, choices, setstate, getrandbits
from numpy import float32, array, amax, amin, mean, median
from time import perf_counter, process_time
from psutil import Process
from importlib import reload
from os.path import getmtime, dirname, join


__DEFAULT_INITIAL_QUERY = [{'gca': NULL_GC, 'gcb': NULL_GC}]


class worker():


    __logger = getLogger(__name__)
    __worker_registry = None
    __work_registry = None
    __work_log_validator = work_log_validator()


    # fitness_function must be a callable that takes a callable func() and returns a single > 0.0 floating point fitness value. The bigger the better.
    # func() takes a numpy.array(dtype=numpy.float32) and returns a numpy.array(dtype=numpy.float32)
    # TODO: Decide what to do with fitness_function
    def __init__(self, worker_config, fitness_function):
        self.config = worker_config
        self.registration_document = { "platform": get_platform_info(), "work": worker_config['work'], "creator": worker_config['creator'] }
        validator = worker_registry_validator(get_config()['tables']['worker_registry']['schema'])
        if not validator.validate(self.registration_document):
            worker.__logger.error("Invalid worker registration document: %s", validator.errors)
            exit(1)
        self.registration_document = validator.normalized(self.registration_document)
        if worker.__worker_registry is None: worker.__worker_registry = database_table(worker.__logger, 'worker_registry')
        worker.__worker_registry.store([self.registration_document])
        if worker.__work_registry is None:  worker.__work_registry = database_table(worker.__logger, 'work_registry', True)
        self.__mutation_file_mtime = getmtime(gm.__file__)
        self.__mutation_keys = list(meta_data.keys())
        self.work = None
        self.__fitness_function = fitness_function
        self.gene_pool = None
        self.__work_log = None
        self.__log_data = {}


    def __function_not_found(self, name):
        worker.__logger.error("The dynamically determined function %s cannot be found.", name)


    def __valid_work(self, population):
        count = 0
        for signature, fitness in self.__calculate_fitness(population).items():
            if not isclose(population[signature], fitness):
                worker.__logger.warning("Fitness score for GC %s cannot be reproduced: Work registry fitness score %f versus worker fitness %f score",
                    signature, population[signature], fitness)
                count += 1
        if count:
            worker.__logger.warning("%d of %d (%0.2f%%) worker registry recorded fitness scores could not be reproduced by the worker.",
                count, len(population), 100.0 * count / len(self.work['population_dict']))
            return False
        worker.__logger.info("Worker was able to reproduce all of the registered work fitness scores.")
        return True


    def __calculate_fitness(self, population):
        return {signature: self.__fitness_function(self.gene_pool.callable(signature)) for signature in population.keys()}


    # TODO: Currently hard coded
    def __stop_criteria_met(self, population):
        for fitness in population.values():
            if fitness == 1.0: return True 
        return False


    def __mutate(self, gc, population):
        # FIXME: The selection of mutation candidates needs to be evolved
        mutation = choice(self.__mutation_keys)
        func = meta_data[mutation]['callable'] 
        # FIXME: The selection of a breeding partner needs to be evolved
        return func([gc]) if meta_data[mutation]['properties']['unary_mutation'] else func([gc, choice(population)])


    def __evolve(self, population):
        if getmtime(gm.__file__) > self.__mutation_file_mtime:
            worker.__logger.debug("%s", list(sys.modules.keys()))
            reload(sys.modules['microbiome.genetics.mutations'])
            from .genetics.mutations import meta_data
            self.__mutation_file_mtime = getmtime(gm.__file__)
            self.__mutation_keys = list(meta_data.keys())

        population_list = list(population.keys())
        new_gcs = [self.__mutate(self.gene_pool[signature], population_list) for signature in population.keys()]
        new_population = {ngc['signature']: 0.0 for ngc in new_gcs}
        self.gene_pool.update(new_population.keys())
        worker.__logger.debug("New population: %s", new_population)
        return new_population


    # TODO: This is currently hard coded.
    def __cull(self, population):
        self.__log_data['born'] = len(population) - self.work['population_limit']
        worker.__logger.debug("Population: %s", population)
        cull_list = [(k, 1.0 - v) for k, v in population.items()]
        cull_list.sort(key=lambda t: t[1])

        # Determine how many were still born
        num = len(cull_list)
        while cull_list and cull_list[-1] == 1.0: del population[cull_list.pop()[0]]
        self.__log_data['still_born'] = num - len(cull_list)
        self.__log_data['culled'] = 0

        if len(cull_list) > self.work['population_limit']:
            self.__log_data['culled'] = len(population) - self.work['population_limit']
            saved = int(0.5 * len(cull_list) + 0.5)
            cull_list = cull_list[saved:]
            weights = [t[1] for t in cull_list]
            for _ in range(self.__log_data['culled']):
                victim = choices(cull_list, weights)
                del population[cull_list[victim][0]]
                weights[victim] = 0.0
        return population


    def __log_work(self):
        self.__log_data['wall_clock_runtime'] = perf_counter() - self.__log_data['wall_clock_runtime']
        self.__log_data['cpu_runtme'] = process_time() - self.__log_data['cpu_runtme']
        self.__log_data['EGPOP'] = self.__log_data['cpu_runtme']
        self.__log_data['RSS'] = Process().memory_info().rss
        self.__log_data['worker'] = self.registration_document['signature']

        fitness_data = array([v for v in self.work['population_dict'].values()])
        self.__log_data['fitness_min'] = amin(fitness_data)
        self.__log_data['fitness_max'] = amax(fitness_data)
        self.__log_data['fitness_mean'] = mean(fitness_data)
        self.__log_data['fitness_median'] = median(fitness_data)

        gc_depth_data = array([self.gene_pool[k]['gc_depth'] for k in self.work['population_dict'].keys()])
        self.__log_data['gc_depth_min'] = amin(gc_depth_data)
        self.__log_data['gc_depth_max'] = amax(gc_depth_data)
        self.__log_data['gc_depth_mean'] = mean(gc_depth_data)
        self.__log_data['gc_depth_median'] = median(gc_depth_data)

        codon_depth_data = array([self.gene_pool[k]['codon_depth'] for k in self.work['population_dict'].keys()])
        self.__log_data['codon_depth_min'] = amin(codon_depth_data)
        self.__log_data['codon_depth_max'] = amax(codon_depth_data)
        self.__log_data['codon_depth_mean'] = mean(codon_depth_data)
        self.__log_data['codon_depth_median'] = median(codon_depth_data)

        gc_count_data = array([self.gene_pool[k]['gc_count'] for k in self.work['population_dict'].keys()])
        self.__log_data['gc_count_min'] = amin(gc_count_data)
        self.__log_data['gc_count_max'] = amax(gc_count_data)
        self.__log_data['gc_count_mean'] = mean(gc_count_data)
        self.__log_data['gc_count_median'] = median(gc_count_data)

        codon_count_data = array([self.gene_pool[k]['codon_count'] for k in self.work['population_dict'].keys()])
        self.__log_data['codon_count_min'] = amin(codon_count_data)
        self.__log_data['codon_count_max'] = amax(codon_count_data)
        self.__log_data['codon_count_mean'] = mean(codon_count_data)
        self.__log_data['codon_count_median'] = median(codon_count_data)

        self.__log_data = worker.__work_log_validator.normalized(self.__log_data)
        self.__work_log.store([self.__log_data])


    def __starting_log_data(self):
        self.__log_data = {
            'wall_clock_runtime': perf_counter(),
            'cpu_runtime': process_time()
        }


    def __handle_maximum_fitness(self, population):
        # TODO: pass mf to a function to handle the population that meet the maximum fitness.
        return [s for s, f in population.items() if f == 1.0]
        

    # Initialise
    # ----------
    # 1. Get latest work definition
    # 2a. Create the gene pool
    # 2b. Verify the fitness function produces the same results.
    #
    # Loop
    # ----
    # 3. Evolve state and assess (this updates the gene pool)
    # 4. Lock the work definition & read it (may have been updated by another worker)
    # 5a. Merge generations
    # 5b. Handle any GC's that have maximum fitness
    # 6. Cull
    # 7. Update work definition and unlock
    # 8. Log work results & stats
    # 9. Update gene pool
    # 10. Assess stopping criteria (and stop if met)
    # 11. Go to #3.
    def evolve(self):

        # Initialise
        self.work = worker.__work_registry.load([{'signature': self.registration_document['work']}])[0]
        work_log_table = 'work_' + self.work['signature'][:16] + '_log'
        update_config({'tables': {work_log_table: deepcopy(get_config()['tables']['work_log_template'])}})
        self.__work_log = database_table(worker.__logger, work_log_table)

        # TODO: Random state management
        # setstate(self.work['evolution_parameters']['random_state'])

        existing_population = len(self.work['population_dict'])
        if existing_population:
            worker.__logger.info("Exisiting population of %d individuals found in work registry.", existing_population)
            self.work['initial_query'] = [{'signature': list(self.work['population_dict'].keys())}]
        elif self.work['initial_query'] is None:
            worker.__logger.info("No exisiting population found in work registry and initial_query == None. Generating population from default query: %s.",
                __DEFAULT_INITIAL_QUERY)
            self.work['initial_query'] = __DEFAULT_INITIAL_QUERY
        else:
            worker.__logger.info("No exisiting population found in work registry. Generating from initial query: %s.", self.work['initial_query'])
        self.gene_pool = gene_pool(self.work['initial_query'], file_ptr=self.work['gene_pool'])
        self.work['population_dict'] = { s['signature']: 0.0 for s in self.gene_pool.gl(self.work['initial_query'], ['signature']) }   
        worker.__logger.info("Starting population of %d individuals loaded into gene pool.", len(self.work['population_dict']))

        if existing_population and not self.__valid_work(self.work['population_dict']):
            worker.__logger.error("Work definition is not consistent with existing work registration details. Worker config: %s", str(self.config))
            worker.__logger.error("Has the fitness function been modified?")
            exit(1)

        # Loop
        epoch = 1
        while not self.__stop_criteria_met(self.work['population_dict']):
            worker.__logger.info("Starting epoch %d.", epoch)
            self.__starting_log_data()
            worker.__logger.debug("Epoch %d. Initialised logging data.", epoch)

            population = self.__evolve(self.work['population_dict'])
            worker.__logger.debug("Epoch %d. Evolution completed.", epoch)

            population = self.__calculate_fitness(population)
            worker.__logger.debug("Epoch %d. Fitness calculated.", epoch)

            population.update(worker.__work_registry.load([{'signature': self.registration_document['work']}], ['population_dict'], True)[0])
            worker.__logger.debug("Epoch %d. Population merged with other workers.", epoch)

            self.__handle_maximum_fitness(population)
            worker.__logger.debug("Epoch %d. Individuals with maximum fitness handled.", epoch)

            self.work['population_dict'] = self.__cull(population)
            worker.__logger.debug("Epoch %d. Culling completed.", epoch)

            worker.__work_registry.store([{'population_dict': self.work['population_dict']}])
            worker.__logger.debug("Epoch %d. Work registry updated.", epoch)

            self.__log_work()
            worker.__logger.debug("Epoch %d. Statistics logged and epoch completed.", epoch)
