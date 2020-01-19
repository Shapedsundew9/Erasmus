'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/codon.py
Path: /home/shapedsundew9/Projects/Erasmus/src
Created Date: Thursday, December 26th 2019, 10:51:24 am
Author: Shaped Sundew

Copyright (c) 2019 Your Company
'''


from inspect import signature


class codon():

    def __init__(self, func, name, desc=None, isMemory=False):
        self.func = func
        self.name = name
        self.desc = desc
        self.isMemory = isMemory
        

    def exec(self, d, m):
        if not callable(self.func): return self.func
        if self.isMemory: return self.func(m, *d[0:len(signature(self.func).parameters) - 1])
        return self.func(*d[0:len(signature(self.func).parameters)])