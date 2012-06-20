from mepgen.regex.regex import *
from mepgen.regex.transformation import regex_to_automaton
from mepgen.automaton.transformation import remove_lambdas, determinize, automaton_to_wordtree
from mepgen.wordtree.transformation import remove_empty_subtrees
	
	
# Checking determinism
reg = Concat(Range('a'),Repeat(Choice(Range('bd'),Range('c'))))
print("reg : " + str(reg))
aut = regex_to_automaton(reg)
print('aut is deterministic : ' + str(aut.is_deterministic()))	

reg2 = Repeat(Concat(Range('a'),Range('b')))
print("reg2 : " + str(reg2))
aut2 = regex_to_automaton(reg2)
print('aut2 is deterministic : ' + str(aut2.is_deterministic()))

reg3 = Repeat(Choice(Range('a'),Range('b')))
print("reg3 : " + str(reg3))
aut3 = regex_to_automaton(reg3)
print('aut3 is deterministic : ' + str(aut3.is_deterministic()))

reg4 = Repeat(Range('a'))
print("reg4 : " + str(reg4))
aut4 = regex_to_automaton(reg4)
print('aut4 is deterministic : ' + str(aut4.is_deterministic()))


# Checking acceptance
tests = [	'ab',
			'ac',
			'a',
			'abcbc',
			'accccc',
			'abcc',
			'cb',
			'cac',
			'acca',
			'abcbbcac',
			'abcd',
			'abce',
			'ebbbb',
			''	]
			
for test in tests:
	print('aut accepts \'' + test + '\' : ' + str(aut.accepts(test)))
	
# Check copy
autcopy = aut.copy()		
for test in tests:
	print('autcopy accepts \'' + test + '\' : ' + str(autcopy.accepts(test)))

autcopy = remove_lambdas(autcopy)
for test in tests:
	print('autcopy without lambdas accepts \'' + test + '\' : ' + str(autcopy.accepts(test)))
	
a1 = remove_lambdas(regex_to_automaton(Range('a')))
print("a1 accepts 'a' : " + str(a1.accepts('a')))
print("a1 accepts 'aa' : " + str(a1.accepts('aa')))
print("a1 accepts 'b' : " + str(a1.accepts('b')))
print("a1 accepts '' : " + str(a1.accepts('')))

a2 = remove_lambdas(regex_to_automaton(Concat(Range('a'),Range('b'))))
print("a2 accepts 'ab' : " + str(a2.accepts('ab')))
print("a2 accepts 'a' : " + str(a2.accepts('a')))
print("a2 accepts 'aa' : " + str(a2.accepts('aa')))
print("a2 accepts 'b' : " + str(a2.accepts('b')))
print("a2 accepts '' : " + str(a2.accepts('')))

autdet = determinize(autcopy)
for test in tests:
	print('autdet accepts \'' + test + '\' : ' + str(autdet.accepts(test)))
print('autdet is deterministic : ' + str(autdet.is_deterministic()))


testswt = [	'a',	'b',
			'ab', 	'aa',
			'abd',	'aba',	'aad',
			'abcd',
			'abdcc',
			'abdcdd',
			'acddddc'	]
for i in range(8):
	wt = remove_empty_subtrees(automaton_to_wordtree(autdet, i))
	if wt == None:
		print("wt(" + str(i) + ") accepts no word")
	else:
		print("autdet to wt(" + str(i) + ") : " + str(wt.wordscount) + " words accepted")
		for	test in testswt:
			print('wt(' + str(i) + ') accepts \'' + test + '\' : ' + str(wt.accepts(test)))
			

length = 8
wt = remove_empty_subtrees(automaton_to_wordtree(autdet, length))
for i in range(8):
	print("random run of wt(" + str(length) + ") : " + wt.randomrun())

# reg : ([a] . (([bd] | [c]))*)
# aut is deterministic : False
# reg2 : (([a] . [b]))*
# aut2 is deterministic : True
# reg3 : (([a] | [b]))*
# aut3 is deterministic : False
# reg4 : ([a])*
# aut4 is deterministic : True
# aut accepts 'ab' : True
# aut accepts 'ac' : True
# aut accepts 'a' : True
# aut accepts 'abcbc' : True
# aut accepts 'accccc' : True
# aut accepts 'abcc' : True
# aut accepts 'cb' : False
# aut accepts 'cac' : False
# aut accepts 'acca' : False
# aut accepts 'abcbbcac' : False
# aut accepts 'abcd' : True
# aut accepts 'abce' : False
# aut accepts 'ebbbb' : False
# aut accepts '' : False
