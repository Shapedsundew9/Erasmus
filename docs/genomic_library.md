# Genomic Library

The genomic library has a layered access model for the best performance.

There are two views of the genomic library data. The storage format as persisted in the database and the application format as viewed through the genomic library API.

## Storage Format

The storage format of the genomic library tries to reduce the space requirements whilst maintaining the ability to do all but corner case queries quickly.
Typically complex fields are stored compressed as byte strings. Below is the definition of a genetic code entry in the genomic library database table.

Field | Type | Restrictions | Description
----- | ---- | ------------ | -----------
graph | BYTEA | NOT NULL IMMUTABLE | The definition of the code as a graph of other codes as a binary compressed array. See [Graph Field Format](###-graph-field-format).
signature | BYTEA | PRIMARY KEY IMMUTABLE | A binary [SHA256](https://en.wikipedia.org/wiki/SHA-2) of the graph field. The signature of a code is assumed to be unique in the codosphere.
generation | BIGINT | NOT NULL | The number of generations of genetic code evolved to create this code. A codon is generation always generation 1.
references | BIGINT | NOT NULL | The number of times this code is referenced in other codes. If this code is referenced by code A once and no other then the reference count is 1. If code A is then referenced by code B this code is referenced by both A & B (through A) and the count is 2.
code_depth | INTEGER | NOT NULL IMMUTABLE | The depth of the code vertex graph.
codon_depth | INTEGER | NOT NULL IMMUTABLE | The depth of the graph after expansion to codon vertices.  
num_codes | INTEGER | NOT NULL IMMUTABLE | The number of vertices in the code vertex graph.
num_unique_codes | INTEGER | NOT NULL IMMUTABLE | The number of unique codes in the code vertex graph.
raw_num_codons | INTEGER | NOT NULL IMMUTABLE | The number of verticies in the codon vertex graph.
opt_num_codons | INTEGER |  | The number of verticies in the codon vertex graph after optimisation.
num_inputs | INTEGER | NOT NULL IMMUTABLE | The number of inputs to the code. I0 in the [Graph Field Format](###-graph-field-format).
num_outputs | INTEGER | NOT NULL IMMUTABLE | The number of outputs from the code. IN in the [Graph Field Format](###-graph-field-format).
classification | BIGINT | NOT NULL | A binary encoded classification. See [Classification Field Format](###-classification-field-format)
creator | BYTEA | NOT NULL IMMUTABLE | A binary [SHA256](https://en.wikipedia.org/wiki/SHA-2) hash identifying the creator. 
created | TIMESTAMP | NOT NULL IMMUTABLE | The date and time of the codes creation."
meta_data | BYTEA | NOT NULL | Other data associated with this code as a binary compressed JSON. See [Meta_Data Field Format](###-meta_data-field-format)

### Graph Field Format

The *graph* field is a binary gzip compatible [python zlib.compress(data, level=9)](https://docs.python.org/3/library/zlib.html) compressed
[python unsigned integer array](https://docs.python.org/3/library/array.html). This keeps the size down at the cost of transparency. Integer size
is validated to be 4 bytes. Where *M* is the value of the *num_outputs* field the structure of the array is as follows:

Index range (inclusive) | Variable | Description
----------------------- | -------- | -----------
0 | N | Number of entries in the genetic code numbered 0 to N inclusive where 0 is the input entry and N is the output entry.
1 | I1 | Number of inputs to entry 1.
2:I1+1 |  | Input references to entry 1 (implicitly to entry 0, the genetic code input)
I1+2:I1+9 |  | Signature of genetic code in entry 1.
I1+10 | I2 | Number of inputs to entry 2.
I1+11:I1+10+2*I2 |  | Input references for entry 2.
I1+11+2*I2:I1+18+2*I2 |  | Signature of genetic code in entry 2.
I1+19+2*I2 | I3 | Number of inputs to entry 3.
I1+20+2*I2:I1+19+2*(I2+I3) |  | Input references for entry 3.
I1+20+2*(I2+I3):I1+27+2*(I2+I3) |  | Signature of genetic code in entry 3.
... |  | Repeat pattern for entry 3 up to but not including entry N, the output entry. Signature of entry N-1 ends at and includes index L-1.
L:L+M*2-1 |  | Input references for entry N, the output entry.

### Classification Field Format

The *classification* field defines the classes that the genetic code is a member of. A genetic code may be a member of many classes although
some classes are mutally exclusive. The class definitions are stored as a bitfield.

Bit range (inclusive) | Description
--------------------- | -----------
[0] | Classification is extended by the *extended_class* dictionary in the *meta_data* field.
[1] | 1 if the genetic code is a codon else 0.
[2:63] | Reserved. See [Glossary](Glossary.md) 

:warning: Classification & its utility are largely TBD at this stage.

### Meta_Data Field Format

The *meta_data* field is a base 64 encoded [python base64.b64encode(data)](https://docs.python.org/3/library/base64.html) gzip compatible 
[python zlib.compress(data, level=9)](https://docs.python.org/3/library/zlib.html) compressed JSON object. This keeps the size down at the cost of transparency.
The JSON object is a dictionary which may contain any key:value pairs. Any key defined below may not be reappropriated for a different purpose and
all string keys starting with an underscore '_' are reserved:

Key | Description
--- | -----------
extended_classification | A dictionary for additional classifications of the genetic code.
parents | A list of lists of parent signatures. See [Parents Key Value](####-parents-key-value).

#### Parents Key Value

The value of the *parents* key is a list of lists. Each sub-list consists of the *signatures* of the set of breeding parents
in the order oldest generation (lowest generation value) first. The sub-lists are independent lists of parents. Parents are
independent when they bear an offspring with the same signature as the offspring of a different set of parents i.e. by
chance (or evolutionary pressures) that a genetically the same offspring has been created. A genetic code always has at least
one parent unless is is a codon. Signatures are stored as hexadecimal strings.

## Application Format

In the application format the compression and complex data structure of the storage format is abstracted. 