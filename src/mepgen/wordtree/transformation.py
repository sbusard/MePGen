def automaton_to_wordtree(automaton):
	pass # TODO
	

def remove_empty_subtrees(wordtree):
	"""
	Returns a copy of wordtree where all subtrees of wordtree
	that recognize no word are removed.
	Returns None if wordtree recognizes no word.
	"""
	
	def _remove_empty_subtrees(wordtree):
		"""
		Returns empty substrees of wordtree, i.e. subtrees that recognize no
		words.
		wordtree is modified in place.
		wordtree must recognize some words.
		"""
		
		for ranges in wordtree.successors:
			if wordtree.successors[ranges].wordscount == 0:
				del wordtree.successors[ranges]
			else:
				_remove_empty_subtrees(wordtree.successors[ranges])
		
	
	if wordree.wordscount == 0:
		return None
		
	wordtree = wordtree.copy()
	_remove_empty_subtrees(wordtree)
	