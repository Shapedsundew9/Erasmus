'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/mutation.py
Path: /home/shapedsundew9/Projects/Erasmus/src
Created Date: Friday, January 10th 2020, 8:42:23 am
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''

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

    def __init__(self, name, weight=1.0):
        self.name = name
        self.weight = weight
        self.code = None


    # Must return a new code object
    def mutate(self, code, partners=None):
        raise NotImplementedError()