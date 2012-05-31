class Automaton:
	"""
	An Automaton represents an automaton. It is composed of states and a
	transition relation over an alphabet. Furthermore, a subset of states are
	the initial ones and another subset are the accepting ones.
	
	An Automaton stores the list of initial and accepting states.
	
	Simon Busard <simon.busard@gmail.com>
	30 - 05 - 2012
	"""
	
	def __init__(self, initials = [], accepting = []):
		self.initials = initials
		self.accepting = accepting