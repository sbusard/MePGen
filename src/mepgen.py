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

# Get the ranges
Vowe = 'AEIOUY'
#vowe = 'aeiouyéàèêëù'
vowe = 'aeiouy'
Cons = 'BCDFGHJKLMNPQRSTVWXZ'
cons = 'bcdfghjklmnpqrstvwxz'
digi = '0123456789'
#punc = '@&"\'(§!)-$,;:=<#°_*%£?./+>{}€[]'
punc = '\'"()[]{}.,;:-@&'

extVowe = 'AEIOUYÁÉÍÓÚÀÈÌÒÙÂÊÎÔÛÄËÏÖÜŸÃÕ'
extvowe = 'aeiouyáéíóúàèìòùâêîôûäëïöüÿãõ'
extCons = 'BCDFGHJKLMNPQRSTVWXZÑÇ'
extcons = 'bcdfghjklmnpqrstvwxzñç'
extpunc = '@&"\'(§!)-^$`,;:=<#°_¨*%£?./+>•“‘{¶«¡ø}—€@∞…÷≠≤’”Ÿ´„[å»Ø]¥‰#¿' + \
			'•\±≥æ®†ºœπµ¬ﬁƒ∂‡‹≈©◊ß~ÆÅ‚™ªïŒ∏|ﬂ·∆∑Ω›⁄¢√∫ı'


# Construct the regex
# PASS := WORD (SEPA WORD)*
# SEPA := digi digi? | punc
# WORD := SYLL+
# SYLL := cons? cons vowe


# SYLL := cons? cons vowe
cv = Concat(Range(cons), Range(vowe))
ccv = Concat(Range(cons), cv)
syll = Choice(ccv, cv)

# SYLL := CONS? CONS VOWE
CV = Concat(Range(Cons), Range(Vowe))
CCV = Concat(Range(Cons), CV)
SYLL = Choice(CCV, CV)

# Syll = CONS cons vowe | CONS vowe
Ccv = Concat(Range(Cons), cv)
Cv = Concat(Range(Cons), Range(vowe))
Syll = Choice(Ccv, Cv)


# WORD := SYLL+
word = Concat(syll, Repeat(syll))
Word = Concat(Syll, Repeat(syll))
WORD = Concat(SYLL, Repeat(SYLL))

fullWord = Choice(Choice(word, Word), WORD)


# SEPA = digi | digi digi | punc
sepa = Choice(Choice(Range(digi), Concat(Range(digi), Range(digi))), Range(punc))

# PASS = WORD (SEPA WORD)*
regex = Concat(fullWord, Repeat(Concat(sepa, fullWord)))


# Get wordtree
print("Constructing the word tree...")
wordtree = regex_to_wordtree(regex, args.size)
print("The tree can generate " + str(wordtree.wordscount) + " words.")
print()

# Generate passwords
for i in range(args.count):
	print(wordtree.randomrun())