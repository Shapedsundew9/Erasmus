'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/genetic_code.py
Path: /home/shapedsundew9/Projects/Erasmus/src
Created Date: Sunday, January 5th 2020, 4:19:17 pm
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''


from random import choices
from numpy import float32, array, amax, amin
from ..draw_graph import draw_graph


class genetic_code():

    _GC = 0
    _PARENT = 1
    _GCA = 2
    _GCB = 3


    # A genetic code is created from a gene pool (so GCA & GCB are references to GC objects not signatures)
    # Build a tree of GC references.
    # Each node in the tree references the GC it represents in the gene pool
    # and references to its parent node, the node that represents GC['GCA'] and the node
    # that represents GC['GCB'] if they exist else None
    def __init__(self, gc):
        addition_queue = [[gc, None, None, None]]
        self.root = addition_queue[0]
        self.node_list = [addition_queue[0]]
        self._depths, self._generations = [gc['code_depth']], [gc['generation']]
        while addition_queue:
            node = addition_queue.pop()
            if not node[genetic_code._GC]['_gca'] is None:
                addition_queue.append([gc['_gca'], node, None, None])
                node[genetic_code._GCA] = addition_queue[-1]
                self.node_list.append(addition_queue[-1])
                self._depths.append(gc['_gca']['code_depth'])
                self._generations.append(gc['_gca']['generation'])
            if not node[genetic_code._GC]['_gcb'] is None:
                addition_queue.append([gc['_gcb'], node, None, None])
                node[genetic_code._GCB] = addition_queue[-1]
                self.node_list.append(addition_queue[-1])
                self._depths.append(gc['_gca']['code_depth'])
                self._generations.append(gc['_gca']['generation'])
        self._generations = array(self._generations, dtype=float32)
        self._depths = array(self._depths, dtype=float32)
        self._generations = float32(1.0) + (float32(1.0) - self._generations / amax(self._generations))
        self._depths = float32(1.0) + (float32(1.0) - self._depths / amax(self._depths))


    def _node(self, node):
        return {'gc': node[genetic_code._GC], 'parent': node[genetic_code._PARENT], '_gca': node[genetic_code._GCA], '_gcb': node[genetic_code._GCB]}


    # Return a randomly selected weighted node
    # TODO: Need a lot of diagnostics around this to see how it behaves
    # Need to identify the instance of the a sub-GC to modifiy which is defined by the incoming
    # edge in the top level GC graph
    def select(self, gpm, dpm):
        node = choices(self.node_list, self._generations * gpm + self._depths * dpm)
        return self.predecesors(node)


    # Return a list of all the predecesors to a given node.
    # The list is in the order parent, grandparent, great grandparent...
    def predecesors(self, node):
        retval = []
        parent = node[genetic_code._PARENT]
        while not parent is None:
            retval.append(self._node(parent))
            parent = parent[genetic_code._PARENT]
        return retval


    # Draw an image of the genetic code graph.
    # This function is usually slow.
    def draw(self):
        dg = draw_graph()
        self.root.append(dg.add_vertex())
        node_list = [self.root]
        while node_list:
            node = node_list.pop()
            for ab in (genetic_code._GCA, genetic_code._GCB):
                if not node[ab] is None:
                    node[ab].append(dg.add_vertex())
                    dg.add_edge(node[-1], node[ab][-1])
        dg.draw("genetic_code")


    