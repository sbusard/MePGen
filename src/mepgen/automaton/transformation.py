from .state import LAMBDA, State
from .automaton import Automaton

def minimize(automaton):
	"""
	Returns the minimization of automaton.
	"""
	pass # TODO
	
	
def determinize(automaton):
	"""
	Returns the determinization of automaton.
	"""
	
	def _get_chars(stateset):
		"""
		Returns the set of characters such that, for each character c,
		there is at least one state in stateset having a transition labeled
		with c.
		"""
		
		chars = set()
		for s in stateset:
			chars = chars | set(s.successors)
			
		return chars
		
	
	# Subsets of states of automaton become states of the determinized automaton
	# Start with the subset of initial states
	# For each new state s, there is an x-transition to another state s' iff
	# there is a state in s with an x-transition to s';
	
	# Use a stack and a dictionary; the stack stores the new states that have
	# no transitions yet, the ditionary stores the information about which
	# subset of states correspond to which new state.
	# - Start with the stack filled with the subset containing only the initial
	# state, the dictionary contains the mapping between this subset and the new
	# state. Be aware of acceptance.
	# - While the stack in non-empty,
	#		- take the next subset
	#		- add transitions for this subset
	#			- for each character,
	#				- get the union of the successors
	#					of the states of the subset
	#				- if this new subset has no corresponding state,
	#					- create it and add the subset to the stack
	#					- add it to accepting ones if one of them is accepting
	#				- add a transition with this character from the new
	#					state of the subset to the corresponding state
	
	ss0 = frozenset([automaton.initial])
	pending = [ss0]
	mapping = {ss0:State()}
	accepting = set()
	if automaton.initial in automaton.accepting:
		accepting.add(mapping[ss0])
	
	while len(pending) > 0:
		ss = pending.pop()
		cc = _get_chars(ss)
		for c in cc:
			succs = set()
			for s in ss:
				succs = succs | s.successors[c]
			succs = frozenset(succs)
			if succs not in mapping:
				mapping[succs] = State()
				pending.append(succs)
				if len(succs & automaton.accepting) > 0:
					accepting.add(mapping[succs])
			mapping[ss].add_successor(c, mapping[succs])
			
	return Automaton(mapping[ss0], accepting)
	
	
def remove_lambdas(automaton):
	"""
	Returns a new automaton accepting the same language as automaton but
	containing no lambda transition.
	"""
	
	def _get_lambda_reachable(state):
		"""
		Returns the set of states reachable
		through lamda transitions from state.
		"""
		
		pending = [state]
		visited = set()
		reachable = set()
		
		while len(pending) > 0:
			s0 = pending.pop()
			visited.add(s0)
			if LAMBDA in s0.successors:
				reachable = reachable | s0.successors[LAMBDA]
				for s in [s for s in s0.successors[LAMBDA] \
							if s not in (visited | set(pending))]:
					pending.append(s)
				
		return reachable
			
	
	# Copy the automaton, then
	# for each state (use a stack and a visited set to compute all states once)
	#	- get all states reachable from lambda transitions
	#		(use a stack and a set, check the set to avoid looping)
	#	- for each of these states, for each character except lambda,
	#		add a transition with this character from the current state
	#		to the reached one
	#	- remove all lambda transitions from the current state
	
	# Note: we can remove lambda transitions from the current state and do not
	# wait until the end of the visit since every one-non-lambda-character paths
	# are preserved by the addition of new transitions.
	
	automaton = automaton.copy()
	
	pending = [automaton.initial]
	visited = set()
	
	while len(pending) > 0:
		s0 = pending.pop()
		visited.add(s0)
		
		reachable = _get_lambda_reachable(s0)
		
		for s in reachable:
			for c in [c for c in s.successors if c != LAMBDA]:
				for sp in s.successors[c]:
					s0.add_successor(c, sp)
			if s in automaton.accepting:
				automaton.accepting.add(s0)
				
		for c in s0.successors:
			for s in s0.successors[c]:
				if s not in visited | set(pending):
					pending.append(s)
					
		if LAMBDA in s0.successors:
			del s0.successors[LAMBDA]
		
	return automaton


def automaton_to_wordtree(automaton):
	pass # TODO