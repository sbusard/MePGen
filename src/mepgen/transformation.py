from mepgen.regex.transformation import regex_to_automaton
from mepgen.automaton.transformation import remove_lambdas, determinize, automaton_to_wordtree
from mepgen.wordtree.transformation import remove_empty_subtrees

def regex_to_wordtree(regex, depth):
	"""
	Returns the wordtree of depth depth recognizing words of length depth
	recognized by regex.
	"""
	
	# Transform regex to automaton
	automaton = regex_to_automaton(regex)
	# Remove lambdas, determinize automaton
	automaton = remove_lambdas(automaton)
	automaton = determinize(automaton)
	# Get the tree, remove empty subtrees
	wordtree = automaton_to_wordtree(automaton, depth)
	wordtree = remove_empty_subtrees(wordtree)
	return wordtree