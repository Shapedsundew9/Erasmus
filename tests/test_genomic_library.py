'''
Filename: /home/shapedsundew9/Projects/Erasmus/tests/test_genomic_library.py
Path: /home/shapedsundew9/Projects/Erasmus/tests
Created Date: Saturday, April 11th 2020, 2:51:52 pm
Author: Shapedsundew9

Copyright (c) 2020 Your Company
'''

import pytest
from psycopg2 import connect
from os.path import isfile
from json import load
from microbiome.genetics.config import set_config
from microbiome.genetics.genomic_library import genomic_library


CODON_LIBRARY_FILE = "./microbiome/genetics/codon_library.json"
test_config = {
    "local_genomic_library": {
        "dbname": "test_library",
        "recreate": True,
        "username": "erasmus",
        "password": "erasmus"
        }
}


# Delete the database after the test
@pytest.fixture(scope="function")
def temp_db():
    config = set_config(test_config)
    c = config['local_genomic_library']
    conn = connect(host=c['host'], port=c['port'], user=c['username'], password=c['password'], dbname='postgres')
    if not conn is None:
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("DROP DATABASE IF EXISTS " + c['dbname'])
        conn.close()
    yield


def test_library_codons(temp_db):
    if not isfile(CODON_LIBRARY_FILE): assert False, "Cannot find {}".format(CODON_LIBRARY_FILE)
    with open(CODON_LIBRARY_FILE, "r") as file_ptr: codon_library = load(file_ptr)
    gl = genomic_library()
    app_codons = [gl.store_gc(codon) for codon in codon_library]
    for app_codon in app_codons: assert app_codon == gl[app_codon['signature']]


