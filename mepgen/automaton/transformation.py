from .state import LAMBDA

def minimize(automaton):
	"""
	Returns the minimization of automaton.
	"""
	pass # TODO
	
	
def determinize(automaton):
	"""
	Returns the determinization of automaton.
	"""
	pass # TODO
	
	
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
				
	pending = [automaton.initial]
	visited = set()
	while len(pending) > 0:
		s0 = pending.pop()
		visited.add(s0)
		
		for c in s0.successors:
			for s in [s for s in s0.successors[c] if s not in visited]:
				pending.append(s)
				
		if LAMBDA in s0.successors:
			del s0.successors[LAMBDA]
		
	return automaton
		