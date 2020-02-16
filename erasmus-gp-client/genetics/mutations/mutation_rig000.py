'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/mutation_insert_gene.py
Path: /home/shapedsundew9/Projects/Erasmus/src
Created Date: Friday, January 10th 2020, 9:00:48 am
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''


from ..genomic_library import genomic_library
from .mutation_base import mutation_base
from ..genetic_code import genetic_code
from copy import deepcopy
from logging import getLogger


# Insert a random genetic_code from the genomic library at a random position
# Append new code inputs to inputs
# Append new code outputs to outputs
class mutation_rig000(mutation_base):

    _glib = genomic_library()
    _logger = getLogger(__name__)


    def __init__(self, weight=1.0):
        super().__init__('replicate', weight)
        self.code = 'rig000'


    def mutate(self, code, partners=None):
        # Create a clone and determine code to insert & position.
        index = code.random_index()
        new_entry = genetic_code(library_entry=self._glib.random_entry()).make_entry()
        mutation_rig000._logger.debug("New entry: %s", new_entry)
        ni = code.num_inputs()
        new_code = code.clone()
        mutation_rig000._logger.debug("Cloned code:\n%s", new_code)

        # Extend the inputs and outputs of the mutated code
        new_code.extend_inputs(new_entry.num_inputs())
        rco = new_entry.num_outputs()
        new_code.extend_outputs(rco)
        mutation_rig000._logger.debug("Extended IO code:\n%s", new_code)

        # Define the new entries input references and the mutated codes extended inputs
        for pos, ref in enumerate(new_entry.input): ref.pos = pos + ni
        new_code.insert_entry(new_entry, index)
        mutation_rig000._logger.debug("Inserted new entry:\n%s", new_code)

        # Define the mutated codes extended output entry input references
        for pos, ref in enumerate(new_code.entries[-1].input[-rco:]): ref.row, ref.pos = index, pos
        mutation_base._logger.debug("%s inserted genetic code %d in position %d", self.code, new_entry.idx, index)
        mutation_rig000._logger.debug("Final mutated code:\n%s", new_code)

        # B'zinga
        return new_code


        