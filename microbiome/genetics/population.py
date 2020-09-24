"""A population is a collection of individuals for a specific fitness function.

Created Date: Friday, January 17th 2020, 4:38:35 pm
Author: Shaped Sundew
"""


from hashlib import sha256
from logging import getLogger
from numpy import float32, array, amax, amin, mean, median
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

    __logger = getLogger(__name__)

    def __init__(self, p_config):
        """Configure population.

        Args
        ----
        p_config (dict): The definition of the population and its current status.

        p_config has the following keys:
            signature (str): SHA256 of the population definition.
            log_table (str): A DB table used for tracking the generational changes in the population.
        """
        self.__table = database_table(population.__logger, 'populations')
        self.__log_table = database_table(population.__logger, p_config.log_table)
        self.definition = self.__table.load(['signature': p_config['signature']])
        self.individuals = self.definition['population_dict']


    def initialize(self, gene_pool, fitness_function=None):
        """Initialize the population.

        Before a population can be used all individuals must be brought into the gene_pool
        and validated. If the individuals of the population are already defined they are scored
        with the fitness_function and compared to the record in the population table. This
        is to verify the fitness function is consistent with the previous work. A WARNING
        is logged if there is a mismatch. If no individuals
        were defined the population initial query is used to define them.

        Args
        ----
        gene_pool (gene_pool): The gene pool from which this population will be drawn.
        fitness_function (func): Takes a population individual GC as a single argument.
        """
        if not self.individuals:
            initial_population = gene_pool.gl(self.definition['initial_query'], ['signature'])
            self.individuals = {s['signature']: self.gene_pool[s['signature']]) for s in initial_population}
            population.__logger.debug("Initial population: %s", self.individuals)
        else:
            individuals_updated = {s['signature']: self.gene_pool[s['signature']]) for s in self.individuals.keys()}
            for s in individuals_updated: individuals_updated[s]['__fitness': self.individuals[s]
            self.individuals = individuals_updated
            for gc in self.individuals.values():
                fitness = fitness_function(gc)
                if not isclose(gc['__fitness'], fitness):
                    population.__logger.warning("Fitness score for GC %s cannot be reproduced: Population fitness score %f versus worker fitness %f score",
                        signature, gc['__fitness'], fitness)


    def log(self):
        """Log the state of the population."""

        fitness_data = array([v['__fitness'] for v in self.individuals.values()])
        code_depth_data = array([k['code_depth'] for k in self.individuals.values()])
        codon_depth_data = array([k['codon_depth'] for k in self.individuals.values()])
        code_count_data = array([k['num_codes'] for k in self.individuals.values()])
        codon_count_data = array([k['raw_num_codes'] for k in self.individuals.values()])
        self.__log_table.store([{
            'fitness_min': float(amin(fitness_data)),
            'fitness_max': float(amax(fitness_data)),
            'fitness_mean': float(mean(fitness_data)),
            'fitness_median': float(median(fitness_data),
            'code_depth_min': int(amin(code_depth_data)),
            'code_depth_max': int(amax(code_depth_data)),
            'code_depth_mean': float(mean(code_depth_data)),
            'code_depth_median': int(median(code_depth_data)),
            'codon_depth_min': int(amin(codon_depth_data)),
            'codon_depth_max': int(amax(codon_depth_data)),
            'codon_depth_mean': float(mean(codon_depth_data)),
            'codon_depth_median': int(median(codon_depth_data)),
            'code_count_min': int(amin(code_count_data)),
            'code_count_max': int(amax(code_count_data)),
            'code_count_mean': float(mean(code_count_data)),
            'code_count_median': int(median(code_count_data)),
            'codon_count_min': int(amin(codon_count_data)),
            'codon_count_max': int(amax(codon_count_data)),
            'codon_count_mean': float(mean(codon_count_data)),
            'codon_count_median': int(median(codon_count_data))
        }])





