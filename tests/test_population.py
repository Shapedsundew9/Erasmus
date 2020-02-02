from erasmus.genetics.genomic_library import genomic_library
from erasmus.population import population
from logging import basicConfig, info, DEBUG


# Logging
basicConfig(filename=__name__ + '.log', filemode='w', format='%(asctime)s %(levelname)-8s %(name)-40s %(message)s', level=DEBUG)


# Needs an empty gene_pool for these tests
#_ = genomic_library(name='test_library', temp=True)


# Check the population basics
def test_basics():
    p = population(lambda x: 1, initial_size=10, size_limit=10)

    # Check population size
    num = len(p)
    assert num == 10

    # Population should remain the same with the next generation
    p.next_generation()
    assert(len(p) == num)

    # Increase the population limit. In theory it could take more than one generation
    # to get to the limit (extremely unlikely to be more than one, nigh on impossible for 2) 
    p.set_size_limit(20)
    p.next_generation()
    p.next_generation()
    assert(len(p) == 20)




