from mepgen.regex.regex import Range, Repeat, Choice, Concat, Automaton
from mepgen.regex.transformation import regex_to_automaton
from mepgen.automaton.transformation import remove_lambdas, determinize

regex = Repeat(Choice(Range(frozenset(['a'])), Range(frozenset(['b']))))
aut = regex_to_automaton(regex)
print("aut is deterministic :", aut.is_deterministic())

tests = ['','a','b','c','aa','ba','ca','aaa','aba','aab','abc']
for test in tests:
	print("aut accepts '" + test + "' :", str(aut.accepts(test)))
	
aut = remove_lambdas(aut)
print("aut is deterministic :", aut.is_deterministic())

tests = ['','a','b','c','aa','ba','ca','aaa','aba','aab','abc']
for test in tests:
	print("aut accepts '" + test + "' :", str(aut.accepts(test)))
	
aut = determinize(aut)
print("aut is deterministic :", aut.is_deterministic())

tests = ['','a','b','c','aa','ba','ca','aaa','aba','aab','abc']
for test in tests:
	print("aut accepts '" + test + "' :", str(aut.accepts(test)))
