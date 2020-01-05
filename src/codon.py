'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/codon.py
Path: /home/shapedsundew9/Projects/Erasmus/src
Created Date: Thursday, December 26th 2019, 10:51:24 am
Author: Shaped Sundew

Copyright (c) 2019 Your Company
'''


class codon():


    def __init__(self, func, name, desc=None, isConstant=False, isUnary=False, isBinary=False,
                    isTernary=False, isBranch=False, isAddressing=False):
        self.func = func
        self.name = name
        self.desc = desc
        self.isConstant = isConstant
        self.isUnary = isUnary
        self.isBinary = isBinary
        self.isTernary = isTernary
        self.isBranch = isBranch
        self.isIndex = isAddressing
        assert(isConstant or isUnary or isBinary or isTernary,
            "Invalid codon construction: Must specify the number of parameters.")

        

    def exec(self, input):
        if self.isConstant: return self.func()
        if self.isUnary: return self.func(input[0])
        if self.isBinary: return self.func(input[0], input[1])
        if self.isTernary: return self.func(input[0], input[1], input[2])
        assert(False, "Invalid codon definition: Number of parameters not specified.")
