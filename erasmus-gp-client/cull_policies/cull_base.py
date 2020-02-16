'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/cull_policies/cull_base.py
Path: /home/shapedsundew9/Projects/Erasmus/src/cull_policies
Created Date: Saturday, January 18th 2020, 3:23:21 pm
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''


# Base class for all cull_policies
# Derived classes have the following naming convention (regex):
#   cull_[rti][ridm][cgi][0-9]{3}
# where
#   [rti]    = (r)andom, (t)argeted or (i)ntelligent
#   [0-9]{3} = an arbitary 3 digit integer

# TODO:
#
class cull_base():

    def __init__(self, name, weight=1.0):
        self.name = name
        self.weight = weight
        self.code = None


    # Must return a new code object
    def cull(self, population):
        raise NotImplementedError()
        # Return list of indices in population._agents to cull