from mepgen.text.text import *
from mepgen.automaton.transformation import automaton_to_wordtree, remove_lambdas, determinize
from mepgen.wordtree.transformation import remove_empty_subtrees
from mepgen.regex.regex import *
from mepgen.regex.transformation import regex_to_automaton, regex_to_wordtree
	

f = open("lovecraft.txt", "r")
text = f.read()
f.close()

Vowe = 'AEIOUY'
vowe = 'aeiouyéàèêëù'
#vowe = 'aeiouy'
Cons = 'BCDFGHJKLMNPQRSTVWXZ'
cons = 'bcdfghjklmnpqrstvwxz'
digi = '0123456789'
#punc = '@&"\'(§!)-$,;:=<#°_*%£?./+>{}€[]'
punc = '\'"()[]{}.,;:-@&'

text = text.lower()
a1 = text_to_automaton(text, lambda x : x.isalpha(), 0)

text = text.upper()
a2 = text_to_automaton(text, lambda x : x.isalpha(), 0)

regex = Choice(Automaton(a1), Automaton(a2))
wt3 = regex_to_wordtree(regex, 16)

text = text.lower() + text.upper()
a4 = determinize(
		remove_lambdas(
			text_to_automaton(text, lambda x : x.isalpha(), 0)
		)
	)
wt4 = automaton_to_wordtree(a4, 16)

words = ['hello', 'this', 'can', 'world', '']
for word in words:
	print("a1 accepts '" + word + "' : " + str(a1.accepts(word)))
	
reg = Repeat(Concat(Automaton(a1), Concat(Range(digi), Range(digi))))
aut = regex_to_automaton(reg)
aut = determinize(remove_lambdas(aut))
	
wt = remove_empty_subtrees(automaton_to_wordtree(aut, 16))
print("wt can produce " + str(wt.wordscount) + " words.")

wt2 = automaton_to_wordtree(a1, 16)
print("wt2 can produce " + str(wt2.wordscount) + " words.")

print("wt3 can produce " + str(wt3.wordscount) + " words.")
print("wt4 can produce " + str(wt4.wordscount) + " words.")

for i in range(10):
	print(wt4.randomrun())