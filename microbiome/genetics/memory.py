'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/memory.py
Path: /home/shapedsundew9/Projects/Erasmus/src
Created Date: Sunday, January 19th 2020, 4:18:09 pm
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''

from numpy import float32, array


class memory():

    def __init__(self):
        self._store = {}


    def __getitem__(self, key):
        if not key in self._store: return array([float32(0.0)])
        return array([self._store[int(key)]])


    # Stores the value in self._store returning its position
    def set(self, key, value):
        self._store[key] = float32(value)
        return array([value])