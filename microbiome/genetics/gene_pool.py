'''
Filename: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics/gene_pool.py
Path: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics
Created Date: Monday, April 13th 2020, 10:36:07 am
Author: Shapedsundew9

Copyright (c) 2020 Your Company
'''


from .config import get_config
from .genomic_library import genomic_library


_CONFIG_SECTION = "population"

# The gene_pool organises genetic codes for a worker. Each worker has its own gene pool.
# The gene pool is responsbile for:
#   1. Gathering an inital population of genetic codes from the genomic library based on the criteria provided by the worker.
#   2. Creating a callable object for each genetic code in the pool.
#   3. Applying any execution time optimisations.
#   4. Adding new (mutated) genetic codes from the worker.
#   5. Purging unused genetic codes.
#   6. Restarting from the last saved state
# The gene pool does not persist state.
# The gene pool is not the same as the population.

# TODO: Can optimise how often code is regenerated & imported by making a hierarchy of volatility
# TODO: Can reduce memory by only reading in fields needed for function.
# TODO: Add selection criteria to initial population
class gene_pool():


    __gc = genomic_library()


    def __init__(self):
        self.__directory, self.__query = get_config(_CONFIG_SECTION, ('working_directory', 'initial_query'))
        if not self.__verify_assets()
        self.__gene_pool = self.__gc.get(self.__query)
        self.__create_callables()
        
        
    def __create_callables(self):
        
