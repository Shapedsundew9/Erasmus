"""A population is a collection of individuals for a specific fitness function.

Created Date: Friday, January 17th 2020, 4:38:35 pm
Author: Shaped Sundew
"""


from hashlib import sha256
from logging import getLogger
from numpy import int32, float32, array, amax, amin, mean, median, count_nonzero, isclose, argmax
from numpy import sum as npsum
from numpy.random import choice
from .gene_pool import gene_pool
from ..config import get_config
from ..database_table import database_table



class population():
    """Defines and manages a population.

    Populations consist of genetic code individuals identified by thier signatures.
    A population manages itself but may influence others when gathered in work.
    i.e. each population has its own population limit, cull policy and other evolution
    parameters. The individuals in the population may be used, mated and/or mutated
    by other populations. The offspring of such interactions remain part of the population.
    """

    _logger = getLogger(__name__)

    def __init__(self, p_config):
        """Configure population.

        Args
        ----
        p_config (dict): The definition of the population and its current status.

        p_config has the following keys:
            signature (str): SHA256 of the population definition.
            log_table (str): A DB table used for tracking the generational changes in the population.
        """
        self._table = database_table(population._logger, 'populations')
        self._log_table = database_table(population._logger, p_config.log_table)
        self.definition = self._table.load([{'signature': p_config['signature']}])[0]
        self.individuals = self.definition['population_dict']


    def initialize(self, gene_pool, target_fitness_function=None):
        """Initialize the population.

        Before a population can be used all individuals must be brought into the gene_pool
        and validated. If the individuals of the population are target individuals and
        already have a target_fitness they are scored with the target_fitness_function 
        and compared to the record in the population table. This
        is to verify the target_fitness_function is consistent with the previous work. A WARNING
        is logged if there is a mismatch. If no individuals
        were defined the population initial query is used to define them.

        Args
        ----
        gene_pool (gene_pool): The gene pool from which this population will be drawn.
        target_fitness_function (func): Takes a target individual GC as a single argument
            retuning a fitness value >= 0.0 and <= 1.0.
        """
        if not self.individuals:
            initial_population = gene_pool.gl(self.definition['initial_query'], ['signature'])
            self.individuals = {s['signature']: gene_pool([s['signature']]) for s in initial_population}
            population._logger.debug("Initial population: %s", self.individuals)
        else:
            individuals_updated = {s['signature']: gene_pool([s['signature']]) for s in self.individuals.keys()}
            for s in individuals_updated: individuals_updated[s]['_target_fitness'] = self.individuals[s]
            self.individuals = individuals_updated
            for gc in filter(lambda x: not x['properties']['mutation'], self.individuals.values()):
                target_fitness = target_fitness_function(gc)
                if not isclose(gc['_target_fitness'], target_fitness):
                    population._logger.warning("Fitness score for GC %s cannot be reproduced: Population fitness score %f versus worker fitness %f score",
                        gc['signature'], gc['_target_fitness'], target_fitness)


    def _mmmm(self, key, data):
        """Find the min, max, mean and median of a numerical array data.

        The results are returned as a dictionary with keys of the form
        key + '_' + x where x is 'min', 'max', 'mean', 'median'.

        Args
        ----
        key (str): The base key for each calaculated value.
        data (array): A numerical array.

        Returns
        -------
        (dict): The results dictionary.
        """
        return {
            key + '_min': amin(data),
            key + '_max': amax(data),
            key + '_mean': mean(data),
            key + '_median': median(data)
        }


    def log(self):
        """Log the state of the population."""
        fitness_data = array([v['_target_fitness'] for v in self.individuals.values()], float32)
        code_depth_data = array([k['code_depth'] for k in self.individuals.values()], int32)
        codon_depth_data = array([k['codon_depth'] for k in self.individuals.values()], int32)
        code_count_data = array([k['num_codes'] for k in self.individuals.values()], int32)
        codon_count_data = array([k['raw_num_codes'] for k in self.individuals.values()], int32)
        log_data = self._mmmm('fitness', fitness_data)
        log_data.update(self._mmmm('code_depth', code_depth_data))
        log_data.update(self._mmmm('codon_depth', codon_depth_data))
        log_data.update(self._mmmm('code_count', code_count_data))
        log_data.update(self._mmmm('codon_count', codon_count_data))
        self._log_table.store([log_data])


    def update_fitness(self, target_fitness_function):
        """Update the fitness of each individual in the population.

        Target fitness is calculated using the target_fitness_function for all target population
        individuals and stored in the extended genetic code dictionary.
        If a target individual is fitter than all of its parent(s).
            Its fitness is increased by 1.
            The mutation that created it fitness is increased by 1.
            If a parasitic GC was inserted during mutation its fitness is increased by 1.
        If a mutation individuals fitness increases.
            If a parasitic GC was involved in the mutation operation its fitness is increased by 1.
        There are no explicit penalties for individual offspring that are as or less suitable
        than thier parent(s). The implicit penalty comes through the weighted selection algorithm
        favouring those individuals with higher fitness and evolvability.

        Args
        ----
        target_fitness_function (func): Takes a target individual GC as a single argument
            returning a fitness value >= 0.0 and <= 1.0.
        """
        for i in filter(lambda x: not x['properties']['mutation'], self.individuals.values()):
            i['_previous_fitness'] = i['_fitness']
            i['_fitness'] = target_fitness_function(i)
            if i['_fitness'] > i['_previous_fitness']:
                self._increment_fitness(i)
                self._increment_fitness(i['_mutated_by'])
                for p in i['_parasites']: self._increment_fitness(p)


    def _increment_fitness(self, xGC):
        """Increment the fitness of an individual.

        Increasing the fitness of an individual increases the evolvability
        of its parent(s).

        Args
        ----
        xGC (xGC): The GC of which fitness will be incremented.
        """
        xGC['fitness'] += 1.0
        for p in xGC['meta_data']['parents'][-1]:
            self._increase_evolvability(gene_pool[p], 1.0)


    def _increase_evolvability(self, xGC, increase):
        """Increase the evolvability of xGC by increase.

        If an individuals evolvability increases the individuals parent(s) evolvability increase
        by 50%% of the individuals evolvability increase.

        NOTE: It is possible (likely) for a single ancestor to get multiple evolvability increases
        from a single descendant if the family tree converges in the past.   

        Args
        ----
        xGC: (xGC) The individual of which evolvability will be increased.
        increase: (float) The amount of evolvability by which to increase.
        """
        evo_queue = [(xGC, increase)]
        while evo_queue:
            xGC, increase = evo_queue.pop()
            xGC['evolvability'] += increase
            for p in xGC['meta_data']['parents'][-1]:
                evo_queue.append((gene_pool[p], increase / 2.0))


    def cull(self):
        """Remove individuals from the population until at the population size limit.

        After breeding/mutation the population may be greater than the size limit.
        If it is it is brought back down to the limit through a random weighted targeting
        of individuals to cull based on their fitness and evolvability. The individual
        with the highest fitness is exempt from the cull (or, in the event of a fitness tie,
        the highest evolvability of the fittest, and if it is still a tie then randomly selected
        from that group).

        The weight of individual, i, eligible for culling is:
            weight = 1.0 - (E(i) / E_max * F(i) / F_max)
        where E(i) is the evolvability of i, E_max is the highest evolvability of any individual in
        the eligible population, F(i) is the target fitness of i and F_max is the highest target
        fitness in the eligible population.

        This gives evolvability and target fitness equal weighting in the survival of eligible
        individuals.
        """
        if len(self.individuals) > self.definition['limit']:
            signature, target_fitness, evolvability = [], [], []
            for k, v in self.individuals.items():
                signature.append(k)
                target_fitness.append(v['_fitness'])
                evolvability.append(v['evolvability'])
            target_fitness = array(target_fitness)
            evolvability = array(evolvability)

            # Identify the individual to save in best_idx        
            best_idx = argmax(target_fitness)
            best_fitness_mask = target_fitness == target_fitness[best_idx]
            if count_nonzero(best_fitness_mask) > 1:
                best_evo = evolvability * best_fitness_mask
                best_evo_idx = argmax(best_evo)
                best_evo_mask = best_evo == best_evo[best_evo_idx]
                if count_nonzero(best_evo_mask) > 1:
                    best_idx = choice(len(best_evo), p=best_evo_mask / npsum(best_evo_mask))
                else:
                    best_idx = argmax(best_evo_mask)

            # Calculate the probabilities for the cull
            weights = target_fitness / npsum(target_fitness) * evolvability / npsum(evolvability)
            weights[best_idx] = 1.0
            probabilities = 1.0 - weights / npsum(weights)
            num_victims = len(self.individuals) - self.definition['limit']
            victims = choice(len(probabilities), size=(num_victims), replace=False, p=probabilities)

            # Cull!
            for v in victims: del self.individuals[signature[v]]

















