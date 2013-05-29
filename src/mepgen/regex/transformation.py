from .regex import Concat, Choice, Repeat, Range, Automaton as AutoReg
from ..automaton import Automaton
from ..automaton import State, LAMBDA
from ..automaton import remove_lambdas, determinize, automaton_to_wordtree
from ..wordtree.transformation import remove_empty_subtrees

def regex_to_automaton(regex):
    """
    Transforms regex into a non-deterministic automaton.
    """
    
    if type(regex) == Range:
        # >s0 -range> (s1)
        s0 = State()
        s1 = State()
        
        s0.add_successor(regex.range, s1)
        
        return Automaton(s0, frozenset([s1]))
        
    if type(regex) == Choice:
        # Add an initial state
        # Add a lambda transition from this state to initial states of
        # automata for left and right
        # The new automaton has the initial state and its accepting ones
        # are the accepting ones of left and right
        l = regex_to_automaton(regex.left)
        r = regex_to_automaton(regex.right)
        
        s0 = State()
        
        s0.add_successor(frozenset([LAMBDA]), l.initial)
        s0.add_successor(frozenset([LAMBDA]), r.initial)
            
        return Automaton(s0, l.accepting | r.accepting)
        
    if type(regex) == Repeat:
        # Add an initial accepting state with lamda transition
        # to child initial one
        # Add a lambda transition from all accepting to the initial state
        # The new automaton has the new initial accepting state
        c = regex_to_automaton(regex.child)
        
        s0 = State()
        
        s0.add_successor(frozenset([LAMBDA]), c.initial)
        for s in c.accepting:
            s.add_successor(frozenset([LAMBDA]), s0)
            
        return Automaton(s0, frozenset([s0]))
        
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
            s.add_successor(frozenset([LAMBDA]), s0)
        s0.add_successor(frozenset([LAMBDA]), r.initial)
            
        return Automaton(l.initial, r.accepting)
        
    if type(regex) == AutoReg:
        # Take a copy of the automaton and return it
        return regex.automaton.copy()
        
        
def regex_to_wordtree(regex, depth):
    """
    Returns the wordtree of depth depth recognizing words of length depth
    recognized by regex.
    """
    
    # Transform regex to automaton
    automaton = regex_to_automaton(regex)
    # Remove lambdas, determinize automaton
    automaton = remove_lambdas(automaton)
    automaton = determinize(automaton)
    # Get the tree, remove empty subtrees
    wordtree = automaton_to_wordtree(automaton, depth)
    wordtree = remove_empty_subtrees(wordtree)
    return wordtree