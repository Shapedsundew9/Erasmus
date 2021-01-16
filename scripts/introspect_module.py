import sys, inspect
import numpy
from pprint import pformat
from re import sub
from json import load, dump


METHOD_DEFINITIONS = {
    '__iter__': None,
    '__next__': None,
    '__reduce__': None,
    '__getattribute__': None,
    'mro': None,
    '__subclassess__': None,
    '__subclasscheck__': None,
    '__sizeof__': None,
    '__setattr__': None,
    '__repr__': None,
    '__call__': None
}

_types = {}
_codons = {}
#_modules = ('numpy', 'builtins')
#_modules = ('builtins',)
_modules = ('numpy',)


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
        if function.__name__[0] != '*':
            name = function.__module__ + '.' + function.__qualname__
            callables.add(name)
            if not name in _codons:
                _codons[name] = {"callable": function}
            else:
                assert _codons[name]["callable"] == function
    for _, method in inspect.getmembers(cls_obj, inspect.ismethoddescriptor):
        if method.__name__[0] != '*':
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
    # Strip out the module name.
    return [sub(r'^.*?\.', '', s) for s in (get_methods(cls_obj) - callables)]


def find_base(cls_obj):
    if not cls_obj.__module__ in _types: _types[cls_obj.__module__] = {} 
    if not cls_obj.__name__ in _types[cls_obj.__module__] and cls_obj.__name__[0] != '_':
        _types[cls_obj.__module__][cls_obj.__name__] = {'type': get_type(cls_obj)}
        get_methods(cls_obj)
        for co in cls_obj.__bases__: find_base(co)
        _types[cls_obj.__module__][cls_obj.__name__]['init'] = {}
        _types[cls_obj.__module__][cls_obj.__name__]['methods'] = {}
        _types[cls_obj.__module__][cls_obj.__name__]['special'] = {}
        for method in methods_delta(cls_obj):
            if method[0:2] == '__' and method[-2:] == '__':
                _types[cls_obj.__module__][cls_obj.__name__]['special'][method] = {}
            else:
                _types[cls_obj.__module__][cls_obj.__name__]['methods'][method] = {}


for m in _modules:
    for _, cls_obj in inspect.getmembers(sys.modules[m], inspect.isclass):
        find_base(cls_obj)
    """        
    for _, function in inspect.getmembers(sys.modules[m], inspect.isfunction):
        print(function, get_signature(function))
    for _, function in inspect.getmembers(sys.modules[m], inspect.isbuiltin):
        print(function, get_signature(function))
    """

def test(test_code):
    try:
        result = eval(test_code)
    except Exception as ex:
        print(ex.args)

unknown = 'str'
test_1 = test(unknown + '()')


#print(len(_codons))
with open('test_types.json', 'w') as njsonfile:
    dump(_types, njsonfile, indent=4, sort_keys=True)
#print(pformat(_codons))
