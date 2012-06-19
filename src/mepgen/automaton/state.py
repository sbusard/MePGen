# Lambda character
LAMBDA = '<lambda>'

class State:
	"""
	A State represents a state of an automaton.
	
	It has a list of successors. Every successor is	reachable through a
	transition labelled with a character.
	
	The transition relation is represented by a dictionary where the keys
	are the characters ranges and the elements are sets of successor states.
	Only one copy of each state is stored such that adding twice the same state
	has no effect.
    
	Simon Busard <simon.busard@gmail.com>
	30 - 05 - 2012
	"""
	
	def __init__(self, successors = None):
		self.successors = successors or {}
		
	def add_successor(self, ran, succ):
		"""
		Adds succ as a successor for this state, reachable through
		the characters or range ran. ran is a list of string, each string
		being considered as a character.
		If succ is already reachable through this range, nothing changes.
		"""
		if ran not in self.successors:
			self.successors[ran] = set([succ])
		else:
			self.successors[ran].add(succ)
			
	def remove_successor(self, char, succ):
		"""
		Removes succ from successors of this state through the character char.
		If succ is not reachable through char from this state, does nothing.
		"""
		for ran in [r for r in self.successors if char in ran]:
			self.successors[ran].remove(succ)
			
	def __str__(self):
		rep = "state(" + str(self.successors) + ")"
		return rep
		
			
	def get_possible_chars(self):
		"""
		Returns the set of characters for which there is successor
		in this state.
		"""
		return {char for ran in self.successors for char in ran}
		
		
	def get_successors(self):
		"""
		Returns the set of successors of this state.
		"""
		return {s for ran in self.successors for s in self.successors[ran]}
		
	
	def get_successors_by_char(self, char):
		"""
		Returns the set of states reachable from this state
		through a transition labeled by char.
		"""
		
		return {s 	for ran in self.successors
					if char in ran
					for s in self.successors[ran]}