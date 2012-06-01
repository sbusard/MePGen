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
	pass # TODO
	
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