from mepgen.text.text import *
from mepgen.automaton.transformation import automaton_to_wordtree, remove_lambdas, determinize, reject_short_words
from mepgen.wordtree.transformation import remove_empty_subtrees
from mepgen.regex.regex import *
from mepgen.regex.transformation import regex_to_automaton, regex_to_wordtree
    

f = open("lovecraft.txt", "r")
text = f.read()
f.close()

digi = '0123456789'
punc = '\'"()[]{}.,;:-@&'

alphafilter = lambda x : x.isalpha()
threshold = 0.05
minwordlen = 4

text = text.lower()
words = reject_short_words(
            remove_lambdas(
                text_to_automaton(text, alphafilter, threshold)
            ),
            minwordlen
        )
text = text.upper()
WORDS = reject_short_words(
            remove_lambdas(
                text_to_automaton(text, alphafilter, threshold)
            ),
            minwordlen
        )


allWords = Choice(Automaton(words), Automaton(WORDS))
sep = Choice(Range(punc), Choice(Range(digi), Concat(Range(digi), Range(digi))))
regex = Concat(allWords, Repeat(Concat(sep, allWords)))
wordtree = regex_to_wordtree(regex, 16)

print("wordtree can produce " + str(wordtree.wordscount) + " words.")
alph = list(wordtree.get_alphabet())
alph.sort()
print(alph)

for i in range(10):
    print(wordtree.randomrun())