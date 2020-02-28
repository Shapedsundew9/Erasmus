'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/genomic_library_entry.py
Path: /home/shapedsundew9/Projects/Erasmus/src
Created Date: Friday, January 10th 2020, 10:38:13 am
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''


class genomic_library_entry():

    def __init__(self, data, eid, ancestor, name, meta_data=None, created=None, idx=None):
        self.data = data
        self.id = eid
        self.ancestor = ancestor
        self.name = name
        self.meta_data = meta_data
        self.created = created
        self.idx = idx

    def __str__(self):
        return str(self.__dict__)

