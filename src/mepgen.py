#! /usr/bin/env python3.2

import argparse
import sys
import pickle
from pickle import UnpicklingError
from mepgen.regex import Concat, Choice, Range, Repeat, AutomatonReg
from mepgen.regex import regex_to_wordtree
from mepgen.text.text import (threshold_matrix, extract_successors,
                              successors_to_automaton)
from mepgen.automaton import (remove_lambdas, determinize, reject_short_words)


# Parse arguments
# mepgen.py -v
#           -s pwdsize (default: 16)
#           -n pwdnumber (default: 10)
#           -t text (default: None)
#           -b threshold (default: 0.0)
#           -l minlen (default: 4)

parser = argparse.ArgumentParser(description="Generate memorable passwords")

parser.add_argument('-v',dest="verbose",help="verbose mode",action='store_true')

word_group = parser.add_argument_group(title="passwords related arguments")
word_group.add_argument('-s',dest="size",help="size of the generated passwords (default: 16)", default=16,type=int)
word_group.add_argument('-n',dest="count",help="number of generated passwords (default: 10)", default=10,type=int)

text_group = parser.add_argument_group(title="source text related arguments")
text_group.add_argument('-t',dest="table",help="successor table (default: None)",default=None)
text_group.add_argument('-b',dest="threshold",help="threshold to keep characters from source file (default: 0.0)",default=0.0,type=float)
text_group.add_argument('-l',dest="minlen",help="minimum length for text generated words (default: 4)",default=4,type=int)

args = parser.parse_args()


# Get the ranges
Vowe = 'AEIOUY'
vowe = 'aeiouy'
Cons = 'BCDFGHJKLMNPQRSTVWXZ'
cons = 'bcdfghjklmnpqrstvwxz'
digi = '0123456789'
punc = '\'"()[]{}.,;:-@&'

# Construct the regex
# PASS := WORD (SEPA WORD)*
# SEPA := digi digi? | punc
# WORD := (vowe | cons)*        if text is not defined

# WORD := (vowe | cons)* if text is not defined
# otherwise, WORD is the set of words, upper and lowercase, from text
fullWord = None
if args.table:
    with open(args.table, 'br') as f:
        try:
            matrix = pickle.load(f)
            matrix = threshold_matrix(matrix, args.threshold)
            aut = successors_to_automaton(extract_successors(matrix))
            fullWord = AutomatonReg(reject_short_words(aut, args.minlen))
        except UnpicklingError:
            print("[WARNING] Cannot load the given table (" + args.table + ") "
                  "Ignoring it.")
if fullWord is None:
    fullWord = Repeat(Range(Vowe + vowe + Cons + cons))

# SEPA := digi digi? | punc
dd = Choice(Range(digi), Concat(Range(digi), Range(digi)))
sepa = Choice(dd, Range(punc))

# PASS := WORD (SEPA WORD)*
sws = Repeat(Concat(sepa, fullWord))
wsws = Concat(fullWord, sws)

regex = wsws


# Get wordtree
if args.verbose:
    print("Constructing the word tree...")
wordtree = regex_to_wordtree(regex, args.size)
if wordtree is None:
    print("There is no possible password generable with the provided arguments... Abort.")
    sys.exit(1)
if args.verbose:
    print("The tree can generate {0} words.".format(str(wordtree.wordscount)))
    print()


# Generate passwords
for i in range(args.count):
    print(wordtree.randomrun())