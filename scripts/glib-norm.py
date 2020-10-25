"""Normalise a genomic library entry JSON data file."""
#!/usr/bin/env python3

from json import load, dump
from sys import exit
from os import access, R_OK
from os.path import isfile
from argparse import ArgumentParser
from microbiome.genetics.genomic_library_entry_validator import genomic_library_entry_validator


parser = ArgumentParser(description='Normalize a JSON file of genomic library entries.')
parser.add_argument('-f', '--filename', type=str, help='full path of the entry JSON file.')
args = parser.parse_args()

if not isfile(args.filename):
    print("ERROR: Cannot find {}.".format(filename))
elif not access(args.filename, R_OK):
    print("ERROR: Cannot access {}.".format(filename))
else:
    try:
        with open(args.filename, 'r') as jsonfile:
            data = load(jsonfile)
    except Exception as e:
        print("ERROR: Unable to read JSON file {} with error {}.".format(args.filename, str(e)))
    else:
        nentries = []
        while data: nentries.append(genomic_library_entry_validator.normalized(data.pop()))
        try:
            with open(args.filename + ".norm", "w") as njsonfile:
                dump(nentries, njsonfile, indent=4, sort_keys=True)
        except Exception as e:
            print("ERROR: Unable to write JSON output file {} with error {}.".format(njsonfile, str(e)))


