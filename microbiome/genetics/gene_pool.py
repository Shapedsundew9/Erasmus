'''
Filename: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics/gene_pool.py
Path: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics
Created Date: Monday, April 13th 2020, 10:36:07 am
Author: Shapedsundew9

Copyright (c) 2020 Your Company
'''

from logging import getLogger
from .genomic_library import genomic_library
from .genomic_library_entry_validator import NULL_GC
from .genetic_code import genetic_code
from tempfile import NamedTemporaryFile
from graph_tool import Graph
from numpy import int64
from copy import copy


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


    __gl = None
    __CALLABLE_FILE_HEADER = "# Erasmus GP Gene Pool\n\n\n"
    __logger = getLogger(__name__)


    def __init__(self, query=[{'gca': NULL_GC, 'gcb': NULL_GC}], delete_callables_file=True, callables_prefix=None):
        if gene_pool.__gl is None: gene_pool.__gl = genomic_library()
        self.delete_callables_file = delete_callables_file
        self.callables_prefix = callables_prefix
        gene_pool.__logger.info("Initial gene pool query: %s", str(query))
        self.__gene_pool = {}
        self.graph = None
        self.update(gene_pool.__gl.load(query))
        self.__create_callables(self.__gene_pool.keys())


    def __getitem__(self, signature):
        return self.__gene_pool[signature]


    def __function_name(self, signature):
        return "gc_" + signature


    def __write_arg(self, iab, c):
        last_arg = len(iab)
        line = ""
        for pos, arg in enumerate(iab, 1):
            line = str(c[arg[1]]) if arg[0] == 'C' else arg[0].lower() + "[" + str(arg[1]) + "]" 
            line += ", " if pos < last_arg else ")\n"
        return line


    def __create_callables(self, active_gcs):
        file_ptr = NamedTemporaryFile(mode='w', suffix='.py', prefix=self.callables_prefix, delete=self.delete_callables_file)
        gene_pool.__logger.debug("Gene pool file created: %s", file_ptr.name)
        file_ptr.write(gene_pool.__CALLABLE_FILE_HEADER)    
        for gc in self.__gene_pool.values(): 
            file_ptr.write("def " + self.__function_name(gc['signature'] + "(i):\n"))
            if not 'function' in gc['meta_data']:
                c = gc['graph']['C'] if 'C' in gc['graph'] else [] 
                if gc['gca'] != NULL_GC: file_ptr.write("\ta = " + self.__function_name(gc['gca']) + "((" + self.__write_arg(gc['graph']['A'], c)) + ")"
                if gc['gcb'] != NULL_GC: file_ptr.write("\tb = " + self.__function_name(gc['gcb']) + "((" + self.__write_arg(gc['graph']['B'], c)) + ")"
                file_ptr.write("\treturn (" + self.__write_arg(gc['graph']['O'], c)) + "\n\n"
            else:
                file_ptr.write(gc['meta_data']['function']['python3']['0']['callable'] + "\n\n")
        file_ptr.close()
        

    # Add a list of genetic codes to the gene pool
    # Ad GCs added have no referencing GC they are considered active
    # Sub-codes will be added automatically if needed
    # GCA & GCB signatures will be replaced with references to the genetic code
    # A 'count' field is added counting the number of references to the GC within the gene pool
    def update(self, gcs, delete=True):
        addition_queue = [gc for gc in gcs if gc['signature'] != NULL_GC]
        signature_queue = [gc['signature'] for gc in addition_queue]
        zero_count_list = []

        # To keep the cruft in the gene pool down delete any GCs that are not referenced by any others
        # To do that we make a list of all the GC's that have a reference count of zero BEFORE we add the
        # new GC's (many of which will have a count of 0 too)
        # Once the new GCs are added if any of this list still has zero references we recursively delete them
        delete_queue = [] if not delete else [gc['signature'] for gc in self.__gene_pool.values() if gc['count'] == 0]

        # Add to the gene pool
        # Link GCA & GCB directly to thier GC objects
        # Add a 'count' of how many references a GC has in the gene pool
        while addition_queue:
            gc = addition_queue.pop()
            signature = signature_queue.pop()
            if not signature in self.__gene_pool:
                self.__gene_pool[signature] = gc
                if 'count' not in gc:
                    gc['count'] = 0
                    zero_count_list.append(signature)
                for ab in ('gca', 'gbc'):
                    if not gc[ab] in self.__gene_pool:
                        if gc[ab] in signature_queue:
                            if  gc[ab] == NULL_GC:
                                gc[ab] = None
                            else:
                                addition_queue.append(gene_pool.__gl[gc[ab]])
                                signature_queue.append(addition_queue[-1]['signature'])
                                gc[ab] = addition_queue[-1]
                                gc[ab]['count'] = 1
                        else:
                            gc[ab] = addition_queue[signature_queue.index(ab)]
                            if not 'count' in gc[ab]: gc[ab]['count'] = 0
                            gc[ab]['count'] += 1
                    else:
                        gc[ab]['count'] += 1

        # Delete any GCs that had no references before before the new GCs were added
        # and still have no references after.
        delete_queue = [signature for signature in delete_queue if not self.__gene_pool[signature]['count']]
        while delete_queue:
            victim = delete_queue.pop()
            for gcab in ('gca', 'gcb'):
                gc = self.__gene_pool[victim][gcab]
                gc['count'] -= 1
                if not gc['count']: delete_queue.append(gc['signature'])
            del self.__gene_pool[victim]

        # Create a a genetic_code node tree for top level (0 gene pool reference count) GCs
        for signature in zero_count_list:
            # GC's put on the zero count list may not have zero count by the time we process the list
            if not self.__gene_pool[signature]['count']: self.__gene_pool[signature]['genetic_code'] = genetic_code(self.__gene_pool[signature])


    def normalize(self, entry):
        gene_pool.__gl.normalize({entry['signature']: entry})