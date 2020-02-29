..
.. Filename: /home/shapedsundew9/Projects/Erasmus/docs/genomic_library.rst
.. Path: /home/shapedsundew9/Projects/Erasmus/docs
.. Created Date: Saturday, February 29th 2020, 4:43:34 pm
.. sectionauthor:: Shapedsundew9
.. 
.. Copyright (c) 2020 Your Company
..
***************
Genomic Library
***************

.. csv-table:: Genomic Library Table Description
   :header: "Field", "Type", "Restrictions", "Description"
   :widths: 20, 15, 20, 50

    "graph","VARCHAR (1024)","NOT NULL","The definition of the code as a graph of other codes see `Graph Field Format`_"
    "signature","CHAR (32)","PRIMARY KEY","A `SHA256 <https://en.wikipedia.org/wiki/SHA-2>`_ of the graph field. The signature of a code is assumed to be unique in the codosphere.`
    "generation","BIGINT","NOT NULL","The number of generations of genetic code evolved to create this code. A codon is generation always generation 1." 
    "references","BIGINT","NOT NULL","The number of times this code is referenced in other codes. If this code is referenced by code A once and no other then the reference count is 1. If code A is then referenced by code B this code is referenced by both A & B (through A) and the count is 2." 
    "multi_ancestor","BOOL","NOT NULL","True if this code has more than two parents. This is possible through chance as well as unconventional breeding. Details are stored in the meta_data field."
    "code_depth","INTEGER","NOT NULL","The depth of the code vertex graph."
    "codon_depth","INTEGER","NOT NULL","The depth of the graph after expansion to codon vertices."  
    "num_codes","INTEGER","NOT NULL","The number of vertices in the code vertex graph."
    "num_uniquie_codes","INTEGER","NOT NULL","The number of unique codes in the code vertex graph."
    "raw_num_codons","INTEGER","NOT NULL","The number of verticies in the codon vertex graph."
    "opt_num_codons","INTEGER",,"The number of verticies in the codon vertex graph after optimisation."
    "num_inputs","INTEGER","NOT NULL","The number of inputs to the code."
    "num_outputs","INTEGER","NOT NULL","The number of outputs from the code."
    "parent_x","CHAR (32)","NOT NULL","The signature field (i.e. a `SHA256 <https://en.wikipedia.org/wiki/SHA-2>`_) of the parent_x code. In the event a code has more than one parent parent_x is the oldest generation parent i.e. parent_x's generation field has the lowest value of all parents. In the event of a tie parent_x is randomly selected. Codon's parent_x are all 0's."
    "parent_y","CHAR (32)",,"The signature field (i.e. a SHA256) of the parent_y code. parent_y is the next oldest generation parent after parent_x in the event of a code having more than 2 parents. Additional parents are stored in the meta_data field."
    "classification","BIGINT","NOT NULL","A binary encoded classification. See `Classification Field Format`_."
    "creator","CHAR (32)","NOT NULL","A `SHA256 <https://en.wikipedia.org/wiki/SHA-2>`_ hash identifying the creator." 
    "created","TIMESTAMP","NOT NULL","The date and time of the codes creation."
    "meta_data","VARCHAR (512)",,"Other data associated with this code. See `Meta_data Field Format`_"


Graph Field Format
******************


Classification Field Format
***************************


Meta_data Field Format
**********************
The meta_data field is a base 64 encoded `python base64.b64encode(data) <https://docs.python.org/3/library/base64.html>`_  gzip compatible 
`python zlib.compress(data, level=9) <https://docs.python.org/3/library/zlib.html>_` compressed JSON object. This keeps the size down at the cost of transparency.
The JSON object is a dictionary which may contain any key:value pairs. However, some keys are reserved:

.. csv-table:: Reserved meta_data keys
   :header: "Key", "Description"
   :widths: 20, 50

   "classification","Reserved for additional classifications."
   "parents","List of parent signatures for the 3rd parent 


