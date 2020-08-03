
Types
=====


+--------------------------------------------------------+
| Genetic Code Type Definition                           | 
+-----------+------------+-------------------------------+
| Bit Field | Identifier | Description                   |
+===========+============+===============================+
| [15]      | RESERVED   | N/A                           |
+-----------+------------+-------------------------------+
| [14:12]   | base_type  | | b’001: Integer              |
|           |            | | b’010: Floating point       |
|           |            | | b’011: Numeric              |
|           |            | | b’100: Object               |
|           |            |                               |
|           |            | All other values RESERVED     |
+-----------+------------+-------------------------------+
| [11:0]    | parameters | See tables below              |
+-----------+------------+-------------------------------+



+------------------------------------------------------------------------+
| Format for base_type == b'001, b'010 or b'011 (Numeric types)          |
+-----------+------------+-----------------------------------------------+
| Bit Field | Identifier | Description                                   |
+===========+============+===============================================+
| [11]      | sign       | | 0: Unsigned.                                |
|           |            | | 1: Signed.                                  |
|           |            |                                               |
|           |            | if bit 13 == 1 then sign == 1.                |
+-----------+------------+-----------------------------------------------+
| [10:8]    | log_size   | log2(Size in bytes).                          |
+-----------+------------+-----------------------------------------------+
| [7:4]     | n_dim      | | Number of dimensions.                       |
|           |            | | 0: scalar.                                  |
|           |            | | 1-15: n_dim-dimensional array.              |
+-----------+------------+-----------------------------------------------+
| [3]       | exact      | | Type log2(size in bytes) is:                |
|           |            | | 0: <= log_size.                             |
|           |            | | 1: == log_size.                             |
+-----------+------------+-----------------------------------------------+
| [2]       | RESERVED   | N/A                                           |
+-----------+------------+-----------------------------------------------+
| [1:0]     | t_idx      | | Template identifier.                        |
|           |            | | 0: No templating.                           |
|           |            | | 1-3: All types with the same t_idx must have|
|           |            | | the exact same 16 bit Genetic Code Type     |
|           |            | | definition. When the genetic code is        |
|           |            | | instantiated all type instances must have   |
|           |            | | exactly the same type.                      |
+-----------+------------+-----------------------------------------------+


+-------------------------------------------------------------------------+
| Format for base_type == b'100 (Objects)                                 |
+-----------+------------+------------------------------------------------+
| Bit Field | Identifier | Description                                    |
+===========+============+================================================+
| [11:2]    | obj_id     | | Object type identifier.                      |
|           |            | | Values 0 to 127 are RESERVED.                |
|           |            | | 28 to 895 are mapped. See obj_id table below.|
|           |            | | 896 to 1023 are user defined.                |
+-----------+------------+------------------------------------------------+
| [1:0]     | t_idx      | | Template identifier.                         |
|           |            | | 0: No templating                             |
|           |            | | 1-3: All types with the same t_idx must have |
|           |            | | the exact same 16 bit Genetic Code Type      |
|           |            | | definition. When the genetic code is         |
|           |            | | instantiated all type instances must have    |
|           |            | | exactly the same type.                       |
+-----------+------------+------------------------------------------------+


