#!/usr/bin/python

import argparse
import pandas as pd
import re

"""Format call signs and country code data in a list of"""
""" (country_code, call_sign_prefix)."""
""" Usage: process_data <input_file> <output_file>"""


def create_association_enum(df):
    result = ['    ("%s", "%s"),  # %s' % (row[0],
                                           row[1]+'-' if row[1].count('-') == 0
                                           else row[1], row[2])
              for row in df[['Alpha-2', 'Registration_Prefix', 'Country']].values]
    result.insert(0, "COUNTRIES_PREFIX = (")
    result.append(")")
    return '\n'.join(result)


def to_regex(pattern):
    reg = ""
    for c in pattern:
        if c.isalpha():
            if c.isupper():
                reg += c
            else:
                reg += "[A-Za-z]"
        elif c.isnumeric():
            reg += "[0-9]"
    reg += '$'
    return reg


def extract_regex(pattern):
    return [to_regex(x) for x in pattern.split(',')]


def create_master_regex(df):
    return {(row[0]+'-' if row[0].count('-') == 0
             else row[0]): extract_regex(row[1])
            for row in df[['Registration_Prefix', 'Pattern']].values}


def match(dict, call_sign):
    match = []
    for key, patterns in dict.items():
        if call_sign.startswith(key):
            for p in patterns:
                if re.match(key+p, call_sign):
                    match.append(key)

    return set(match)


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input',
                    help="Input csv file containing "
                    "(Country, Registration_Prefix, Alpha-2) column",
                    required=True)
parser.add_argument('-o', '--output',
                    help="output file, if none print the result on console",
                    required=False)
args = parser.parse_args()


df = pd.read_csv(args.input, na_filter=False)

header_message = ("# This file has been generated,"
                  " all changes need to be done in the source file")

enum = create_association_enum(df)

regexes = create_master_regex(df)

if args.output:
    enum = header_message + enum
    with open(args.output, "w") as out:
        out.write(enum)
else:
    print(enum)

# TODO: Use Pickle to serialize result
for i in range(10000):
    print(match(regexes, 'F-OGAA'))
