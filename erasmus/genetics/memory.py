'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/memory.py
Path: /home/shapedsundew9/Projects/Erasmus/src
Created Date: Sunday, January 19th 2020, 4:18:09 pm
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''


from numpy import int32


class memory():

    def __init__(self):
        self._store = []


    def __getitem__(self, key):
        return self._store[key]


    # Stores the value in self._store returning its position
    def __setitem__(self, key, value):
        idx = int32(key)
        if idx < 0 or idx >= len(self._store):
            self._store.append(value)
            return len(self._store) - 1
        self._store[key] = value
        return key