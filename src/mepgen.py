#! /usr/bin/env python3.2

import argparse
import sys
from mepgen.regex.regex import Concat, Choice, Range, Repeat, Automaton
from mepgen.regex.transformation import regex_to_wordtree
from mepgen.text.text import text_to_automaton
from mepgen.automaton.transformation import (remove_lambdas, determinize,
                                             reject_short_words)


def get_text_from_filename(filename):
    """Return the content of filename"""
    f = open(filename,"r")
    text = f.read()
    f.close()
    return text


# Parse arguments
# mepgen.py -v
#           -s pwdsize (default: 16)
#           -n pwdnumber (default: 10)
#           -t text (default: None)
#           -b threshold (default: 0.0)

parser = argparse.ArgumentParser(description="A memorable passwords generator")

parser.add_argument('-v',dest="verbose",help="verbose mode",action='store_true')

word_group = parser.add_argument_group(title="passwords related arguments")
word_group.add_argument('-s',dest="size",help="size of the generated passwords (default: 16)", default=16,type=int)
word_group.add_argument('-n',dest="count",help="number of generated passwords (default: 10)", default=10,type=int)

text_group = parser.add_argument_group(title="source text related arguments")
text_group.add_argument('-t',dest="text",help="source text (default: None)",default=None,type=get_text_from_filename)
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

# WORD := (vowe | cons)+ if text is not defined
# otherwise, WORD is the set of words, upper and lowercase, from text
if args.text:
    Word = Automaton(reject_short_words(
            text_to_automaton(args.text,
                              lambda x : x.isalpha(),
                              args.threshold),
            args.minlen))
    word = Automaton(reject_short_words(
            text_to_automaton(args.text.lower(),
                              lambda x : x.isalpha(),
                              args.threshold),
            args.minlen))
    WORD = Automaton(reject_short_words(
            text_to_automaton(args.text.upper(),
                              lambda x : x.isalpha(),
                              args.threshold),
            args.minlen))
    fullWord = Choice(Choice(Word, word), WORD)
else:
    fullWord = Concat(Range(Vowe + vowe + Cons + cons),
                      Repeat(Range(Vowe + vowe + Cons + cons)))

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