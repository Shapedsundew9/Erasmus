from os.path import isfile
from json import load
from microbiome.genetics.entry_validator import entry_validator


CODON_LIBRARY_FILE = "./microbiome/genetics/codon_library.json"


def test_codon_library():
    if not isfile(CODON_LIBRARY_FILE): assert False, "Cannot find {}".format(CODON_LIBRARY_FILE)
    with open(CODON_LIBRARY_FILE, "r") as file_ptr: codon_library = load(file_ptr)
    validator = entry_validator()
    for codon in codon_library: assert validator(codon), codon["meta_data"]["name"] + ":" + str(validator.errors)

        