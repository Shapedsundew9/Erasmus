'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/codon.py
Path: /home/shapedsundew9/Projects/Erasmus/src
Created Date: Thursday, December 26th 2019, 10:51:24 am
Author: Shaped Sundew

Copyright (c) 2019 Your Company
'''


class codon():


    def __init__(self, func, name, desc=None, isUnary=False, isTernary=False, isBranch=False, isAddressing=False):
        self.func = func
        self.desc = desc
        self.isUnary = isUnary
        self.isBranch = isBranch
        self.isIndex = isAddressing
        self.isTernary = isTernary


    def exec(self, input):
        return self.func(input[0]) if not self.isUnary or self.isBranch else self.func(input[0], input[1])

