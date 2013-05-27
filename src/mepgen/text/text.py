from ..wordtree.wordtree import Wordtree
from ..automaton.state import State
from ..automaton.automaton import Automaton

def text_to_matrix(text, charfilter=None):
    """
    Returns a matrix where to each row and column is associated a non-blank
    character, such that the (i,j) value of the matrix is the number of times
    character i is followed by character j in the given text.
    If charfilter is not None, it is used as a filter for allowed characters.
    charfilter is then a function taking one character as argument and returning
    a boolean saying whether or not the character has to be taken into account
    or not.
    
    The returned matrix is a dictionary where keys are characters and values
    are dictionaries. The inner dictionary has characters as keys
    and positive integers as values.
    This representation of the matrix does not represent explicitely value 0.
    Instead, the value is missing.
    """
    
    def _inc_value(matrix, c1, c2):
        """
        Increment the value of matrix[c1][c2].
        If such a value does not exist yet, put it at 1.
        Returns nothing.
        """
        
        if c1 not in matrix:
            matrix[c1] = {}
        if c2 not in matrix[c1]:
            matrix[c1][c2] = 0
        matrix[c1][c2] += 1
        
    
    matrix = {}

    for i in range(len(text) - 1):
        if charfilter == None or \
           (charfilter(text[i]) and charfilter(text[i + 1])):
            _inc_value(matrix, text[i], text[i + 1])
            
    return matrix
    
    
def threshold_matrix(matrix, threshold):
    """
    Returns a new matrix m where, for each character c, 
    each non zero value in m[c] is the same as the one in
    matrix and no value is below sum(matrix[c]) * threshold, for each c.
    
    The returned matrix is a new matrix.
    It is a dictionary where keys are characters and values
    are dictionaries. The inner dictionary has characters as keys
    and positive integers as values.
    This representation of the matrix does not represent explicitely value 0.
    Instead, the value is missing.
    """
    
    def _set_value(matrix, c1, c2, value):
        """
        Set the value of matrix[c1][c2] to value.
        If such a value does not exist yet, create it.
        Returns nothing.
        """
        
        if c1 not in matrix:
            matrix[c1] = {}
        if c2 not in matrix[c1]:
            matrix[c1][c2] = 0
        matrix[c1][c2] = value
        
    
    newmatrix = {}
    
    # For each pair (c1, c2), if the value matrix[c1][c2] is higher
    # than rowsum, save it in newmatrix. Otherwise, drop it.
    
    for c1 in matrix:
        rowsum = 0
        for c2 in matrix[c1]:
            rowsum += matrix[c1][c2]
        minvalue = rowsum * threshold
        for c2 in matrix[c1]:
            if matrix[c1][c2] >= minvalue:
                _set_value(newmatrix, c1, c2, matrix[c1][c2])
                
    return newmatrix
    
    
def extract_successors(matrix):
    """
    Extract successors from matrix.
    
    matrix is a dictionary with chars as keys and dictionaries as values.
    Each inner dictionary gives the possible chars successing to the key.
    The value of each element of inner dictionaries is unspecified.
    
    successors are extracted from matrix. The returned dictionary has same keys
    as matrix, and each value is a set of possible next chars, such that
    c2 is in successors[c1] iff c2 is a key of matrix[c1].
    """
    
    successors = {}
    for c1 in matrix:
        successors[c1] = set()
        for c2 in matrix[c1]:
            successors[c1].add(c2)
    return successors
    

def successors_to_automaton(successors):
    """
    Returns the automaton based on successors.
    
    successors gives, for each char of a set of characters,
    the set of possible successing characters.
    
    From successors, returns an automaton such that every state is accepting,
    and every accepted word is composed of characters such that every two pairs
    of chars are successing regarding to successors.
    
    successors is a dictionary with chars as keys and set of chars as values.
    """
    
    # The automaton has one initial state.
    # In addition to this state, there is a state for each character appearing
    # in successors (as key or in sets).
    # There is a transition from state s1 to state s2 iff s1 is initial
    # or the character of s1 can be followed by the char of s2 regarding to
    # successors, i.e. char(s2) is in successors[s1]
    # All states except the initial one are accepting.
    
    s0 = State()
    states = {}
    allstates = set()
    
    ranges = {}
    for c in successors:
        if c not in states:
            states[c] = State()
            allstates.add(states[c])
        if (s0, states[c]) not in ranges:
            ranges[(s0, states[c])] = set()
        ranges[(s0, states[c])] |= {c}
        for cp in successors[c]:
            if cp not in states:
                states[cp] = State()
                allstates.add(states[cp])
            if (states[c], states[cp]) not in ranges:
                ranges[(states[c], states[cp])] = set()
            ranges[(states[c], states[cp])] |= {cp}
            
    for (s, sp) in ranges:
        s.add_successor(frozenset(ranges[(s, sp)]), sp)
            
    return Automaton(s0, allstates)
        

def text_to_automaton(text, charfilter, threshold):
    """
    Returns the automaton accepting all words of any length > 0 such that
    every character c of the word appears in text and charfilter(c) is True.
    threshold is used to eliminate the too rare following characters, i.e.
    for each character c of text, it can be followed in accepting words only
    by characters that occur after c at least (threshold * 100)% of the time.
    """

    matrix = text_to_matrix(text, charfilter)
    matrix = threshold_matrix(matrix, threshold)
    succs = extract_successors(matrix)
    return successors_to_automaton(succs)