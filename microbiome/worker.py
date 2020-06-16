'''
Filename: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics/worker.py
Path: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics
Created Date: Tuesday, May 5th 2020, 6:00:39 pm
Author: Shapedsundew9

Copyright (c) 2020 Your Company
'''

from .platform_info import get_platform_info
from .config import get_config, update_config
from .database_table import database_table
from .genetics.gene_pool import gene_pool
from .worker_registry_validator import worker_registry_validator
from .work_log_validator import work_log_validator
from copy import deepcopy
from logging import getLogger
from math import isclose
from random import choices, setstate, getrandbits
from numpy import float32, array, amax, amin, mean, median
from time import perf_counter, process_time
from psutil import Process


class worker():


    __logger = getLogger(__name__)
    __worker_registry = None
    __work_registry = None
    __work_log_validator = work_log_validator()


    # fitness_function must be a callable that takes a callable func() and returns a single > 0.0 floating point fitness value. The bigger the better.
    # func() takes a numpy.array(dtype=numpy.float32) and returns a numpy.array(dtype=numpy.float32)
    def __init__(self, worker_config, fitness_function):
        self.config = worker_config
        self.registration_document = { "platform": get_platform_info(), "work": worker_config['work'] }
        validator = worker_registry_validator()
        if not validator.validate(self.registration_document):
            worker.__logger.error("Invalid worker registration document: %s", validator.errors)
            exit(1)
        self.registration_document = validator.normalized(self.registration_document)
        if worker.__worker_registry is None: worker.__worker_registry = database_table(worker.__logger, 'worker_registry')
        worker.__worker_registry.store([self.registration_document])
        if worker.__work_registry is None:  worker.__work_registry = database_table(worker.__logger, 'work_registry')
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


    # Creation of a new GC as a mutation of an existing GC requires
    # specific fields to be updated related to lineage 
    def __create_predecesors(self, new_gc, predecesor_list):
        new_gc_list = [new_gc]
        signature = predecesor_list[0]['gc']['signature']
        if len(predecesor_list) > 1:
            for predecesor in predecesor_list[1:]:
                ngcab, gcab = ('gcb', 'gca') if signature == predecesor['gca']['signature'] else ('gca', 'gcb')
                gc = predecesor['gc']
                new_gc = {'graph': deepcopy(gc['graph'])}
                new_gc[gcab] = new_gc_list[-1]['signature']
                new_gc[ngcab] = predecesor[ngcab]['signature']
                new_gc['creator'] = self.config['creator']
                new_gc['meta_data'] = {'parents': [gc['signature']]}        
                self.gene_pool.normalize(new_gc)
                new_gc_list.append(new_gc)
        return new_gc_list


    # To duplicate a GC a new GC is added that takes the same inputs as the
    # original GC and connects them to two copies in GCA & GCB
    def __gc_duplication(self, agc):
        cf = self.work['evolution_parameters']['asexual']['config']['duplication']
        predecesor_list = agc['genetic_code'].select(cf['dpm'], cf['gpm'])
        if predecesor_list:
            gc = predecesor_list[0]['gc']

            # Define the new GC
            new_inputs = [['I', i] for i in range(gc['num_inputs'])]
            new_gc = {'graph': {
                'A': new_inputs,
                'B': new_inputs,
                'O': [[gcab, i] for gcab in ['A', 'B'] for i in range(gc['num_outputs'])]
            }}
            new_gc['gca'] = gc['signature']
            new_gc['gcb'] = gc['signature']
            new_gc['creator'] = self.config['creator']
            new_gc['meta_data'] = {'parents': [gc['signature']]}
            self.gene_pool.normalize(new_gc)
            return self.__create_predecesors(new_gc, predecesor_list)
        return [agc['genetic_code']['gc']]


    def __gc_addition(self, agc):
        cf = self.work['evolution_parameters']['asexual']['config']['addition']
        predecesor_list = agc['genetic_code'].select(cf['dpm'], cf['gpm'])
        if predecesor_list and False:
            return self.__create_predecesors({}, predecesor_list)
        return [agc['genetic_code']['gc']]


    # To subtract a GC find set GCA or GCB to None from a random selection.
    # Route any inputs & constants to outputs.
    # This will likely change the number of outputs.
    def __gc_subtraction(self, agc):
        cf = self.work['evolution_parameters']['asexual']['config']['subtraction']
        predecesor_list = agc['genetic_code'].select(cf['dpm'], cf['gpm'])
        if not agc['gca'] is None and not agc['gcb'] is None:
            new_gc = {'graph': deepcopy(agc['graph'])}
            new_gc['gca'] = agc['gca']
            new_gc['gcb'] = agc['gcb']
            if bool(getrandbits(1)):
                new_gc['graph']['O'].extend(new_gc['graph']['A'])
                new_gc['graph']['A'] = []
                new_gc['gca'] = None
            else:
                new_gc['graph']['O'].extend(new_gc['graph']['B'])
                new_gc['graph']['B'] = []
                new_gc['gcb'] = None
            new_gc['creator'] = self.config['creator']
            new_gc['meta_data'] = {'parents': [agc['signature']]}
            self.gene_pool.normalize(new_gc)
            return self.__create_predecesors(new_gc, predecesor_list)
        return [agc['genetic_code']['gc']]


    def __gc_exchange(self, agc):
        cf = self.work['evolution_parameters']['asexual']['config']['exchange']
        predecesor_list = agc['genetic_code'].select(cf['dpm'], cf['gpm'])
        if predecesor_list and False:
            return self.__create_predecesors({}, predecesor_list)
        return [agc['genetic_code']['gc']]


    def __gc_rewire(self, agc):
        cf = self.work['evolution_parameters']['asexual']['config']['rewire']
        predecesor_list = agc['genetic_code'].select(cf['dpm'], cf['gpm'])
        if predecesor_list and False:
            return self.__create_predecesors({}, predecesor_list)
        return [agc['genetic_code']['gc']]


    def __gc_adjust_constant(self, agc):
        cf = self.work['evolution_parameters']['asexual']['config']['adjust_constant']
        predecesor_list = agc['genetic_code'].select(cf['dpm'], cf['gpm'])
        if predecesor_list and False:
            return self.__create_predecesors({}, predecesor_list)
        return [agc['genetic_code']['gc']]


    # Returns a list of GC's to add to the gene pool.The last is added to the next generation population.
    def __asexual_reproduction(self, agc):
        worker.__logger.debug("Asexual reproduction for individual %s", agc['signature'])
        cf = self.work['evolution_parameters']['asexual']['config']
        method = '__gc_' + choices(list(cf.keys()), [v['weight'] for v in cf.values()])
        return getattr(self, method, lambda: self.__function_not_found(method))(agc)


    # Returns a list of GC's to add to the gene pool.The last is added to the next generation population. 
    def __sexual_reproduction(self, signature):
        worker.__logger.debug("Sexual reproduction for individual %s", signature)
        # TODO: Implement
        return {}


    def __evolve(self, population):
        cf = self.work['evolution_parameters']
        new_population = {}
        new_gc_list = []
        for signature in population.keys():
            funct = self.__asexual_reproduction if choices([True, False], [cf['asexual']['weight'], cf['sexual']['weight']]) else self.__sexual_reproduction
            new_gc_list.extend(funct(self.gene_pool[signature]))
            new_population[new_gc_list[-1]] = 0.0
        self.gene_pool.update(new_gc_list)
        return new_population


    # TODO: This is currently hard coded.
    def __cull(self, population):
        self.__log_data['born'] = len(population) - self.work['population_limit']
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
    # 5. Merge generations
    # 6. Cull
    # 7. Update work definition and unlock
    # 8. Log work results & stats
    # 9. Update gene pool
    # 10. Assess stopping criteria (and stop if met)
    # 11. Go to #3.
    def evolve(self):

        # Initialise
        self.work = worker.__work_registry.load([{'signature': self.registration_document['work']}])[0]
        work_log_table = 'work_' + self.work['signature'] + '_log'
        update_config({'table': {work_log_table: deepcopy(get_config()['table']['work_log_template'])}})
        self.__work_log = database_table(worker.__logger, work_log_table)
        setstate(self.work['evolution_parameters']['random_state'])
        existing_population = len(self.work['population_dict'])
        if existing_population: self.work['initial_query'] = [{'signature': list(self.work['population_dict'].keys())}]
        self.gene_pool = gene_pool(self.work['initial_query'], self.config['gene_pool_prefix'])
        if existing_population and not self.__valid_work(self.work['population_dict']):
            gene_pool.__logger.error("Work definition is not consistent with existing work registration details. Worker config: %s", str(self.config))
            exit(1)
        
        # Loop
        while not self.__stop_criteria_met(self.work['population_dict']):
            self.__starting_log_data()
            population = self.__evolve(self.work['population_dict'])
            population = self.__calculate_fitness(population)
            population.update(worker.__work_registry.load([{'signature': self.registration_document['work']}], ['population_dict'], True)[0])
            self.work['population_dict'] = self.__cull(population)
            worker.__work_registry.store([{'population_dict': self.work['population_dict']}])
            self.__log_work()
