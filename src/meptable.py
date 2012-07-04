#! /usr/bin/env python3.2

import argparse
import pickle

from mepgen.text.text import text_to_matrix, threshold_matrix

def get_text_from_filename(filename):
    """Return the content of filename"""
    f = open(filename,"r")
    text = f.read()
    f.close()
    return text

# arguments:
#   -h, -v
#   -b  threshold (default: 0.0)

# Parse arguments
parser = argparse.ArgumentParser(description="Generate successor tables "
                                             "from texts")
parser.add_argument('source',help="source text",metavar='SOURCE')
parser.add_argument('dest',help="destination file",metavar='DEST')
parser.add_argument('-v',dest="verbose",help="verbose mode",action='store_true')
parser.add_argument('-b',dest="threshold",help="threshold to keep characters from source file (default: 0.0)",default=0.0,type=float)

args = parser.parse_args()

# Get the text
if args.verbose:
    print("Reading the source text (" + args.source + ")...")
text = get_text_from_filename(args.source)

# Create the table
if args.verbose:
    print("Creating the table...")
charfilter = lambda x: x.isalpha()
matrix = text_to_matrix(text, charfilter)
matrix = threshold_matrix(matrix, args.threshold)

# Store the table
with open(args.dest, 'bw') as dest:
    if args.verbose:
        print("Storing the table in destination file (" + args.dest +")...")
    pickle.dump(matrix, dest)