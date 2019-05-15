#!/usr/bin/python

import argparse
import pandas as pd

"""Format call signs and country code data in a list of"""
""" (country_code, call_sign_prefix)."""
""" Usage: process_data <input_file> <output_file>"""

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
result = ['    ("%s", "%s"),  # %s' % (row[0],
                                       row[1]+'-' if row[1].count('-') == 0
                                       else row[1], row[2])
          for row in df[['Alpha-2', 'Registration_Prefix', 'Country']].values]
result.insert(0, "COUNTRIES_PREFIX = (")
result.append(")")

header_message = ("# This file has been generated,"
                  " all changes need to be done in the source file")

if args.output:
    result.insert(0, header_message)
    with open(args.output, "w") as out:
        out.write("\n".join(result))
else:
    print("\n".join(result))
