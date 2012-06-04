from .regex import Concat, Choice, Repeat, Range
from ..automaton.automaton import Automaton
from ..automaton.state import State, LAMBDA

def regex_to_automaton(regex):
	"""
	Transforms regex into a non-deterministic automaton.
	"""
	
	if type(regex) == Range:
		# >s0 -range> (s1)
		s0 = State()
		s1 = State()
		
		for char in regex.range:
			s0.add_successor(char, s1)
		
		return Automaton(s0, set([s1]))
		
	if type(regex) == Choice:
		# Add an initial state
		# Add a lambda transition from this state to initial states of
		# automata for left and right
		# The new automaton has the initial state and its accepting ones
		# are the accepting ones of left and right
		l = regex_to_automaton(regex.left)
		r = regex_to_automaton(regex.right)
		
		s0 = State()
		
		s0.add_successor(LAMBDA, l.initial)
		s0.add_successor(LAMBDA, r.initial)
			
		return Automaton(s0, l.accepting | r.accepting)
		
	if type(regex) == Repeat:
		# Add an initial accepting state with lamda transition
		# to child initial one
		# Add a lambda transition from all accepting to the initial state
		# The new automaton has the new initial accepting state
		c = regex_to_automaton(regex.child)
		
		s0 = State()
		
		s0.add_successor(LAMBDA, c.initial)
		for s in c.accepting:
			s.add_successor(LAMBDA, s0)
			
		return Automaton(s0, set([s0]))
		
	if type(regex) == Concat:
		# Add an intermediate state leading through lambda to the initial state
		# of right
		# Add lambda transitions from all accepting states of left to this
		# intermediate state
		# The new automaton has the same initial state as left
		# and same accepting states has right
		l = regex_to_automaton(regex.left)
		r = regex_to_automaton(regex.right)
		
		s0 = State()
		
		for s in l.accepting:
			s.add_successor(LAMBDA, s0)
		s0.add_successor(LAMBDA, r.initial)
			
		return Automaton(l.initial, r.accepting)