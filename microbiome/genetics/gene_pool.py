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
from numpy import int64, float32, zeros, ndarray, array
from copy import copy
from ..draw_graph import draw_graph
from sys import path
from os.path import dirname, abspath, basename
from importlib import import_module, reload


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
        return self.__gene_pool[signature]


    def function_name(self, signature):
        return "gc_" + signature


    def __update(self):
        self.update(gene_pool.__gl.load(self.__query), push=False)


    def __function_not_found(self, name):
        gene_pool.__logger.error("The the GC function %s cannot be found.", name)


    def __write_arg(self, iab, c):
        last_arg = len(iab)
        line = ""
        for pos, arg in enumerate(iab, 1):
            line = str(c[arg[1]]) if arg[0] == 'C' else arg[0].lower() + "[" + str(arg[1]) + "]" 
            line += ", " if pos < last_arg else ")\n"
        return line


    def __create_callables(self, active_gcs):
        file_ptr = open(self.__file_ptr.name, "w")
        gene_pool.__logger.debug("Gene pool file created: %s", file_ptr.name)
        file_ptr.write(gene_pool.__CALLABLE_FILE_HEADER)    
        file_ptr.write("\n\nfrom microbiome.genetics.gc_mutation_functions import *\nfrom random import random, uniform\n\n\n")
        signature_list = list(self.__gene_pool.keys())
        for signature in sorted(signature_list):
            gc = self.__gene_pool[signature]
            file_ptr.write("def " + self.function_name(signature) + "(i):\n")
            if not 'function' in gc['meta_data']:
                c = gc['graph']['C'] if 'C' in gc['graph'] else [] 
                if gc['gca'] != NULL_GC: file_ptr.write("\ta = " + self.function_name(gc['gca']) + "((" + self.__write_arg(gc['graph']['A'], c)) + ")"
                if gc['gcb'] != NULL_GC: file_ptr.write("\tb = " + self.function_name(gc['gcb']) + "((" + self.__write_arg(gc['graph']['B'], c)) + ")"
                file_ptr.write("\treturn (" + self.__write_arg(gc['graph']['O'], c)) + ",)\n\n\n"
            else:
                format_dict = {'c' + str(i): v for i, v in enumerate(gc['graph']['C'])} if 'C' in gc['graph'] else {}
                format_dict.update({'i' + str(i): 'i[{}]'.format(i) for i in range(gc['num_inputs'])})
                file_ptr.write("\treturn (" + gc['meta_data']['function']['python3']['0']['inline'].format(format_dict) + ",)\n\n\n")

        # Add some function meta_data
        file_ptr.write("meta_data = {\n\t")
        lines = []
        for gc in self.__gene_pool.values():
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


    # Add a list of genetic codes to the gene pool
    # GCs added have no referencing GC they are considered active
    # Sub-codes will be added automatically if needed
    # GCA & GCB signatures will be replaced with references to the genetic code
    # A 'count' field is added counting the number of references to the GC within the gene pool
    def update(self, gcs, delete_queue=None, push=True):
        addition_queue = [gc for gc in gcs if gc['signature'] != NULL_GC]
        signature_queue = [gc['signature'] for gc in addition_queue]
        zero_count_list = []
        if delete_queue is None: delete_queue = [] 

        # Add to the gene pool
        # Link GCA & GCB directly to thier GC objects
        # Add a 'count' of how many references a GC has in the gene pool
        while addition_queue:
            gc = addition_queue.pop()
            signature = signature_queue.pop()
            if not signature in self.__gene_pool:
                self.__gene_pool[signature] = gc
                self.__push_queue.append(gc)
                if '__count' not in gc:
                    gc['__count'] = 0
                    zero_count_list.append(signature)
                for __ab, ab in (('__gca', 'gca'), ('__gcb', 'gcb')):
                    if not gc[ab] in self.__gene_pool:
                        if not gc[ab] in signature_queue:
                            if  gc[ab] == NULL_GC:
                                gc[__ab] = None
                            else:
                                addition_queue.append(gene_pool.__gl[gc[ab]])
                                signature_queue.append(addition_queue[-1]['signature'])
                                gc[__ab] = addition_queue[-1]
                                gc[__ab]['__count'] = 1
                        else:
                            gc[__ab] = addition_queue[signature_queue.index(gc[ab])]
                            if not '__count' in gc[__ab]: gc[__ab]['__count'] = 0
                            gc[__ab]['__count'] += 1
                    else:
                        gc[__ab]['__count'] += 1

        # Delete any GCs that were sent for deletion that have no references.
        delete_queue = [signature for signature in delete_queue if not self.__gene_pool[signature]['count']]
        while delete_queue:
            victim = delete_queue.pop()
            for __gcab in ('__gca', '__gcb'):
                gc = self.__gene_pool[victim][__gcab]
                if not gc is None:
                    gc['__count'] -= 1
                    if not gc['__count']: delete_queue.append(gc['signature'])
            del self.__gene_pool[victim]

        # Create a a genetic_code node tree for top level (0 gene pool reference count) GCs
        for signature in zero_count_list:
            # GC's put on the zero count list may not have zero count by the time we process the list
            if not self.__gene_pool[signature]['__count']: self.__gene_pool[signature]['__genetic_code'] = genetic_code(self.__gene_pool[signature])
        
        # Update the genomic library
        if push: self.push()

        # Re-create the callables file
        self.__create_callables(self.__gene_pool.keys())


    def validate(self, entry):
        return gene_pool.__gl.validate(entry)


    def normalize(self, entry):
        return gene_pool.__gl.normalize(entry)


    def draw(self, root=None):
        dg = draw_graph()
        node_list = [root] if not root is None else [gc['signature'] for gc in self.__gene_pool.values() if gc['count'] == 0]
        for node in node_list: node['vertex'] = dg.add_vertex()

        while node_list:
            node = self.__gene_pool[node_list.pop()]
            for gcab in ('gca', 'gcb'):
                if not self.__gene_pool[gcab] is None:
                    if not 'vertex' in self.__gene_pool[gcab]: self.__gene_pool[gcab]['vertex'] = dg.add_vertex()
                    dg.add_edge(node['vertex'], self.__gene_pool[gcab]['vertex'])
                    node_list.append(gcab)

        dg.draw("gene_pool")