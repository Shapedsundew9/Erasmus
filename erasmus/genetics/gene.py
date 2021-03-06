'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/genetic_code.py
Path: /home/shapedsundew9/Projects/Erasmus/src
Created Date: Sunday, January 5th 2020, 4:19:17 pm
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''


from .genetic_code import genetic_code
from .codon_library import codon_library
from .genomic_library import genomic_library
from .genomic_library_entry import genomic_library_entry
from numpy import array, zeros, float32
from logging import getLogger
#from graph_tool.all import Graph


# gene() is a wrapper to a genetic_code that makes it executable.
# This layer is abstracted as there are opportunities for optimisation and caching
# of genes to increase performance.
class gene():


    _glib = genomic_library()
    _logger = getLogger(__name__)


    # seed is a genetic_code or an index to one
    def __init__(self, gc=None):
            if isinstance(gc, genomic_library_entry): gc = genetic_code(library_entry=gc) 
            self.genetic_code = genetic_code() if gc is None else gc
 

    def exec(self, d=array([]), m=None):
        for i, g in enumerate(self.genetic_code.entries, 1):
            gene._logger.debug("Input to entry %d (%s): %s", i, g, d)
            num_params = len(g.input)
            if d.shape[0] < num_params:
                tmp = zeros((num_params), dtype=float32)
                tmp[0:d.shape[0]] = d
                d = tmp
            if d.shape[0] > num_params: d = d[:num_params]
            output = codon_library[g.idx].exec(d, m, g.output) if g.is_codon else gene(self._glib[g.idx]).exec(d, m)
            g.set_output(output)
            if i < len(self.genetic_code.entries): d = self.genetic_code.get_inputs(i)
        return d


    def add_code_to_library(self, meta_data=None):
        return gene._glib.add_code(self.genetic_code, meta_data)

