from mepgen.automaton.transformation import reject_short_words, remove_lambdas
from mepgen.regex.regex import *
from mepgen.regex.transformation import regex_to_automaton

reg = Repeat(Range('a'))
aut = regex_to_automaton(reg)

tests = ['', 'a', 'b', 'aa', 'ab', 'ba', 'aaa', 'aaaa', 'aaaaa']
for test in tests:
	print("aut '{0}' : {1}".format(test, aut.accepts(test) and "accepting" or "not accepting"))
	
autrlw = reject_short_words(remove_lambdas(aut), 4)
for test in tests:
	print("autrlw '{0}' : {1}".format(test, autrlw.accepts(test) and "accepting" or "not accepting"))