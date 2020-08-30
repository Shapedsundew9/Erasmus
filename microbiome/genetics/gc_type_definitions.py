"""Definition of gc_types.

All types must be representable as an executable string. e.g.

"123" is an integer (could be one of many specific types)
"{'signature': '0123456701234567012345670123456701234567012345670123456701234567'}" is an obj8, obj9 or obj10
"float32(7)" is a float32 

All gc_types must be valid classes.
"""

from numpy import int8, int16, int32, int64
from numpy import uint8, uint16, uint32, uint64
from numpy import float32, float64


class uint(int): pass
class int1024(int): pass
class float1024(float): pass


class obj128(str): pass
class obj129(int): pass


