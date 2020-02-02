from erasmus.genetics.genomic_library import genomic_library
from erasmus.population import population
from erasmus.locales.io import scalar_identity, scalar_identity_fitness
from logging import basicConfig, info, DEBUG
from numpy.random import randint
from functools import partial
from numpy import array, float32


# Logging
basicConfig(filename=__name__ + '.log', filemode='w', format='%(asctime)s %(levelname)-8s %(name)-40s %(message)s', level=DEBUG)


# Needs an empty gene_pool for these tests
_ = genomic_library(name='test_library', temp=True)

    
def test_scalar():
    fitness_function = partial(scalar_identity_fitness, enviroment=scalar_identity, target=array([2.0], dtype=float32))
    p = population(fitness_function, 1, 1)
    p.next_generation()
    #p.agents[0]._gene.genetic_code.draw()