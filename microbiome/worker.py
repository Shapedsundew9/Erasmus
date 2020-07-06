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
        worker.__work_log_validator = work_log_validator(get_config()['tables']['work_log_template']['schema'])
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
        valid_population, _ = self.__calculate_fitness([self.gene_pool[signature] for signature in population.keys()])
        for signature, fitness in valid_population.items():
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


    # GCs may be generated that are not valid to be put into the genomic library
    # They are identfied and collected seperately from the functioning
    # population.
    def __calculate_fitness(self, gcs):
        f_pop = {}
        nf_pop = []
        valid_gcs = []
        for gc in gcs:
            if self.gene_pool.validate(gc):
                self.gene_pool.normalize(gc)
                valid_gcs.append(gc)
            else:
                nf_pop.append(gc)
                self.__log_data['invalid_gc'] += 1    
   
        self.gene_pool.update(valid_gcs)

        # TODO: Use __individual_fitness()
        for gc in valid_gcs:
                try:
                    fitness = self.__fitness_function(self.gene_pool.callable(gc['signature']), gc=gc)
                except Exception as ex:
                    worker.__logger.info("Individual failed the fitness test: {}, {}".format(type(ex).__name__, ex.args))
                    f_pop[gc['signature']] = 0.0
                    self.__log_data['failed_fitness'] += 1       
                else:
                    f_pop[gc['signature']] = fitness

        return f_pop, nf_pop


    def __individual_fitness(self, gc):
        try:
            fitness = self.__fitness_function(self.gene_pool.callable(gc['signature']), gc=gc)
        except Exception as ex:
            worker.__logger.info("Individual failed the fitness test: {}, {}".format(type(ex).__name__, ex.args))
            fitness = 0.0
        return fitness


    # TODO: Currently hard coded
    def __stop_criteria_met(self, population):
        if len(population) != self.work['population_limit']: return False
        for fitness in population.values():
            if fitness == 1.0: return True 
        return False


    # Return a copy of the GC without any unique fields
    def __clone(self, gc):
        return {
            'graph': deepcopy(gc['graph']),

            # If this is generation 0 then generation 1 cannot have GCA == NULL_GC
            'gca': gc['gca'] if gc['gca'] != NULL_GC else gc['signature'],
            'gcb': gc['gcb'],
            'properties': deepcopy(gc['properties']),
        }


    def __mutate(self, signature, population, meta_data, invalid=None):
        # FIXME: The selection of mutation candidates needs to be evolved
        mutation = choice(self.__mutation_keys)
        worker.__logger.debug("Chosen mutation %s", mutation)

        # Mutations modify the GC passed to them so it is necessary to
        # clone the relevant fields into a new object
        gc = invalid if not invalid is None else self.__clone(self.gene_pool[signature])

        # Unary or binary copulation
        if meta_data[mutation]['properties']['unary_mutation']:
            func = lambda: meta_data[mutation]['callable']((gc,)) 
        else:
            # FIXME: The selection of a breeding partner needs to be evolved
            partner = choice(population)
            func = lambda: meta_data[mutation]['callable']((gc, self.__clone(self.gene_pool[partner])))

        # Handle & log failed conception i.e. runtime exceptions in mutation
        try:
                ngc = func()[0]
        except Exception as ex:
            worker.__logger.warning("Conception failed with {}, {}".format(type(ex).__name__, ex.args))
            self.__log_data['failed_conception'] += 1
            ngc = None

        # Update parentage & class data
        if not ngc is None:
            if not 'meta_data' in ngc: ngc['meta_data'] = {}
            ngc['meta_data']['parents'] = [[signature]] if invalid is None else invalid['meta_data']['parents']
            if meta_data[mutation]['properties']['binary_mutation']: ngc['meta_data']['parents'][-1].append(partner)
            ngc['alpha_class'] = 1

        return ngc


    def __evolve(self, population, invalid_population):
        if getmtime(gm.__file__) > self.__mutation_file_mtime:
            reload(sys.modules['microbiome.genetics.mutations'])
            from .genetics.mutations import meta_data
            self.__mutation_file_mtime = getmtime(gm.__file__)
            self.__mutation_keys = list(meta_data.keys())

        population_list = list(population.keys())
        new_gcs = []
        for signature in population.keys():
            gc = self.__mutate(signature, population_list, meta_data)
            if not gc is None: new_gcs.append(gc)
        for invalid in invalid_population:
            gc = self.__mutate(NULL_GC, population_list, meta_data, invalid)
            if not gc is None: new_gcs.append(gc)
        worker.__logger.debug("%s", new_gcs)
        self.__log_data['born'] = len(new_gcs)
        return new_gcs


    # TODO: This is currently hard coded.
    def __cull(self, population, invalid_population, minimum_viable_fraction=0.0):
        max_fitness = 1.0 if not len(population) else max((max(population.values()), 1.0))
        cull_list = [(k, max_fitness - v + 1.0) for k, v in population.items()]
        cull_list.extend([(i, max_fitness) for i in range(len(invalid_population))])
        cull_list.sort(key=lambda x:x[1])
        worker.__logger.debug("Cull list: %s", cull_list)
        # Determine how many were still born
        self.__log_data['culled'] = 0
        if len(cull_list) > self.work['population_limit']:
            self.__log_data['culled'] = len(cull_list) - self.work['population_limit']
            saved = int(minimum_viable_fraction * (self.work['population_limit'] - 2)) + 1
            cull_list = cull_list[saved:]
            worker.__logger.debug("Reduced cull list: %s", cull_list)
            weights = [t[1] for t in cull_list]
            indices = list(range(len(cull_list)))
            ip_victims = []
            for _ in range(self.__log_data['culled']):
                victim_idx = choices(indices, weights)[0]
                victim = cull_list[victim_idx][0]
                worker.__logger.debug("Cull victim: %s", victim)
                if victim in population:
                    del population[victim]
                else:
                    ip_victims.append(victim)
                weights[victim_idx] = 0.0
            invalid_population = [p for i, p in enumerate(invalid_population) if i not in ip_victims]
        self.__log_data['population'] = len(population) + len(invalid_population)
        return population, invalid_population


    def __log_work(self):
        self.__log_data['wall_clock_runtime'] = perf_counter() - self.__log_data['wall_clock_runtime']
        self.__log_data['cpu_runtime'] = process_time() - self.__log_data['cpu_runtime']
        self.__log_data['EGPOPs'] = self.__log_data['cpu_runtime']
        self.__log_data['RSS'] = Process().memory_info().rss / (1024 * 1024 * 1024.0)
        self.__log_data['worker'] = self.registration_document['signature']

        fitness_data = array([v for v in self.work['population_dict'].values()])
        self.__log_data['fitness_min'] = float(amin(fitness_data)) if fitness_data.size > 0 else None
        self.__log_data['fitness_max'] = float(amax(fitness_data)) if fitness_data.size > 0 else None
        self.__log_data['fitness_mean'] = float(mean(fitness_data)) if fitness_data.size > 0 else None
        self.__log_data['fitness_median'] = float(median(fitness_data)) if fitness_data.size > 0 else None

        code_depth_data = array([self.gene_pool[k]['code_depth'] for k in self.work['population_dict'].keys()])
        self.__log_data['code_depth_min'] = int(amin(code_depth_data)) if code_depth_data.size > 0 else None
        self.__log_data['code_depth_max'] = int(amax(code_depth_data)) if code_depth_data.size > 0 else None
        self.__log_data['code_depth_mean'] = float(mean(code_depth_data)) if code_depth_data.size > 0 else None
        self.__log_data['code_depth_median'] = int(median(code_depth_data)) if code_depth_data.size > 0 else None

        codon_depth_data = array([self.gene_pool[k]['codon_depth'] for k in self.work['population_dict'].keys()])
        self.__log_data['codon_depth_min'] = int(amin(codon_depth_data)) if codon_depth_data.size > 0 else None
        self.__log_data['codon_depth_max'] = int(amax(codon_depth_data)) if codon_depth_data.size > 0 else None
        self.__log_data['codon_depth_mean'] = float(mean(codon_depth_data)) if codon_depth_data.size > 0 else None
        self.__log_data['codon_depth_median'] = int(median(codon_depth_data)) if codon_depth_data.size > 0 else None

        code_count_data = array([self.gene_pool[k]['num_codes'] for k in self.work['population_dict'].keys()])
        self.__log_data['code_count_min'] = int(amin(code_count_data)) if code_count_data.size > 0 else None
        self.__log_data['code_count_max'] = int(amax(code_count_data)) if code_count_data.size > 0 else None
        self.__log_data['code_count_mean'] = float(mean(code_count_data)) if code_count_data.size > 0 else None
        self.__log_data['code_count_median'] = int(median(code_count_data)) if code_count_data.size > 0 else None

        codon_count_data = array([self.gene_pool[k]['raw_num_codons'] for k in self.work['population_dict'].keys()])
        self.__log_data['codon_count_min'] = int(amin(codon_count_data)) if codon_count_data.size > 0 else None
        self.__log_data['codon_count_max'] = int(amax(codon_count_data)) if codon_count_data.size > 0 else None
        self.__log_data['codon_count_mean'] = float(mean(codon_count_data)) if codon_count_data.size > 0 else None
        self.__log_data['codon_count_median'] = int(median(codon_count_data)) if codon_count_data.size > 0 else None

        self.__log_data = worker.__work_log_validator.normalized(self.__log_data)
        self.__work_log.store([self.__log_data])


    def __starting_log_data(self):
        self.__log_data = {
            'wall_clock_runtime': perf_counter(),
            'cpu_runtime': process_time(),
            'failed_conception': 0,
            'failed_fitness': 0,
            'invalid_gc': 0 
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
        worker.__logger.info("Starting population of %d individuals loaded into gene pool.", len(self.work['population_dict']))

        if existing_population and not self.__valid_work(self.work['population_dict']):
            worker.__logger.error("Work definition is not consistent with existing work registration details. Worker config: %s", str(self.config))
            worker.__logger.error("Has the fitness function been modified?")
            exit(1)
        if not existing_population:
            initial_population = self.gene_pool.gl(self.work['initial_query'], ['signature'])
            self.work['population_dict'] = { s['signature']: self.__individual_fitness(self.gene_pool[s['signature']]) for s in initial_population }   
            worker.__logger.debug("Initial population: %s", self.work['population_dict'])


        # Loop
        epoch = 0
        invalid_population = []
        while not self.__stop_criteria_met(self.work['population_dict']):
            epoch += 1
            worker.__logger.info("Starting epoch %d.", epoch)
            self.__starting_log_data()
            worker.__logger.debug("Epoch %d. Initialised logging data.", epoch)

            new_gcs = self.__evolve(self.work['population_dict'], invalid_population)
            worker.__logger.debug("Epoch %d. Breeding completed.", epoch)

            population, invalid_population_tmp = self.__calculate_fitness(new_gcs)
            invalid_population.extend(invalid_population_tmp)
            population.update(self.work['population_dict'])
            worker.__logger.debug("Epoch %d. Fitness calculated", epoch)
            worker.__logger.debug("Epoch %d. Population: %s", epoch, population)
            worker.__logger.debug("Epoch %d. Invalid population: %s", epoch, invalid_population)

            population.update(worker.__work_registry.load([{'signature': self.registration_document['work']}], ['population_dict'], True)[0]['population_dict'])
            worker.__logger.debug("Epoch %d. Population merged with other workers.", epoch)
            worker.__logger.debug("Epoch %d. Population: %s", epoch, population)
            worker.__logger.debug("Epoch %d. Invalid population: %s", epoch, invalid_population)

            self.__handle_maximum_fitness(population)
            worker.__logger.debug("Epoch %d. Individuals with maximum fitness handled.", epoch)

            self.work['population_dict'], invalid_population = self.__cull(population, invalid_population)
            worker.__logger.debug("Epoch %d. Culling completed.", epoch)
            worker.__logger.debug("Epoch %d. Population: %s", epoch, population)
            worker.__logger.debug("Epoch %d. Invalid population: %s", epoch, invalid_population)

            worker.__work_registry.update([{'population_dict': self.work['population_dict']}], [{'signature': self.registration_document['work']}])
            worker.__logger.debug("Epoch %d. Work registry updated.", epoch)

            self.__log_work()
            worker.__logger.debug("Epoch %d. Statistics logged and epoch completed.", epoch)
            #if epoch == 2: barf()
