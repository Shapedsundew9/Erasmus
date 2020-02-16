from erasmus.genetics.genomic_library import genomic_library
from erasmus.population import population
from erasmus.locales.io import scalar_identity, oneD_identity, identity_fitness
from logging import basicConfig, INFO, DEBUG
from numpy.random import randint
from functools import partial
from numpy import array, float32


# Logging
basicConfig(filename=__name__ + '.log', filemode='w', format='%(asctime)s %(levelname)-8s %(name)-42s %(message)s', level=DEBUG)


# Needs an empty gene_pool for these tests
_ = genomic_library(name='test_library', temp=True)

    
def test_scalar():
    fitness_function = partial(identity_fitness, environment=scalar_identity())
    p = population(fitness_function, 10, 1000)
    p.evolve_until(5.0)
 

def test_oneD():
    fitness_function = partial(identity_fitness, environment=oneD_identity())
    p = population(fitness_function, 10, 1000)
    p.evolve_until(2.0)

