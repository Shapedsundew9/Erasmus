'''
Filename: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics/worker.py
Path: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics
Created Date: Tuesday, May 5th 2020, 6:00:39 pm
Author: Shapedsundew9

Copyright (c) 2020 Your Company
'''

import sys
import tracemalloc
from traceback import format_exc
from .genetics import mutations as gm
from .genetics.mutations import meta_data
from .platform_info import get_platform_info
from .config import get_config, update_config
from .database_table import database_table
from .genetics.gene_pool import gene_pool
from .worker_registry_validator import worker_registry_validator
from .work_log_validator import work_log_validator
from .genetics.genomic_library_entry_validator import NULL_GC, DEAD_GC_PREFIX
from copy import deepcopy
from logging import getLogger
from math import isclose
from random import choice, choices, setstate, getrandbits, randrange
from numpy import float32, array, amax, amin, mean, median
from time import perf_counter, process_time
from psutil import Process
from importlib import reload
from os.path import getmtime, dirname, join
from pprint import pformat


_DEFAULT_INITIAL_QUERY = [{'gca': NULL_GC, 'gcb': NULL_GC}]


class worker():


    _logger = getLogger(__name__)
    _worker_registry = None
    _work_registry = None
    _work_log_validator = work_log_validator()


    # fitness_function must be a callable that takes a callable func() and returns a single > 0.0 floating point fitness value. The bigger the better.
    # func() takes a numpy.array(dtype=numpy.float32) and returns a numpy.array(dtype=numpy.float32)
    # TODO: Decide what to do with fitness_function
    def __init__(self, worker_config, fitness_function):
        #tracemalloc.start()
        self.config = worker_config
        worker._work_log_validator = work_log_validator(get_config()['tables']['work_log_template']['schema'])
        self.registration_document = { "platform": get_platform_info()['signature'], "work": worker_config['work'], "creator": worker_config['creator'] }
        self._egpopss = get_platform_info()['EGPOps/s']
        validator = worker_registry_validator(get_config()['tables']['worker_registry']['schema'])
        if not validator.validate(self.registration_document):
            worker._logger.error("Invalid worker registration document: %s", validator.errors)
            exit(1)
        self.registration_document = validator.normalized(self.registration_document)
        if worker._worker_registry is None: worker._worker_registry = database_table(worker._logger, 'worker_registry')
        worker._worker_registry.store([self.registration_document])
        if worker._work_registry is None:  worker._work_registry = database_table(worker._logger, 'work_registry', True)
        self.gene_pool = None


    def _function_not_found(self, name):
        worker._logger.error("The dynamically determined function %s cannot be found.", name)




    # GCs may be generated that are not valid to be put into the genomic library
    # They are identfied and collected seperately from the functioning
    # population.
    def _calculate_fitness(self, gcs):
        f_pop = {}

        for gc in gcs:
            fitness = 0.0 if '_fitness_sum' not in gc else gc['_fitness_sum'] / gc['_fitness_count']
            gc['_valid'], err = self.gene_pool.validate(gc)
            if gc['_valid']:
                self.gene_pool.normalize(gc)
                fitness += self._individual_fitness(gc)
                f_pop[gc['signature']] = fitness
            else:
                # Set fitness to < 1.0
                # Fitness > 0.0 and < 1.0 are invalid GC's
                # The more errors in the GC validation the lower the fitness. 
                gc['signature'] = DEAD_GC_PREFIX + "{:032x}".format(randrange(16**32))
                num_errs = sum([len(e) for e in err.values()])
                f_pop[gc['signature']] = 0.5 / num_errs
                self._log_data['invalid_gc'] += 1    

            # Propagate backwards mutation efficacy
            mutation_queue = []
            if 'mutations' in gc['meta_data']: mutation_queue .append((gc['meta_data']['mutations'], fitness))
            while mutation_queue:
                mutation_list, fitness = mutation_queue.pop()
                shared_fitness = fitness / float(len(mutation_list))
                for mutation in mutation_list:
                    self._update_mutation_fitness(mutation, shared_fitness)
                    if 'mutations' in self.gene_pool[mutation]['meta_data']:
                        mutation_queue.append((self.gene_pool[mutation]['meta_data']['mutations'], shared_fitness))

        self.gene_pool.add(gcs)
        return f_pop


    # Returns a value >= 1.0
    # 1.0 is the minimum fitness for a valid GC
    def _individual_fitness(self, gc):
        try:
            fitness = 1.0 + self._fitness_function(self.gene_pool.callable(gc['signature']), gc=gc)
        except Exception as ex:
            worker._logger.info("Individual failed the fitness test: {}, {}".format(type(ex).__name__, ex.args))
            fitness = 1.0
        return fitness


    # TODO: Currently hard coded
    def _stop_criteria_met(self, population):
        if len(population) != self.work['population_limit']: return False
        for fitness in population.values():
            if fitness == 1.0: return True 
        return False


    # Return a copy of the GC without any unique fields
    def _clone(self, gc):
        return {
            '_valid': gc['_valid'],
            'graph': deepcopy(gc['graph']),
    
            # If this is generation 0 then generation 1 cannot have GCA == NULL_GC
            '_gca': gc['_gca'] if not gc['_gca'] is None else gc,
            '_gcb': gc['_gcb'],
            'gca': gc['gca'] if not gc['_gca'] is None else gc['signature'],
            'gcb': gc['gcb'],
            'properties': deepcopy(gc['properties']),
        }


    def _update_mutation_fitness(self, mutation, fitness):
        gc = self.gene_pool[mutation]
        if not '_fitness_sum' in gc:
            gc['_fitness_sum'] = 0.0
            gc['_fitness_count'] = 0
        self.gene_pool[mutation]['_fitness_sum'] += fitness
        self.gene_pool[mutation]['_fitness_count'] += 1


    def _mutate(self, signature, population, meta_data):
        # FIXME: The selection of mutation candidates needs to be evolved
        mutation = choice(self._mutation_keys)
        worker._logger.debug("Chosen mutation %s", mutation)

        # Mutations modify the GC passed to them so it is necessary to
        # clone the relevant fields into a new object
        parent = self.gene_pool[signature]
        gc = self._clone(parent)

        # Unary or binary copulation
        if meta_data[mutation]['properties']['unary_mutation']:
            func = lambda: meta_data[mutation]['callable']((gc,)) 
        else:
            # FIXME: The selection of a breeding partner needs to be evolved
            partner = choice(population)
            func = lambda: meta_data[mutation]['callable']((gc, self._clone(self.gene_pool[partner])))

        # Handle & log failed conception i.e. runtime exceptions in mutation
        try:
            ngc = func()[0]
        except Exception as ex:
            worker._logger.warning("Conception failed with {}, {}, {}".format(type(ex).__name__, ex.args, format_exc()))
            self._log_data['failed_conception'] += 1
            ngc = None
            self._update_mutation_fitness(mutation, 0.0)

        # It is possible that a mutation could turn a gc into another type
        if not isinstance(ngc, dict): ngc = None

        # Update parentage & class data
        if not ngc is None:
            if not 'meta_data' in ngc: ngc['meta_data'] = {}
            ngc['meta_data']['parents'] = [[signature]] if parent['_valid'] else deepcopy(parent['meta_data']['parents']) 
            if meta_data[mutation]['properties']['binary_mutation']: ngc['meta_data']['parents'][-1].append(partner)
            if 'mutations' not in ngc['meta_data']:
                ngc['meta_data']['mutations'] = [mutation]
            else:
                ngc['meta_data']['mutations'].append(mutation)
            ngc['alpha_class'] = 1

        #if 'name' in self.gene_pool[mutation]['meta_data'] and self.gene_pool[mutation]['meta_data']['name'] == "Stack": worker._logger.debug("barf")
        return ngc


    def _evolve(self, population):
        if getmtime(gm._file_) > self._mutation_file_mtime:
            reload(sys.modules['microbiome.genetics.mutations'])
            from .genetics.mutations import meta_data
            self._mutation_file_mtime = getmtime(gm._file_)
            self._mutation_keys = list(meta_data.keys())

        population_list = list(population.keys())
        new_gcs = []
        for signature in population.keys():
            gc = self._mutate(signature, population_list, meta_data)
            if not gc is None: new_gcs.append(gc)
        worker._logger.debug("%s", pformat(new_gcs, width=180))
        self._log_data['born'] = len(new_gcs)
        return new_gcs





    def _log_work(self):
        self._log_data['wall_clock_runtime'] = perf_counter() - self._log_data['wall_clock_runtime']
        self._log_data['cpu_runtime'] = process_time() - self._log_data['cpu_runtime']
        self._log_data['EGPOps'] = self._egpopss * self._log_data['cpu_runtime']
        self._log_data['RSS'] = Process().memory_info().rss / (1024 * 1024 * 1024.0)
        self._log_data['worker'] = self.registration_document['signature']


    def _starting_log_data(self):
        self._log_data = {
            'wall_clock_runtime': perf_counter(),
            'cpu_runtime': process_time(),
            'failed_conception': 0,
            'failed_fitness': 0,
            'invalid_gc': 0 
        }


    def _handle_maximum_fitness(self, population):
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
        self.work = worker._work_registry.load([{'signature': self.registration_document['work']}])[0]
        work_log_table = 'work_' + self.work['signature'][:16] + '_log'
        update_config({'tables': {work_log_table: deepcopy(get_config()['tables']['work_log_template'])}})
        self._work_log = database_table(worker._logger, work_log_table)

        # TODO: Random state management
        # setstate(self.work['evolution_parameters']['random_state'])

        existing_population = len(self.work['population_dict'])
        if existing_population:
            worker._logger.info("Exisiting population of %d individuals found in work registry.", existing_population)
            self.work['initial_query'] = [{'signature': list(self.work['population_dict'].keys())}]
        elif self.work['initial_query'] is None:
            worker._logger.info("No exisiting population found in work registry and initial_query == None. Generating population from default query: %s.",
                _DEFAULT_INITIAL_QUERY)
            self.work['initial_query'] = _DEFAULT_INITIAL_QUERY
        else:
            worker._logger.info("No exisiting population found in work registry. Generating from initial query: %s.", self.work['initial_query'])
        self.gene_pool = gene_pool(self.work['initial_query'], file_ptr=self.work['gene_pool'])
        worker._logger.info("Starting population of %d individuals loaded into gene pool.", len(self.work['population_dict']))

        if existing_population and not self._valid_work(self.work['population_dict']):
            worker._logger.error("Work definition is not consistent with existing work registration details. Worker config: %s", str(self.config))
            worker._logger.error("Has the fitness function been modified?")
            exit(1)
        if not existing_population:
            initial_population = self.gene_pool.gl(self.work['initial_query'], ['signature'])
            self.work['population_dict'] = { s['signature']: self._individual_fitness(self.gene_pool[s['signature']]) for s in initial_population }   
            worker._logger.debug("Initial population: %s", self.work['population_dict'])


        # Loop
        epoch = 0
        while not self._stop_criteria_met(self.work['population_dict']):
            epoch += 1
            worker._logger.info("Starting epoch %d.", epoch)
            self._starting_log_data()
            worker._logger.debug("Epoch %d. Initialised logging data.", epoch)

            new_gcs = self._evolve(self.work['population_dict'])
            worker._logger.debug("Epoch %d. Breeding completed.", epoch)

            population = self._calculate_fitness(new_gcs)
            population.update(self.work['population_dict'])
            worker._logger.debug("Epoch %d. Fitness calculated", epoch)
            worker._logger.debug("Epoch %d. Population: %s", epoch, pformat(population))

            population.update(worker._work_registry.load([{'signature': self.registration_document['work']}], ['population_dict'], True)[0]['population_dict'])
            worker._logger.debug("Epoch %d. Population merged with other workers.", epoch)
            worker._logger.debug("Epoch %d. Population: %s", epoch, pformat(population))

            self._handle_maximum_fitness(population)
            worker._logger.debug("Epoch %d. Individuals with maximum fitness handled.", epoch)

            self.work['population_dict'] = self._cull(population)
            worker._logger.debug("Epoch %d. Culling completed.", epoch)
            worker._logger.debug("Epoch %d. Population: %s", epoch, pformat(population))

            worker._work_registry.update([{'population_dict': self.work['population_dict']}], [{'signature': self.registration_document['work']}])
            worker._logger.debug("Epoch %d. Work registry updated.", epoch)

            self._log_work()
            worker._logger.debug("Epoch %d. Statistics logged and epoch completed.", epoch)


            """
            snapshot = tracemalloc.take_snapshot()
            top_stats = snapshot.statistics('lineno')

            print("\n[ Top 10 ]")
            for stat in top_stats[:10]:
                print(stat)

            if epoch == 20: import pdb; pdb.set_trace()
            """