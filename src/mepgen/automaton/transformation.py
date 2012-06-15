from .state import LAMBDA, State
from .automaton import Automaton
from ..wordtree.wordtree import Wordtree

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
				if c in s.successors:
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


def automaton_to_wordtree(automaton, depth):
	"""
	Returns the wordtree corresponding to the unrolling of automaton depth time.
	This means that the resulting wordtree recognizes all words of length depth
	that automaton recognizes.
	The resulting wordtree can contain empty subtrees.
	"""
	
	
	def _automaton_to_wordtree(built, accepting, state, depth):
		"""
		Returns the wordtree corresponding to unrolling state depth time.
		Uses accepting as the set of accepting states to correctly set as
		accepting or not the created wordtree nodes.
		built is a dictionary of (state, depth) to wordtree, used to save memory
		by reusing built wordtrees.
		"""
	
		# Generate the mapping range -> state
		#	=> create a dictionary where keys are states, values are ranges
		# For each state, get the sub-wordtree of depth-1
		# Create the new wordtree with the correct ranges
		
		if depth <= 0:
			return Wordtree({}, state in accepting)
		
		ranges = {}
		states = set()
		for c in state.successors:
			for s in state.successors[c]:
				states.add(s)
				if s not in ranges:
					ranges[s] = set()
				ranges[s].add(c)
				
		successors = {}
		for s in states:
			if (s, depth-1) in built:
				successors[frozenset(ranges[s])] = built[(s, depth-1)]
			else:
				successors[frozenset(ranges[s])] = \
								_automaton_to_wordtree(	built, accepting,
														s, depth-1)
		wt = Wordtree(successors)
		built[(state, depth)] = wt
		return wt
		
	
	# Warning: only wordtree with depth 0 have to be accepting, and only if
	# the corresponding state of automaton is accepting.
	# This ensures to recognize only words of length depth instead of words
	# of length at most depth.
	
	return _automaton_to_wordtree(	{}, automaton.accepting,
									automaton.initial, depth)
									
									
def reject_short_words(automaton, minlen):
	"""
	Returns a copy of automaton that accepts the set of words that automaton
	accepts and have a length >= minlen.
	automaton must contain no lambda transitions.
	
	This function introduces lambda transitions into the returned automaton.
	"""
	
	# Create an automaton that is an unrolling of automaton to minlen,
	# set the end states as accepting
	# and add a lambda transition from all these states to the initial state
	# of the copy of the original automaton.
	
	# Starts with a copy of automaton.initial
	s0 = State()
	currentStage = {s0 : automaton.initial}
	currentCopy = {automaton.initial : s0}
	nextStage = {}
	
	# For each stage
	for i in range(minlen):
		# For each unrolled state, get its corresponding state of automaton
		for s in currentStage:
			for c in currentStage[s].successors:
				for sp in currentStage[s].successors[c]:
					# unroll it, i.e.
					#	create a copy of each of its successors,
					#	if this copy does not exist yet,
					if sp not in currentCopy:
						news = State()
						currentCopy[sp] = news
					else:
						news = currentCopy[sp]
					# 	add the existing transitions
					s.add_successor(c, news)
					# and keep the copy for the next stage
					nextStage[news] = sp
		currentStage = nextStage
		currentCopy = {}
		nextStage = {}
		
	# Get final states and set them as accepting
	accepting = currentStage.keys()
	
	# Get a copy of the original automaton
	autcopy = automaton.copy()
	
	# Add a lambda transition from every accepting state to autcopy initial
	for s in accepting:
		s.add_successor(LAMBDA, autcopy.initial)
		
	# Return the new automaton, composed of the unrolling above and the copy
	return Automaton(s0, set(accepting) | autcopy.accepting)