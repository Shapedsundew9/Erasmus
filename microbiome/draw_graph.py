'''
Filename: /home/shapedsundew9/Projects/Erasmus/microbiome/draw_graph.py
Path: /home/shapedsundew9/Projects/Erasmus/microbiome
Created Date: Monday, June 15th 2020, 9:15:00 am
Author: Shapedsundew9

Copyright (c) 2020 Your Company
'''


from graph_tool import Graph
from graph_tool.draw import graph_draw, sfdp_layout


class draw_graph:

    def __init__(self):
        self.__graph = Graph()
        self.__vlabel = self.__graph.new_vertex_property("string")
        self.__vsize = self.__graph.new_vertex_property("float")
        self.__vcolour = self.__graph.new_vertex_property("float")
        self.__eweight = self.__graph.new_edge_property("float")
        self.__elabel = self.__graph.new_vertex_property("string")


    def add_vertex(self, label="None", size=0, colour=0):
        v = self.__graph.add_vertex()
        self.__vlabel[v] = label
        self.__vsize[v] = size
        self.__vcolour[v] = colour
        return v


    def add_edge(self, v1, v2, label="None", weight=0):
        e = self.__graph.add_edge(v1, v2)
        self.__elabel[e] = label
        self.__eweight[e] = weight


    def draw(self, base_name, vlabels=True, vsize=True, vcolour=True, elabel=False, eweight=False):
        graph_draw(self.__graph, output_size=(1000, 1000), output=base_name + '.png')