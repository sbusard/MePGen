from random import random

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
		# FIXME Seems buggy!
		
		def _copy(visited, wordtree):
			"""
			Copies the given wordtree by using visited as a dictionary of
			already copied sub-wordtrees.
			"""
			
			if len(wordtree.successors) <= 0:
				wt = Wordtree({}, wordtree.accepting)
				visited[wordtree] = wt
				return wt

			else:
				successors = {}
				for ranges in wordtree.successors:
					wtr = wordtree.successors[ranges]
					if wtr in visited:
						successors[ranges] = visited[wtr]
					else:
						successors[ranges] = _copy(visited, wtr)
				wt = Wordtree(successors, wordtree.accepting)
				visited[wtr] = wt
				return wt
				
		return _copy({}, self)		
			
			
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
	
	
	def randomrun(self):
		"""
		Returns a random accepting run of this tree.
		The result is a random word accepted by this tree.
		This tree must accept at least one word.
		"""
		
		if self.wordscount <= 0:
			print("[ERROR] Cannot produce a randomrun since no word is possible!")
		
		# We have to select a possible next character
		
		if len(self.successors) <= 0:
			return ''
			
		charcount = 0
		bounds = {}
		for ranges in self.successors:
			bounds[(charcount,charcount + len(ranges))] = \
			 	(ranges, self.successors[ranges])
			charcount += len(ranges)
		
		charid = int(random() * charcount)
		for (begin, end) in bounds:
			if begin <= charid and charid < end:
				char = list(bounds[(begin,end)][0])[charid-begin]
				state = bounds[(begin,end)][1]
				return char + state.randomrun()