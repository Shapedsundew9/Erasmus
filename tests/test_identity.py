from erasmus.genetics.genomic_library import genomic_library
from erasmus.population import population
from erasmus.locales.io import scalar_identity, scalar_identity_fitness
from logging import basicConfig, INFO, DEBUG
from numpy.random import randint
from functools import partial
from numpy import array, float32


# Logging
basicConfig(filename=__name__ + '.log', filemode='w', format='%(asctime)s %(levelname)-8s %(name)-42s %(message)s', level=INFO)


# Needs an empty gene_pool for these tests
_ = genomic_library(name='test_library', temp=True)

    
def test_scalar():
    fitness_function = partial(scalar_identity_fitness, enviroment=scalar_identity, target=array([2.0], dtype=float32))
    p = population(fitness_function, 10, 1000)
    p.evolve_until(2.0)
    print(p.agents[0]._gene.genetic_code)
    #p.agents[0]._gene.genetic_code.draw()