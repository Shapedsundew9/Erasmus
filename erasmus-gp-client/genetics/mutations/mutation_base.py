'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/mutation.py
Path: /home/shapedsundew9/Projects/Erasmus/src
Created Date: Friday, January 10th 2020, 8:42:23 am
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''


from logging import getLogger


# Base class for all mutations
# Derived classes have the following naming convention (regex):
#   mutation_[rti][ridm][cgi][0-9]{3}
# where
#   [rti]    = (r)andom, (t)argeted or (i)ntelligent
#   [ridm]   = (r)eplicate, (insert), (d)elete or (m)odify
#   [cgi]    = (c)odon, (g)ene or (i)nput
#   [0-9]{3} = an arbitary 3 digit integer

# TODO:
# Swap random inputs within a genetic code entry
# Swap random inputs between genetic code entries
# 
class mutation_base():


    _logger = getLogger(__name__)

    
    def __init__(self, name, weight=1.0):
        self.name = name
        self.weight = weight
        self.code = None


    # Insert new_entry into code at index
    def _insert(self, new_code, new_entry, index):
        mutation_base._logger.debug("New entry: %s", new_entry)
        ni = new_code.num_inputs()
        mutation_base._logger.debug("Cloned code:\n%s", new_code)

        # Extend the inputs and outputs of the mutated code
        new_code.extend_inputs(new_entry.num_inputs())
        rco = new_entry.num_outputs()
        new_code.extend_outputs(rco)
        mutation_base._logger.debug("Extended IO code:\n%s", new_code)

        # Define the new entries input references and the mutated codes extended inputs
        for pos, ref in enumerate(new_entry.input): ref.pos = pos + ni
        new_code.insert_entry(new_entry, index)
        mutation_base._logger.debug("Inserted new entry:\n%s", new_code)

        # Define the mutated codes extended output entry input references
        for pos, ref in enumerate(new_code.entries[-1].input[-rco:]): ref.row, ref.pos = index, pos
        mutation_base._logger.debug("%s inserted genetic code %d in position %d", self.code, new_entry.idx, index)
        mutation_base._logger.debug("Final mutated code:\n%s", new_code)

        return new_code


    # Must return a new code object or None
    def mutate(self, code, partners=None):
        raise NotImplementedError()