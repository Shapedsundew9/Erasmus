'''
Filename: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics/worker.py
Path: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics
Created Date: Tuesday, May 5th 2020, 6:00:39 pm
Author: Shapedsundew9

Copyright (c) 2020 Your Company
'''

from .platform_info import get_platform_info
from .config import get_config
from .database_table import database_table
from .genetics.gene_pool import gene_pool
from .worker_registry_validator import worker_registry_validator
from copy import deepcopy
from logging import getLogger
from math import isclose
from random import choices, setstate
from numpy import float32, array, amax, amin


class worker():


    __logger = getLogger(__name__)
    __worker_registry = None
    __work_registry = None


    # Work is the signature of the registered work.
    def __init__(self, config):
        self.config = config
        self.registration_document = { "platform": get_platform_info(), "work": config['work'] }
        validator = worker_registry_validator()
        if not validator.validate(self.registration_document):
            worker.__logger.error("Invalid worker registration document: %s", validator.errors)
            exit(1)
        self.registration_document = validator.normalized(self.registration_document)
        if worker.__worker_registry is None: worker.__worker_registry = database_table(worker.__logger, get_config()['worker_registry'])
        worker.__worker_registry.store([self.registration_document])
        if worker.__work_registry is None:  worker.__work_registry = database_table(worker.__logger, get_config()['work_registry'])
        self.work = None
        self.gene_pool = None


    def __function_not_found(self, name):
        worker.__logger.error("The dynamically determined function %s cannot be found.", name)


    def __valid_work(self):
        count = 0
        for signature, fitness in self.__calculate_fitness().items():
            if not isclose(self.work['population_dict'][signature], fitness):
                worker.__logger.warning("Fitness score for GC %s cannot be reproduced: Work registry fitness score %f versus worker fitness %f score",
                    signature, self.work['population_dict'][signature], fitness)
                count += 1
        if count:
            worker.__logger.warning("%d of %d (%0.2f%%) worker registry recorded fitness scores could not be reproduced by the worker.",
                count, len(self.work['population_dict']), 100.0 * count / len(self.work['population_dict']))
            return False
        worker.__logger.info("Worker was able to reproduce all of the registered work fitness scores.")
        return True


    def __calculate_fitness(self):
        # TODO: Implement
        return {}


    def __stop_criteria_met(self):
        # TODO: Implement
        return True


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


    def __gc_addition(self, signature):
        cf = self.work['evolution_parameters']['asexual']['config']['addition']
        return {}


    def __gc_subtraction(self, signature):
        cf = self.work['evolution_parameters']['asexual']['config']['subtraction']
        return {}


    def __gc_exchange(self, signature):
        cf = self.work['evolution_parameters']['asexual']['config']['exchange']
        return {}


    def __gc_rewire(self, signature):
        cf = self.work['evolution_parameters']['asexual']['config']['rewire']
        return {}


    def __gc_adjust_constant(self, signature):
        cf = self.work['evolution_parameters']['asexual']['config']['adjust_constant']
        return {}


    def __asexual_reproduction(self, signature):
        worker.__logger.debug("Asexual reproduction for individual %s", signature)
        cf = self.work['evolution_parameters']['asexual']['config']
        method = '__gc_' + choices(list(cf.keys()), [v['weight'] for v in cf.values()])
        return getattr(self, method, lambda: self.__function_not_found(method))(signature)


    def __sexual_reproduction(self, signature):
        worker.__logger.debug("Sexual reproduction for individual %s", signature)
        # TODO: Implement
        return {}


    def __evolve(self):
        cf = self.work['evolution_parameters']
        new_population = {}
        new_gc_list = []
        for signature in self.work['population_dict'].keys():
            funct = self.__asexual_reproduction if choices([True, False], [cf['asexual']['weight'], cf['sexual']['weight']]) else self.__sexual_reproduction
            new_gc_list.extend(funct(self.gene_pool[signature]))
            new_population[new_gc_list[-1]] = 0.0
        self.gene_pool.update(new_gc_list)
        return new_population


    def __cull(self):
        # TODO: Implement
        return {}


    def __log_work(self):
        # TODO: Implement
        pass


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
        setstate(self.work['evolution_parameters'])
        existing_population = len(self.work['population_dict'])
        if existing_population: self.work['initial_query'] = [{'signature': list(self.work['population_dict'].keys())}]
        self.gene_pool = gene_pool(self.work['initial_query'], self.config['delete_gene_pool'], self.config['gene_pool_prefix'])
        if existing_population and not self.__valid_work():
            gene_pool.__logger.error("Work definition is not consistent with existing work registration details. Worker config: %s", str(self.config))
            exit(1)
        
        # Loop
        while not self.__stop_criteria_met():
            self.work['population_dict'] = self.__evolve()
            self.work['population_dict'] = self.__calculate_fitness()
            self.work['population_dict'].update(worker.__work_registry.lock_and_load([{'signature': self.registration_document['work']}], ['population_dict'])[0])
            self.work['population_dict'] = self.__cull()
            worker.__work_registry.store_and_release([{'population_dict': self.work['population_dict']}])
            self.__log_work()
