from .state import LAMBDA

class Automaton:
	"""
	An Automaton represents an automaton. It is composed of states and a
	transition relation over an alphabet. Furthermore, a subset of states are
	the initial ones and another subset are the accepting ones.
	
	An Automaton stores the sets of initial and accepting states.
	
	Simon Busard <simon.busard@gmail.com>
	30 - 05 - 2012
	"""
	
	def __init__(self, initials = None, accepting = None):
		self.initials = initials or set()
		self.accepting = accepting or set()
		
	def __str__(self):
		pass # TODO
		
	def accepts(self, word):
		"""
		Returns whether the word is accepted by this automaton.
		Since this automaton is potentially non-deterministic and non-minimal,
		it accepts word iff there is a run that accepts word.
		"""
		
		# To check whether word is accepted:
		# check if there is an accepting run from any initial state for word
		for s0 in self.initials:
			if self._accepts(word, s0, []):
				return True
		return False
		
	def _accepts(self, word, start, lambdas):
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
					if self._accepts(word[1:], s, []):
						return True
		if LAMBDA in start.successors:
			for s in [x for x in start.successors[LAMBDA] \
						if x not in lambdas]:
				if self._accepts(word, s, lambdas + [start]):
					return True
		
		return False