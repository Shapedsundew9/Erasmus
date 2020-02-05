'''
Filename: /home/shapedsundew9/Projects/Erasmus/src/genetic_code.py
Path: /home/shapedsundew9/Projects/Erasmus/src
Created Date: Sunday, January 5th 2020, 4:19:17 pm
Author: Shaped Sundew

Copyright (c) 2020 Your Company
'''

from hashlib import md5 as hash_function
from zlib import compress, decompress
from pickle import dumps, loads
from base64 import b64encode, b64decode
from numpy import array
from numpy.random import randint
from random import choices
from inspect import signature
from .genetic_code_entry import genetic_code_entry as entry
from .genomic_library_entry import genomic_library_entry
from .codon_library import codon_library
from graph_tool.all import Graph, sfdp_layout, graph_draw


_INPUT_ENTRY = 0
_OUTPUT_ENTRY = -1


# The genetic code is a list of gene/codon references & the connectivity
# entry = [inputs, reference to gene/codon, outputs]
# entries = [ input_entry, entry0, entry1, entry2, ... entryN, output_entry]
class genetic_code():


    def __init__(self, name=None, ancestor=None, codon_idx=None, constant=None, idx=None, library_entry=None):
        # TODO: Optimisation idea: entries is a list of entry's which is very inefficient.
        # Much less RAM can be used by arranging the components into numpy arrays
        # at the cost of construction time CPU.

        if library_entry == None:
            # self.entries = [input_entry, output_entry]
            self.entries = [entry(idx=0), entry(idx=1)]
            self.name = name
            self.ancestor = ancestor
            self.idx = idx
            if not codon_idx is None: self._initialise_with_codon(*codon_idx, constant)
        else:
            self.entries = self.zdeserialise(library_entry.data, library_entry.idx)
            self.name = library_entry.name
            self.ancestor = library_entry.ancestor
 

    def __getitem__(self, key):
        return self.entries[key]


    def __len__(self):
        return len(self.entries) - 2


    def __str__(self):
        ret_val = "Name: %s, Ancestor: %s, Library Index: %d\n".format((self.name, self.ancestor, self.idx))
        for e in self.entries: ret_val += str(e) + "\n"
        return ret_val


    def _initialise_with_codon(self, c, i, constant):
        self.name = c.name
        if not callable(c.func):
            self._initialise_with_constant(i, constant)
        else:
            num_param = len(signature(c.func).parameters)
            if num_param == 2: self._initialise_with_binary(i)
            if num_param == 1: self._initialise_with_unary(i)
            if num_param == 3: self._initialise_with_ternary(i)
            self.entries[_OUTPUT_ENTRY].set_input([len(self.entries) - 2, 0])        


    def _initialise_with_constant(self, i, constant):
        self.append(entry([constant], i, [constant]))


    def _initialise_with_unary(self, i):
        self.entries[_INPUT_ENTRY].set_input([1])        
        self.append(entry([[0, 0]], i, [0]))


    def _initialise_with_binary(self, i):
        self.entries[_INPUT_ENTRY].set_input([2])        
        self.append(entry([[0, 0], [0, 1]], i, [0]))


    def _initialise_with_ternary(self, i):
        self.entries[_INPUT_ENTRY].set_input([3])        
        self.append(entry([[0, 0], [0, 1], [0, 2]], i, [0]))


    def id(self):
        return hash_function(dumps(self.entries)).hexdigest()


    def zserialise(self):
        return b64encode(compress(dumps(self.entries), 9))


    def zdeserialise(self, obj, idx):
        self.entries = loads(decompress(b64decode(obj)))
        self.idx = idx
        return self


    def append(self, code):
        self.entries.insert(-1, code)
        return self


    def input_size(self)
        return self.entries[0].get_input()[0]


    def output_size(self)
        return self.entries[-1].get_output()[0]


    def insert(self, pos, code):
        input_options = [o for o in e.get_outputs() for e in self.entries[:pos + 1]]
        output_options = [i for i in self.entries[e].get_inputs() for e in self.entries[pos + 1:]]
        inputs = choices(input_options, k=code.input_size())
        outputs = choices(output_options, k=code.output_size())
        new_entry = entry(inputs, code.idx, outputs)
        self.entries.insert(pos + 1, new_entry)
        self._new_self()
        return self


    def _new_self(self):
        self.ancestor = self.idx
        self.name = None
        self.idx = None        


    def make_library_entry(self, meta_data=None):
        return genomic_library_entry(self.zserialise(), self.id(), self.ancestor, self.name, meta_data)


    def random_index(self):
        return 0 if not len(self) else randint(len(self))


    def _add_vertex(self, graph, name, is_func):
        v = graph.add_vertex()
        graph.vertex_properties.name = name
        graph.vertex_properties.type = is_func
        return v
        

    def draw(self, filename="genetic_code.png"):
        g = Graph()
        g.vertex_properties['name'] = g.new_vertex_property("string")
        g.vertex_properties['type'] = g.new_vertex_property("bool")
        entries_v_list = []
        for e in self.entries:
            entry_v = []
            if e.is_input():
                entry_v.append([self._add_vertex(g, 'i' + str(i), False) for i in range(e.get_input()[0])])
                entry_v.append(self._add_vertex(g, 'input', True))
                for v in entry_v[0]: g.add_edge(v, entry_v[1])
                entry_v.append([self._add_vertex(g, 'o' + str(i), False) for i in range(e.get_input()[0])])
                for v in entry_v[-1]: g.add_edge(entry_v[1], v)
            else:
                entry_v.append([])
                entry_v.append(self._add_vertex(g, e.get_name(), True))
                for i in e.get_input(): g.add_edge(entries_v_list[i[0]][2][i[1]], entry_v[-1])
                entry_v.append([self._add_vertex(g, 'o' + str(i), False) for i in range(e.get_output())])
                for v in entry_v[-1]: g.add_edge(entry_v[1], v)
            entries_v_list.append(entry_v)
            graph_draw(g, sfdp_layout(g), output_size=(1000, 1000), vertex_color=[1,1,1,0],
                    vertex_fill_color=g.vertex_properties['type'], vertex_size=1, edge_pen_width=1.2, output=filename)


