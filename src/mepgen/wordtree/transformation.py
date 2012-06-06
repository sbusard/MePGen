def remove_empty_subtrees(wordtree):
	"""
	Returns a copy of wordtree where all subtrees of wordtree
	that recognize no word are removed.
	Returns None if wordtree recognizes no word.
	"""
	
	def _remove_empty_subtrees(visited, wordtree):
		"""
		Returns empty substrees of wordtree, i.e. subtrees that recognize no
		words.
		wordtree is modified in place.
		wordtree must recognize some words.
		visited is the set of wordtree already emptied
		"""
		
		# FIXME Seems buggy!
		
		succs = {}
		for ranges in wordtree.successors:
			if wordtree.successors[ranges].wordscount > 0:
				if wordtree.successors[ranges] not in visited:
					visited.add(wordtree.successors[ranges])
					succs[ranges] = wordtree.successors[ranges]
					_remove_empty_subtrees(visited, succs[ranges])
		wordtree.successors = succs
		
	
	if wordtree.wordscount == 0:
		return None

	wordtree = wordtree.copy()
	_remove_empty_subtrees(set(), wordtree)
	return wordtree
	