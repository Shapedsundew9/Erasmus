'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/genetic_code.py
Path: /home/shapedsundew9/Projects/Erasmus/src
Created Date: Sunday, January 5th 2020, 4:19:17 pm
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''


from random import choices
from numpy import float32, array, amax, amin


class genetic_code():

    __GC = 0
    __PARENT = 1
    __GCA = 2
    __GCB = 3


    # A genetic code is created from a gene pool (so GCA & GCB are references to GC objects not signatures)
    # Build a tree of GC references.
    # Each node in the tree references the GC it represents in the gene pool
    # and references to its parent node, the node that represents GC['GCA'] and the node
    # that represents GC['GCB'] if they exist else None
    def __init__(self, gc):
        addition_queue = [[gc, None, None, None]]
        self.root = addition_queue[0]
        self.node_list = [addition_queue[0]]
        self.__depths, self.__generations = [gc['code_depth']], [gc['generation']]
        while addition_queue:
            node = addition_queue.pop()
            if not node[genetic_code.__GC]['gca'] is None:
                addition_queue.append([gc['gca'], node, None, None])
                node[genetic_code.__GCA] = addition_queue[-1]
                self.node_list.append(addition_queue[-1])
                self.__depths.append(gc['gca']['code_depth'])
                self.__generations.append(gc['gca']['generation'])
            if not node[genetic_code.__GC]['gcb'] is None:
                addition_queue.append([gc['gcb'], node, None, None])
                node[genetic_code.__GCB] = addition_queue[-1]
                self.node_list.append(addition_queue[-1])
                self.__depths.append(gc['gca']['code_depth'])
                self.__generations.append(gc['gca']['generation'])
        self.__generations = array(self.__generations, dtype=float32)
        self.__depths = array(self.__depths, dtype=float32)
        self.__generations = float32(1.0) + (float32(1.0) - self.__generations / amax(self.__generations))
        self.__depths = float32(1.0) + (float32(1.0) - self.__depths / amax(self.__depths))


    def __node(self, node):
        return {'gc': node[genetic_code.__GC], 'parent': node[genetic_code.__PARENT], 'gca': node[genetic_code.__GCA], 'gcb': node[genetic_code.__GCB]}


    # Return a randomly selected weighted node
    # TODO: Need a lot of diagnostics around this to see how it behaves
    # Need to identify the instance of the a sub-GC to modifiy which is defined by the incoming
    # edge in the top level GC graph
    def select_gc(self, gpm, dpm):
        node = choices(self.node_list, self.__generations * gpm + self.__depths * dpm)
        return self.predecesors(node)


    # Return a list of all the predecesors to a given node.
    # The list is in the order parent, grandparent, great grandparent...
    def predecesors(self, node):
        retval = [self.__node(node)]
        parent = node[genetic_code.__PARENT]
        while not parent is None:
            retval.append(self.__node(parent))
            parent = parent[genetic_code.__PARENT]
        return retval


    