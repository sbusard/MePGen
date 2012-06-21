#! /usr/bin/env python3.2

import argparse
from mepgen.regex.regex import Concat, Choice, Range, Repeat
from mepgen.transformation import regex_to_wordtree

# Parse arguments
# mepgen.py -s pwdsize (default: 16) -n pwdnumber (default: 10)

parser = argparse.ArgumentParser(description="A memorable passwords generator")
parser.add_argument('-s',dest="size",help="size of the generated passwords (default: 16)", default=16,type=int)
parser.add_argument('-n',dest="count",help="number of generated passwords (default: 10)", default=10,type=int)

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
# PASS := SEPA? WORD (SEPA WORD)* SEPA?
# SEPA := punc? digi digi? punc? | punc
# WORD := SYLL SYLL+
# SYLL := GCON GVOW
# GVOW := vowe [hmn]? | vowe vowe
# GCON := /* generated from gconbase */

gconbase = {
    'b': 'fhjlmnprsvwz',
    'c': 'cfhklmnrsvwxz',
    'd': 'dhjlmnrstwz',
    'f': 'fhlmnrvw',
    'g': 'fghlmnrstwz',
    'h': 'bcdfghjklmnpqrstvwxz',
    'j': 'fghjlmnrtvw',
    'k': 'cfhklmnrsvwxz',
    'l': 'bcdfghjklmnpqrstvwxz',
    'm': 'bcdfghjklmnpqrstvwxz',
    'n': 'bcdfghjklmnpqrstvwxz',
    'p': 'fhjlmnprsvwz',
    'q': 'cfhklmnrsvwxz',
    'r': 'bcdfghjklmnpqrstvwxz',
    's': 'cfghklmnpqrsvwz',
    't': 'dhjlmnrstwz',
    'v': 'fhlmnrvw',
    'w': 'hw',
    'x': 'hsxz',
    'z': 'cfghklmnpqrsvwz'
}

def generate_regex_from_dict(chardict):
    """
    Generates the regex corresponding to the association in chardict.
    chardict is a dictionary where keys are single characters and values are
    characters ranges.
    """
    
    def _generate_choice_regex_from_list(reglist):
        """
        Generates a regex made of choices, corresponding to the choices to
        take one regex of reglist.
        reglist is a list of regex, and every element is uniquely present in it.
        reglist is not empty.
        """
        
        if len(reglist) == 1:
            return reglist[0]
            
        else:
            left = reglist[:int(len(reglist) / 2)]
            right = reglist[int(len(reglist) / 2):]
            lreg = _generate_choice_regex_from_list(left)
            rreg = _generate_choice_regex_from_list(right)
            return Choice(lreg, rreg)
    
    conslist = []
    for char in chardict:
        ranges = [Range(c) for c in chardict[char]]
        choices = _generate_choice_regex_from_list(ranges)
        conslist.append(Choice(Range(char), Concat(Range(char), choices)))
        
    return _generate_choice_regex_from_list(conslist)
    
    
gcon = generate_regex_from_dict(gconbase)
        

# gvow := vowe [hmnw]? | vowe vowe
gvow = Choice(
            Choice(
                Concat(
                    Range(vowe),
                    Range('hmnw')
                ),
                Range(vowe)
            ),
            Concat(
                Range(vowe),
                Range(vowe)
            )
        )

#syll = Concat(Range(cons), Range(vowe))
#SYLL = Concat(Range(Cons), Range(Vowe))
#Syll = Concat(Range(Cons), Range(vowe))

syll = Concat(gcon, gvow)


# WORD := SYLL SYLL+
#word = Concat(syll, Concat(syll, Repeat(syll)))
#Word = Concat(Syll, Concat(syll, Repeat(syll)))
#WORD = Concat(SYLL, Concat(SYLL, Repeat(SYLL)))

#fullWord = Choice(Choice(word, Word), WORD)

fullWord = Concat(syll, Choice(syll, Concat(syll, Repeat(syll))))


# SEPA := punc? digi digi? punc? | punc
dd = Concat(Range(digi), Range(digi))
dde = Choice(Range(digi), dd)
pedde = Choice(dde, Concat(Range(punc), dde))
peddepe = Choice(pedde, Concat(pedde, Range(punc)))
sepa = Choice(peddepe, Range(punc))

# PASS := SEPA? WORD (SEPA WORD)* SEPA?
sws = Repeat(Concat(sepa, fullWord))
wsws = Concat(fullWord, sws)
sewsws = Choice(Concat(sepa, wsws), wsws)
sewswsse = Choice(sewsws, Concat(sewsws, sepa))

regex = sewswsse


# Get wordtree
print("Constructing the word tree...")
wordtree = regex_to_wordtree(regex, args.size)
print("The tree can generate " + str(wordtree.wordscount) + " words.")
print()

# Generate passwords
for i in range(args.count):
    print(wordtree.randomrun())