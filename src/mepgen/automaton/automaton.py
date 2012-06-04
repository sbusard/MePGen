from .state import LAMBDA, State

class Automaton:
	"""
	An Automaton represents an automaton. It is composed of states and a
	transition relation over an alphabet. Furthermore, a state is
	the initial one and a subset of the states are the accepting ones.
	
	An Automaton stores the initial state and the set of accepting states.
	
	Simon Busard <simon.busard@gmail.com>
	30 - 05 - 2012
	"""
	
	def __init__(self, initial, accepting = None):
		self.initial = initial
		self.accepting = accepting or set()
		
		
	def __str__(self):
		pass # TODO
		
		
	def accepts(self, word):
		"""
		Returns whether the word is accepted by this automaton.
		Since this automaton is potentially non-deterministic and non-minimal,
		it accepts word iff there is a run that accepts word.
		"""
		
		def _accepts(word, start, lambdas):
			"""
			Recursive run of this automaton from the state start, for word.
			lambdas is the set of states already visited when traversing
			a LAMBDA transition.
			"""

			# To check whether this automaton accepts word from start,
			# the word is accepted if
			#	- the word is empty and start is accepting, or
			#	- the word is emtpy and accepted by any state reachable
			#		through a lambda transition that is not in lambdas, or
			#	- the word without its first character is accepted 
			#		by a state reachable through a transition labeled
			#		with its first character, or
			#	- the word is accepted by a state reachable through a lambda
			#		transition that is not in lambdas.
			# the word is not accepted otherwise

			if word == '':
				if start in self.accepting:
					return True
			else:
				if word[0] in start.successors:
					for s in start.successors[word[0]]:
						if _accepts(word[1:], s, []):
							return True
			if LAMBDA in start.successors:
				for s in [x for x in start.successors[LAMBDA] \
							if x not in lambdas]:
					if _accepts(word, s, lambdas + [start]):
						return True

			return False
		
		# To check whether word is accepted:
		# check if there is an accepting run from the initial state for word
		if _accepts(word, self.initial, []):
			return True
		return False
		
		
	def is_deterministic(self):
		"""
		Returns whether this automaton is deterministic.
		
		An automaton is deterministic iff for each state, there is at most
		one successor for each character.
		"""
		
		# Maintain two structures:
		# 	- one stack to perform the search (here, BFS)
		#	- one set to store visited states
		
		pending = [self.initial]
		visited = set()
		
		while len(pending) > 0:
			s0 = pending.pop()			
			visited.add(s0)
			for char in s0.successors:
				if len(s0.successors[char]) > 1:
					return False
				for s in s0.successors[char]:
					if s not in visited:
						pending.append(s)
			
		return True
		
	def copy(self):
		"""
		Returns a new automaton, composed of new states, that is a copy
		of this automaton.
		"""
		
		# Get all states
		# Copy them
		# Copy transitions
		# Get accepting states
		# Return automaton
		
		# Get all states
		visited = set()
		pending = [self.initial]
		
		while len(pending) > 0:
			s = pending.pop()
			visited.add(s)
			for char in s.successors:
				for sp in s.successors[char]:
					if sp not in visited:
						pending.append(sp)
						
		# Copy states
		copies = {}
		for s in visited:
			copies[s] = State()
			
		# Copy transitions
		for s in visited:
			for char in s.successors:
				for sp in s.successors[char]:
					copies[s].add_successor(char, copies[sp])
					
		# Get accepting states
		accepting = set()
		for s in visited:
			if s in self.accepting:
				accepting.add(copies[s])
				
		return Automaton(copies[self.initial], accepting)	