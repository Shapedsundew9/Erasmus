import sys, inspect
import numpy
from pprint import pformat


_types = {}
_codons = {}
#_modules = ('numpy', 'builtins')
_modules = ('builtins',)


def get_type(cls_obj):
    if len(cls_obj.__bases__) == 1:
        return cls_obj.__bases__[0].__module__ + '.' + cls_obj.__bases__[0].__name__
    return [n.__module__ + '.' + n.__name__ for n in cls_obj.__bases__]


def get_signature(func):
    try:
        return inspect.signature(func)
    except:
        return None


# Return the qualified name of all the methods & functions in the class
def get_methods(cls_obj):
    callables = set()
    for _, function in inspect.getmembers(cls_obj, inspect.isfunction):
        if function.__name__[0] != '_':
            name = function.__module__ + '.' + function.__qualname__
            callables.add(name)
            if not name in _codons:
                _codons[name] = {"callable": function}
            else:
                assert _codons[name]["callable"] == function
    for _, method in inspect.getmembers(cls_obj, inspect.ismethoddescriptor):
        if method.__name__[0] != '_':
            name = method.__qualname__
            callables.add(name)
            if not name in _codons:
                _codons[name] = {"callable": method}
            else:
                assert _codons[name]["callable"] == method
    for co in cls_obj.__bases__: callables.update(get_methods(co))
    return callables


# Return the set of methods and functions that are not defined by a parent.
def methods_delta(cls_obj):
    callables = set()
    for co in cls_obj.__bases__: callables.update(get_methods(co))
    return list(get_methods(cls_obj) - callables)


def find_base(cls_obj):
    type_name = cls_obj.__module__ + '.' + cls_obj.__name__ 
    if not type_name in _types and cls_obj.__name__[0] != '_':
        _types[type_name] = {'type': get_type(cls_obj)}
        get_methods(cls_obj)
        for co in cls_obj.__bases__: find_base(co)
        _types[type_name]['codons'] = methods_delta(cls_obj)


for m in _modules:
    for _, cls_obj in inspect.getmembers(sys.modules[m], inspect.isclass):
        find_base(cls_obj)
"""
    for _, function in inspect.getmembers(sys.modules[m], inspect.isfunction):
        print(function, print_signature(function))
    for _, function in inspect.getmembers(sys.modules[m], inspect.isbuiltin):
        print(function, print_signature(function))
"""


print(len(_codons))
print(pformat(_types))
print(pformat(_codons))
