'''
Filename: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics/gene_pool.py
Path: /home/shapedsundew9/Projects/Erasmus/microbiome/genetics
Created Date: Monday, April 13th 2020, 10:36:07 am
Author: Shapedsundew9

Copyright (c) 2020 Your Company
'''

from logging import getLogger, DEBUG
from .genomic_library import genomic_library
from .genomic_library_entry_validator import NULL_GC, DEAD_GC_PREFIX
from .genetic_code import genetic_code
from tempfile import NamedTemporaryFile
from graph_tool import Graph
from numpy import int64, float32, zeros, ndarray, array
from copy import copy
from ..draw_graph import draw_graph
from sys import path
from os.path import dirname, abspath, basename
from importlib import import_module, reload
from pprint import pformat


def __reference():
    """Generate infinite reference sequence."""
    i = 0
    while True:
        yield i
        i += 1


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
    __CALLABLE_FILE_HEADER = "# Erasmus GP Gene Pool\n"
    __META_DATA_FIELDS = ('num_inputs', 'num_outputs', 'properties', 'alpha_class', 'beta_class')
    __logger = getLogger(__name__)


    def __init__(self, query=[{'gca': NULL_GC, 'gcb': NULL_GC}], callables_prefix=None, file_ptr=None):
        if gene_pool.__gl is None: gene_pool.__gl = genomic_library()
        self.__query = query
        self.__file_ptr = NamedTemporaryFile(mode='w', suffix='.py', prefix=callables_prefix, delete=False) if file_ptr is None else open(file_ptr, 'w')
        self.__file_ptr.write(gene_pool.__CALLABLE_FILE_HEADER)
        self.__file_ptr.close()
        gene_pool.__logger.info("Initial gene pool query: %s", str(query))
        self.__gene_pool = {}
        self.__module = None
        path.insert(1, dirname(abspath(self.__file_ptr.name)))
        self.__module = import_module(basename(self.__file_ptr.name)[:-3])
        self.__push_queue = []
        self.__update()
 

    def __getitem__(self, signature):
        if signature not in self.__gene_pool:
            gcs = gene_pool.__gl.load([{'signature': signature}])
            self.add(gcs)
        return self.__gene_pool[signature]


    def function_name(self, signature):
        return "gc_" + signature


    # Any GCs pulled from the genomic library are by definition valid
    def __update(self):
        gcs = gene_pool.__gl.load(self.__query)
        self.add(gcs)


    def __function_not_found(self, name):
        gene_pool.__logger.error("The the GC function %s cannot be found.", name)


    def __write_arg(self, iab, c):
        return "(" + ", ".join([str(c[arg[1]]) if arg[0] == 'C' else arg[0].lower() + "[" + str(arg[1]) + "]" for arg in iab]) + ",)"
        

    def __create_callables(self, active_gcs):
        file_ptr = open(self.__file_ptr.name, "w")
        gene_pool.__logger.debug("Gene pool file created: %s", file_ptr.name)
        file_ptr.write(gene_pool.__CALLABLE_FILE_HEADER)    
        file_ptr.write("\n\nfrom microbiome.genetics.gc_mutation_functions import *\nfrom random import random, uniform\n\n\n")
        for gc in active_gcs:
            if gene_pool.__logger.getEffectiveLevel() == DEBUG: file_ptr.write("'''\n{}\n'''\n".format(pformat({k: v for k, v in gc.items() if k[:2] != '__'})))    
            file_ptr.write("def " + self.function_name(gc['signature']) + "(i):\n")
            if not 'function' in gc['meta_data']:
                c = gc['graph']['C'] if 'C' in gc['graph'] else [] 
                if gc['gca'] != NULL_GC: file_ptr.write("\ta = " + self.function_name(gc['gca']) + "(" + self.__write_arg(gc['graph']['A'], c) + ")\n")
                if gc['gcb'] != NULL_GC: file_ptr.write("\tb = " + self.function_name(gc['gcb']) + "(" + self.__write_arg(gc['graph']['B'], c) + ")\n")
                file_ptr.write("\treturn " + self.__write_arg(gc['graph']['O'], c) + "\n\n\n")
            else:
                format_dict = {'c' + str(i): v for i, v in enumerate(gc['graph']['C'])} if 'C' in gc['graph'] else {}
                format_dict.update({'i' + str(i): 'i[{}]'.format(i) for i in range(gc['num_inputs'])})
                file_ptr.write("\treturn (" + gc['meta_data']['function']['python3']['0']['inline'].format(format_dict) + ",)\n\n\n")

        # Add some function meta_data
        file_ptr.write("meta_data = {\n\t")
        lines = []
        for gc in active_gcs:
            line = "'{}':{{".format(gc['signature']) + ','.join(["'{}': {}".format(k, gc[k]) for k in gene_pool.__META_DATA_FIELDS])
            lines.append(line + ", 'callable': {} }}".format(self.function_name(gc['signature'])))
        file_ptr.write(',\n\t'.join(lines) + "\n}\n")
        file_ptr.close()
        if not self.__module is None: reload(self.__module)


    # Get from the genomic library
    def gl(self, queries, fields):
        return gene_pool.__gl.load(queries, fields)


    def push(self):
        if self.__push_queue: gene_pool.__gl.store(self.__push_queue)
        self.__push_queue.clear()


    # Return the GC function
    def callable(self, signature):
        method = self.function_name(signature)
        return getattr(self.__module, method, lambda: self.__function_not_found(method))


    # Delete any GCs that were sent for deletion that have no references.
    def remove(self, gcs):
        delete_queue = [self.__gene_pool[gc] for gc in gcs]
        while delete_queue:
            victim = delete_queue.pop()
            if not '__count' in victim or not victim['__count']:
                for __gcab in ('__gca', '__gcb'):
                    gc = victim[__gcab]
                    if not gc is None:
                        gc['__count'] -= 1
                        if not gc['__count']: delete_queue.append(gc)
                del self.__gene_pool[victim['signature']]


    # Add a list of genetic codes to the gene pool
    # GCs added have no referencing GC they are considered active
    # Sub-codes will be added automatically if needed
    # GCA & GCB signatures will be replaced with references to the genetic code
    # A 'count' field is added counting the number of references to the GC within the gene pool
    def add(self, gcs):
        addition_queue = [self.extended_genetic_code(gc) for gc in gcs if gc['signature'] != NULL_GC]
        signature_queue = [xgc['signature'] for xgc in addition_queue]

        # Add to the gene pool
        # Link GCA & GCB directly to thier GC objects
        # Add a 'count' of how many references a GC has in the gene pool
        while addition_queue:
            xgc = addition_queue.pop()
            signature = signature_queue.pop()
            if not signature in self.__gene_pool:
                self.__gene_pool[signature] = xgc
                self.__push_queue.append(xgc)
                for __ab, ab in (('__gca', 'gca'), ('__gcb', 'gcb')):
                    if  xgc[ab] != NULL_GC:
                        if not xgc[ab] in self.__gene_pool:
                            if not xgc[ab] in signature_queue:
                                gene_pool.__logger.debug("Loading GCAB %s from genomic library.", xgc[ab])
                                addition_queue.append(gene_pool.__gl[xgc[ab]])
                                signature_queue.append(addition_queue[-1]['signature'])
                                xgc[__ab] = addition_queue[-1]
                                xgc[__ab]['__count'] = 1
                            else:
                                xgc[__ab] = addition_queue[signature_queue.index(xgc[ab])]
                                xgc[__ab]['__count'] += 1
                        else:
                            xgc[__ab] = self.__gene_pool[xgc[ab]]
                            xgc[__ab]['__count'] += 1
        self.__create_callables(self.__gene_pool.values())

    
    def extended_genetic_code(self, gc, count=0):
        """Extend the gc dictionary with gene pool specific fields.

        The supplied genetic code dictionary, gc, is updated to include
        the extended fields to reduce duplication and increase performance.

        All xGC keys start with '__'.
            '__valid' (bool): True if the xGC is a valid GC.
            '__count' (int): The number of times this xGC is referenced by other xGCs.
            '__gca' (xGC): The xGC of GCA or None if GCA is the NULL_GC.
            '__gcb' (xGC): The xGC of GCB or None if GCB is the NULL_GC.
            '__ref' (int): The gene pool unique reference.
            '__fitness' (float): Value between 0.0 and 1.0.
            '__previous_fitness' (float): The fitness from the previous evaluation.
            '__mutated_by' (xGC): The GC that mutated this GC last. 

        Args
        ----
            gc (dict): An application format genetic code.

        Returns
        -------
            (dict): The extended genetic code dictionary.
        """
        gc['__valid'] = True
        gc['__count'] = count
        gc['__gca'] = None
        gc['__gcb'] = None
        gc['__ref'] = __reference()
        gc['__fitness'] = 0.0
        gc['__previous_fitness'] = 0.0
        gc['__mutated_by'] = None
        return gc

