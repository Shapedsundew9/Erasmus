'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/locales/logic_land.py
Path: /home/shapedsundew9/Projects/Erasmus/src/locales
Created Date: Saturday, January 18th 2020, 4:32:45 pm
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''


from numpy import array, meshgrid


# Generates all the combinations of boolean inputs for num inputs
def _inputs(num=2):
    boolean = [[True, False]] * num
    return array(meshgrid(*boolean)).T.reshape((-1, len(boolean)))


def ll_and():
    _in = _inputs(2)
    return (_in, array([i[0] and i[1] for i in _in]))
    