'''
Filename: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics/gene_pool.py
Path: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics
Created Date: Monday, April 13th 2020, 10:36:07 am
Author: Shapedsundew9

Copyright (c) 2020 Your Company
'''


from .config import get_config
from .genomic_library import genomic_library
from .genomic_library_entry_validator import NULL_GC
from os.path import join


__UNIQUE_CHARS = 16
__CALLABLE_FILE_HEADER = "# Erasmus GP Gene Pool\n\n\n"
__CODON_ONLY_QUERY = [{'gca': NULL_GC, 'gcb': NULL_GC}]

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
class gene_pool():


    __gl = genomic_library()


    def __init__(self, worker_id, query=__CODON_ONLY_QUERY):
        self.__callable_path = join(working_directory, "gene_pool_" + worker_id + ".py")
        self.__callable_file_ptr = None
        self.__active_gcs = gene_pool.__gl.load(query)
        self.__gene_pool = set()
        self.__create_callables()


    def __function_name(self, signature):
        return "gc_" + signature[:__UNIQUE_CHARS]


    def __write_arg(self, iab, c):
        last_arg = len(iab)
        line = ""
        for pos, arg in enumerate(iab, 1):
            line = str(c[arg[1]]) if arg[0] == 'C' else arg[0].lower() + "[" + str(arg[1]) + "]" 
            line += ", " if pos < last_arg else ")\n"
        return line


    def __write_gc_function(self, gc):
        self.__callable_file_ptr.write("def " + self.__function_name(gc['signature'] + "(i):\n"))
        if not 'function' in gc['meta_data']:
            c = gc['graph']['C']
            self.__callable_file_ptr.write("\ta = " + self.__function_name(gc['gca']) + "((" + self.__write_arg(gc['graph']['A'], c)) + ")"
            if not gc['gcb'] == NULL_GC: self.__callable_file_ptr.write("\tb = " + self.__function_name(gc['gcb']) + "((" + self.__write_arg(gc['graph']['B'], c)) + ")"
        self.__callable_file_ptr.write("\treturn (" + self.__write_arg(gc['graph']['O'], c)) + "\n\n"


    def __recurse_gcs(self, gc):
        if not bytearray.fromhex(gc['signature']) in self.__gene_pool:
            self.__gene_pool.add()
            self.__write_gc_function(gc)
            if not 'function' in gc['meta_data']:  
                if not bytearray.fromhex(gc['gca']) in self.__gene_pool and gc['gca'] != NULL_GC: self.__recurse_gcs(gene_pool.__gl[gc['gca']])
                if not bytearray.fromhex(gc['gcb']) in self.__gene_pool and gc['gcb'] != NULL_GC: self.__recurse_gcs(gene_pool.__gl[gc['gcb']])


    def __create_callables(self):
        self.__callable_file_ptr = open(self.__callable_path, "w")
        self.__callable_file_ptr.write(__CALLABLE_FILE_HEADER)    
        for gc in self.__active_gcs: self.__recurse_gcs(gc)
        self.__callable_file_ptr.close()
