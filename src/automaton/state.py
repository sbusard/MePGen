class State:
	"""
	A State represents a state of an automaton.
	
	It has a list of successors. Every successor is	reachable through a
	transition labelled with a character. There is no duplicated transitions,
	i.e. there is at most one couple <char,succ> for each character char and
	successor succ in the transition relation.
	
	The transition relation is represented by a dictionary where the keys
	are the characters and the elements are sets of successor states. Only one
	copy of each state is stored such that adding twice the same state has no
	effect.
    
	Simon Busard <simon.busard@gmail.com>
	30 - 05 - 2012
	"""
	
	# TODO Define lambda character
	
	def __init__(self, successors = {}):
		self.successors = successors
		
	def add_successor(self, char, succ):
		"""
		Adds succ as a successor for this state, reachable through the character 
		char. If succ is already reachable through char, nothing changes.
		"""
		if char not in self.successors:
			self.successors[char] = set([succ])
		else:
			self.successors[char].add(succ)
			
	def remove_successor(self, char, succ):
		"""
		Removes succ from successors of this state through the character char.
		If succ is not reachable through char from this state, does nothing.
		"""
		if succ in self.successors[char]:
			self.successors[char].remove(succ)
			
	def __str__(self):
		# TODO