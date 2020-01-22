'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/locales/io.py
Path: /home/shapedsundew9/Projects/Erasmus/src/locales
Created Date: Tuesday, January 21st 2020, 6:13:41 pm
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''

from numpy.random import randint
from numpy import array, iinfo, int32

_MIN_SCALAR = iinfo(int32).min
_MAX_SCALAR = iinfo(int32).max
_MIN_VECTOR = 1
_MAX_VECTOR = 128


def scalar_identity():
    i = array([randint(2**30)])
    return (i, i)


def _D_identity(num=1):
    i = array([randint(_MIN_SCALAR, _MAX_SCALAR, size=(randint(_MIN_VECTOR, _MAX_SCALAR, size=num)))])
    return (i, i)


def oneD_identity():
    return _D_identity(1)
   

def twoD_identity():
    return _D_identity(2)


def threeD_identity():
    return _D_identity(3)


#TODO: Add n-dimensionsal version