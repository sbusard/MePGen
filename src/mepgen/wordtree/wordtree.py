class Wordtree:
	"""
	A Wordtree is a tree recognizing a word.
	It is a state with a set of successors, reachable through a range of
	characters. Furthermore, a Wordtree may be accepting, and is also labeled
	with the number of different words it can recognize.
    
	Simon Busard <simon.busard@gmail.com>
	04 - 06 - 2012
	"""
	
	def __init__(self, successors, accepting = False):
		"""
		Creates a new Wordtree.
		
		successors is a dictonary with frozensets of characters as keys
		and Wordtrees as values. successors[{c1,c2,...,cn}] = wt means that
		wt is reachable from this Wordtree through characters c1 to cn.
		
		For the tree words count to be correct,
		the set of keys must be disjoint, meaning that
		no character is in two different sets. This is not verified.
		"""
		self.successors = successors
		self.accepting = accepting
		self.wordscount = accepting and 1 or 0
		for ranges in successors:
			self.wordscount += len(ranges) * successors[ranges].wordscount
		
			
	def __str__(self):
		pass # TODO
		
		
	def copy(self):
		if len(successors) <= 0:
			return Wordtree({}, self.accepting)
		
		else:
			successors = {}
			for ranges in self.successors:
				successors[ranges] = self.successors[ranges].copy()
			return Wordtree(successors, self.accepting)
			
			
	def accepts(self, word):
		"""
		Returns whether the given word is accepted by this wordtree.
		
		A word is accepted iff there is a run this tree that accepts the word.
		A run accepts the word if it ends in an accepting state.
		"""
		
		if word == '':
			return self.accepting
			
		else:
			for ranges in self.successors:
				if word[0] in ranges:
					if self.successors[ranges].accepts(word[1:]):
						return True
						
		return False
					