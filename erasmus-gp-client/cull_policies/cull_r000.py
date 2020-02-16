'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/cull_policies/cull_r000.py
Path: /home/shapedsundew9/Projects/Erasmus/src/cull_policies
Created Date: Saturday, January 18th 2020, 3:28:11 pm
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''

from .cull_base import cull_base
from numpy.random import randint


class cull_r000(cull_base):

    def __init__(self, weight=1.0):
        super().__init__('random', weight)
        self.code = 'r000'


    def cull(self, population, num=1):
        return [randint(len(population.agents)) for _ in range(num)]

