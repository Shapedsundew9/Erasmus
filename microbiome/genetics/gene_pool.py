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
from tempfile import NamedTemporaryFile
from graph_tool import Graph
from numpy import int64


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
        self.__callable_file_ptr = None
        gene_pool.__logger.info("Initial gene pool query: %s", str(query))
        self.__gene_pool = {gc['signature']: gc for gc in gene_pool.__gl.load(query)}
        self.graph = None
        self.__create_callables(self.__gene_pool.keys())


    def __function_name(self, signature):
        return "gc_" + signature


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
            c = gc['graph']['C'] if 'C' in gc['graph'] else [] 
            if gc['gca'] != NULL_GC: self.__callable_file_ptr.write("\ta = " + self.__function_name(gc['gca']) + "((" + self.__write_arg(gc['graph']['A'], c)) + ")"
            if gc['gcb'] != NULL_GC: self.__callable_file_ptr.write("\tb = " + self.__function_name(gc['gcb']) + "((" + self.__write_arg(gc['graph']['B'], c)) + ")"
            self.__callable_file_ptr.write("\treturn (" + self.__write_arg(gc['graph']['O'], c)) + "\n\n"
        else:
            self.__callable_file_ptr.write(gc['meta_data']['function']['python3']['0']['callable'] + "\n\n")


    def __add_to_graph(self, gc, parent=None):
        if 'vertex' not in gc:
            gc['vertex'] = self.graph.add_vertex()
            self.graph.vertex_properties.signature[gc['vertex']] = gc['signature']
        if not parent is None:
            if 'vertex' not in parent:
                parent['vertex'] = self.graph.add_vertex()
                self.graph.vertex_properties.signature[parent['vertex']] = parent['signature']
            if not parent['vertex'] in gc['vertex'].get_in_neighbors(): self.graph.add_edge(parent['vertex'], gc['vertex'])


    def __recurse_gcs(self, gc, parent=None):
        self.__add_to_graph(gc, parent)
        if not gc['signature'] in self.__gene_pool:
            self.__gene_pool[gc['signature']] = gc
            self.__write_gc_function(gc)
            if not gc['gca'] in self.__gene_pool and gc['gca'] != NULL_GC: self.__recurse_gcs(gene_pool.__gl[gc['gca']][0], gc)
            if not gc['gcb'] in self.__gene_pool and gc['gcb'] != NULL_GC: self.__recurse_gcs(gene_pool.__gl[gc['gcb']][0], gc)


    def __create_callables(self, active_gcs):
        self.graph = Graph()
        self.graph.vertex_properties['signature'] = self.graph.new_vp('string')
        self.__callable_file_ptr = NamedTemporaryFile(mode='w', suffix='.py', prefix=self.callables_prefix, delete=self.delete_callables_file)
        gene_pool.__logger.debug("Gene pool file created: %s", self.__callable_file_ptr.name)
        self.__callable_file_ptr.write(gene_pool.__CALLABLE_FILE_HEADER)    
        for gc in active_gcs:
            if gc['signature'] != NULL_GC: self.__recurse_gcs(gc)
        self.__callable_file_ptr.close()


    def __edge_list(self, signature, incoming_edge=None):
        edge_list = [] if incoming_edge is None else [(self.__gene_pool[signature], incoming_edge)]
        for edge in self.__gene_pool[signature]['vertex'].get_out_edges():
            edge_list.extend(self.__edge_list(self.graph.vertex_properties.signature[edge.target()], edge))
        return edge_list


    def edge_list(self, signature):
        if 'edge_list' not in self.__gene_pool['signature']: self.__gene_pool['signature']['edge_list'] = self.__edge_list(signature)
        return self.__gene_pool['signature']['edge_list']


    # Creation of a new GC within an existing GC (signature) requires
    # modification of all of the GC's in between 
    def create(self, new, signature, parent_a, parent_b=None):
        if parent_b is None:
            new['generation'] = parent_a['generation'] + 1
            new['properties'] = parent_a['properties']
            new['meta_data'] = {'parents': [parent_a['signature']]}
        else:
            new['generation'] = max((parent_a['generation'], parent_b['generation'])) + 1
            new['properties'] = {k: parent_a[k] or parent_b[k] for k in parent_a['properties'}
            new['meta_data'] = {'parents': [parent_a['signature']]}
