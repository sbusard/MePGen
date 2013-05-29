from .automaton import Automaton
from .automaton import State, LAMBDA
from .automaton import remove_lambdas, determinize, automaton_to_wordtree
from .wordtree.transformation import remove_empty_subtrees

class Regex():
    """
    A Regex represents a regular expression. Each Regex has a type
    (CONCAT, CHOICE, REPEAT, RANGE).
    
    For example, the regular expression (a.(b|c))* is represented by
    (   REPEAT, 
        (   CONCAT,
            (RANGE('a')),
            (   CHOICE,
                (RANGE('b')),
                (RANGE('c'))
            )
        )
    )
    """
        

class Concat(Regex):
    
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def __str__(self):
        return "(" + str(self.left) + " . " + str(self.right) + ")"
        
    def copy(self):
        return Concat(self.left.copy(), self.right.copy())
        

class Choice(Regex):

    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def __str__(self):
        return "(" + str(self.left) + " | " + str(self.right) + ")"
        
    def copy(self):
        return Concat(self.left.copy(), self.right.copy())
        
        
class Repeat(Regex):
    
    def __init__(self, child):
        self.child = child
    
    def __str__(self):
        return "(" + str(self.child) + ")*"
        
    def copy(self):
        return Concat(self.child.copy())


class Range(Regex):
    
    def __init__(self, regrange):
        """
        regrange is a frozenset of strings.
        """
        self.range = regrange
        
    def __str__(self):
        return str(self.range)
        
    def copy(self):
        return Range(self.range)
        
        
class AutomatonReg(Regex):
    """
    Automaton regex is a regex defined by an automaton.
    """
    
    def __init__(self, automaton):
        self.automaton = automaton
        
    def __str__(self):
        return "Automaton(" + str(self.automaton) + ")"
    
    def copy(self):
        return AutomatonReg(self.automaton.copy())



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
        
    if type(regex) == AutomatonReg:
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