#! /usr/bin/env python3.2

import argparse
from mepgen.regex.regex import Concat, Choice, Range, Repeat
from mepgen.transformation import regex_to_wordtree

# Parse arguments
# mepgen.py -s pwdsize (default: 16) -n pwdnumber (default: 10)

parser = argparse.ArgumentParser(description="A memorable passwords generator")
parser.add_argument('-s',dest="size",help="size of the generated passwords", default=16,type=int)
parser.add_argument('-n',dest="count",help="number of generated passwords", default=10,type=int)

args = parser.parse_args()

# Construct the regex
regex = Repeat(Concat(Range('a'),Repeat(Choice(Range('bd'),Range('c')))))

# Get wordtree
wordtree = regex_to_wordtree(regex, args.size)

# Generate passwords
for i in range(args.count):
	print(wordtree.randomrun())