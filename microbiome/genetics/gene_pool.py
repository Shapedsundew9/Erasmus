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


def _reference():
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
class _gene_pool():


    _gl = None
    _CALLABLE_FILE_HEADER = "# Erasmus GP Gene Pool\n"
    _META_DATA_FIELDS = ('num_inputs', 'num_outputs', 'properties', 'alpha_class', 'beta_class')
    _logger = getLogger(__name__)


    def __init__(self, query=[{'gca': NULL_GC, 'gcb': NULL_GC}], callables_prefix=None, file_ptr=None):
        if gene_pool._gl is None: gene_pool._gl = genomic_library()
        self._query = query
        self._file_ptr = NamedTemporaryFile(mode='w', suffix='.py', prefix=callables_prefix, delete=False) if file_ptr is None else open(file_ptr, 'w')
        self._file_ptr.write(gene_pool._CALLABLE_FILE_HEADER)
        self._file_ptr.close()
        gene_pool._logger.info("Initial gene pool query: %s", str(query))
        self._gene_pool = {}
        path.insert(1, dirname(abspath(self._file_ptr.name)))
        self._module = import_module(basename(self._file_ptr.name)[:-3])
        self._push_queue = []
        self._update()
 

    def __getitem__(self, signature):
        if signature not in self._gene_pool:
            gcs = self.extended_genetic_code(gene_pool._gl[signature], stored=True)
            self.add(gcs)
        return self._gene_pool[signature]


    def function_name(self, signature):
        return "gc_" + signature


    # Any GCs pulled from the genomic library are by definition valid
    def _update(self):
        gcs = [self.extended_genetic_code(gc, stored=True) for gc in gene_pool._gl.load(self._query)]
        self.add(gcs)


    def _function_not_found(self, name):
        gene_pool._logger.error("The the GC function %s cannot be found.", name)


    def _write_arg(self, iab, c):
        return "(" + ", ".join([str(c[arg[1]]) if arg[0] == 'C' else arg[0].lower() + "[" + str(arg[1]) + "]" for arg in iab]) + ",)"
        

    def _create_callables(self, active_gcs):
        file_ptr = open(self._file_ptr.name, "w")
        gene_pool._logger.debug("Gene pool file created: %s", file_ptr.name)
        file_ptr.write(gene_pool._CALLABLE_FILE_HEADER)    
        file_ptr.write("\n\nfrom microbiome.genetics.gc_mutation_functions import *\nfrom random import random, uniform\n\n\n")
        for gc in active_gcs:
            if gene_pool._logger.getEffectiveLevel() == DEBUG: file_ptr.write("'''\n{}\n'''\n".format(pformat({k: v for k, v in gc.items() if k[:2] != '_'})))    
            file_ptr.write("def " + self.function_name(gc['signature']) + "(i):\n")
            if not 'function' in gc['meta_data']:
                c = gc['graph']['C'] if 'C' in gc['graph'] else [] 
                if gc['gca'] != NULL_GC: file_ptr.write("\ta = " + self.function_name(gc['gca']) + "(" + self._write_arg(gc['graph']['A'], c) + ")\n")
                if gc['gcb'] != NULL_GC: file_ptr.write("\tb = " + self.function_name(gc['gcb']) + "(" + self._write_arg(gc['graph']['B'], c) + ")\n")
                file_ptr.write("\treturn " + self._write_arg(gc['graph']['O'], c) + "\n\n\n")
            else:
                format_dict = {'c' + str(i): v for i, v in enumerate(gc['graph']['C'])} if 'C' in gc['graph'] else {}
                format_dict.update({'i' + str(i): 'i[{}]'.format(i) for i in range(gc['num_inputs'])})
                file_ptr.write("\treturn (" + gc['meta_data']['function']['python3']['0']['inline'].format(format_dict) + ",)\n\n\n")

        # Add some function meta_data
        file_ptr.write("meta_data = {\n\t")
        lines = []
        for gc in active_gcs:
            line = "'{}':{{".format(gc['signature']) + ','.join(["'{}': {}".format(k, gc[k]) for k in gene_pool._META_DATA_FIELDS])
            lines.append(line + ", 'callable': {} }}".format(self.function_name(gc['signature'])))
        file_ptr.write(',\n\t'.join(lines) + "\n}\n")
        file_ptr.close()
        if not self._module is None: reload(self._module)


    # Get from the genomic library
    def gl(self, queries):
        return [self.extended_genetic_code(gc, stored=True) for gc in gene_pool._gl.load(queries, fields)]


    def push(self):
        if self._push_queue: gene_pool._gl.store(self._push_queue)
        self._push_queue.clear()


    # Return the GC function
    def callable(self, signature):
        method = self.function_name(signature)
        return getattr(self._module, method, lambda: self._function_not_found(method))


    # Delete any GCs that were sent for deletion that have no references.
    def remove(self, gcs):
        delete_queue = [self._gene_pool[gc] for gc in gcs]
        while delete_queue:
            victim = delete_queue.pop()
            if not '_count' in victim or not victim['_count']:
                for _gcab in ('_gca', '_gcb'):
                    gc = victim[_gcab]
                    if not gc is None:
                        gc['_count'] -= 1
                        if not gc['_count']: delete_queue.append(gc)
                del self._gene_pool[victim['signature']]


    # Add a list of genetic codes to the gene pool
    # GCs added have no referencing GC they are considered active
    # Sub-codes will be added automatically if needed
    # GCA & GCB signatures will be replaced with references to the genetic code
    # A 'count' field is added counting the number of references to the GC within the gene pool
    def add(self, gcs, x=False):
        addition_queue = [self.extended_genetic_code(gc) for gc in gcs if gc['signature'] != NULL_GC] if not x else gcs
        signature_queue = [xgc['signature'] for xgc in addition_queue]

        # Add to the gene pool
        # Link GCA & GCB directly to thier GC objects
        # Add a 'count' of how many references a GC has in the gene pool
        while addition_queue:
            xgc = addition_queue.pop()
            signature = signature_queue.pop()
            if not signature in self._gene_pool:
                self._gene_pool[signature] = xgc
                self._push_queue.append(xgc)
                for _ab, ab in (('_gca', 'gca'), ('_gcb', 'gcb')):
                    if  xgc[ab] != NULL_GC:
                        if not xgc[ab] in self._gene_pool:
                            if not xgc[ab] in signature_queue:
                                gene_pool._logger.debug("Loading GCAB %s from genomic library.", xgc[ab])
                                addition_queue.append(self.extended_genetic_code(gene_pool._gl[xgc[ab]], stored=True))
                                signature_queue.append(addition_queue[-1]['signature'])
                                xgc[_ab] = addition_queue[-1]
                                xgc[_ab]['_count'] = 1
                            else:
                                xgc[_ab] = addition_queue[signature_queue.index(xgc[ab])]
                                xgc[_ab]['_count'] += 1
                        else:
                            xgc[_ab] = self._gene_pool[xgc[ab]]
                            xgc[_ab]['_count'] += 1
        self._create_callables(self._gene_pool.values())

    
    def extended_genetic_code(self, gc, count=0, stored=False):
        """Extend the gc dictionary with gene pool specific fields.

        The supplied genetic code dictionary, gc, is updated to include
        the extended fields to reduce duplication and increase performance.
        Keys of the format '_microbiome_.*' are used to snapshot fields that
        may be altered in parallel by other workers.  

        All xGC keys start with '_'.
            '_valid' (bool): True if the xGC is a valid GC.
            '_count' (int): The number of times this xGC is referenced by other xGCs.
            '_gca' (xGC): The xGC of GCA or None if GCA is the NULL_GC.
            '_gcb' (xGC): The xGC of GCB or None if GCB is the NULL_GC.
            '_ref' (int): The gene pool unique reference.
            '_target_fitness' (float): The target fitness (None if the GC is a mutation).
            '_previous_fitness' (float): The fitness from the previous evaluation.
            '_mutated_by' (xGC): The GC that mutated this GC last.
            '_parasites' (list): List of xGCs having a parasitic role in mutation to create this GC.
            '_func' (func): The executable code for this GC.
            '_microbiome_fitness': The fitness the GC had when it was last synchronised with the biome.
            '_microbiome_evolvability': The evolvability the GC had when it was last synchronised with the biome.
            '_stored': The GC has been perisited in the Genomic Library storage. 

        Args
        ----
            gc (dict): An application format genetic code.

        Returns
        -------
            (dict): The extended genetic code dictionary.
        """
        gc['_valid'] = True
        gc['_count'] = count
        gc['_gca'] = None
        gc['_gcb'] = None
        gc['_ref'] = _reference()
        gc['_target_fitness'] = 0.0
        gc['_previous_fitness'] = 0.0
        gc['_mutated_by'] = None
        gc['_parasites'] = []
        gc['_func'] = None
        gc['_microbiome_fitness'] = gc['fitness']
        gc['_microbiome_evolvability'] = gc['evolvability']
        gc['_stored'] = stored
        return gc


gene_pool = _gene_pool()