from .wordtree import Wordtree

class Automaton:
    """
    An Automaton represents an automaton. It is composed of states and a
    transition relation over an alphabet. Furthermore, a state is
    the initial one and a subset of the states are the accepting ones.
    
    An Automaton stores the initial state and the set of accepting states.
    
    Simon Busard <simon.busard@gmail.com>
    30 - 05 - 2012
    """
    
    def __init__(self, initial, accepting = None):
        self.initial = initial
        self.accepting = accepting or set()
        
        
    def __str__(self):
        pass # TODO
        
        
    def accepts(self, word):
        """
        Returns whether the word is accepted by this automaton.
        Since this automaton is potentially non-deterministic and non-minimal,
        it accepts word iff there is a run that accepts word.
        """
        
        def _accepts(word, start, lambdas):
            """
            Recursive run of this automaton from the state start, for word.
            lambdas is the set of states already visited when traversing
            a LAMBDA transition.
            """

            # To check whether this automaton accepts word from start,
            # the word is accepted if
            #   - the word is empty and start is accepting, or
            #   - the word is emtpy and accepted by any state reachable
            #       through a lambda transition that is not in lambdas, or
            #   - the word without its first character is accepted 
            #       by a state reachable through a transition labeled
            #       with its first character, or
            #   - the word is accepted by a state reachable through a lambda
            #       transition that is not in lambdas.
            # the word is not accepted otherwise

            if word == '':
                if start in self.accepting:
                    return True
            else:
                for ran in [r for r in start.successors if word[0] in r]:
                    for s in start.successors[ran]:
                        if _accepts(word[1:], s, set()):
                            return True
            for ran in [r for r in start.successors if LAMBDA in r]:
                for s in [x for x in start.successors[ran] if x not in lambdas]:
                    if _accepts(word, s, lambdas | set([start])):
                        return True

            return False
        
        # To check whether word is accepted:
        # check if there is an accepting run from the initial state for word
        if _accepts(word, self.initial, set()):
            return True
        return False
        
        
    def is_deterministic(self):
        """
        Returns whether this automaton is deterministic.
        
        An automaton is deterministic iff for each state, there is at most
        one successor for each character.
        """
        
        # Maintain two structures:
        #   - one stack to perform the search
        #   - one set to store visited states
        
        pending = [self.initial]
        visited = set()
        
        while len(pending) > 0:
            s0 = pending.pop()          
            visited.add(s0)
            chars = s0.get_possible_chars()
            for char in chars:
                nexts = s0.get_successors_by_char(char)
                if len(nexts) > 1:
                    return False
                for s in nexts:
                    if s not in visited:
                        pending.append(s)
            
        return True
        
    def copy(self):
        """
        Returns a new automaton, composed of new states, that is a copy
        of this automaton.
        """
        
        # Get all states
        # Copy them
        # Copy transitions
        # Get accepting states
        # Return automaton
        
        # Get all states
        visited = set()
        pending = [self.initial]
        
        while len(pending) > 0:
            s = pending.pop()
            visited.add(s)
            for ran in s.successors:
                for sp in s.successors[ran]:
                    if sp not in visited:
                        pending.append(sp)
                        
        # Copy states
        copies = {}
        for s in visited:
            copies[s] = State()
            
        # Copy transitions
        for s in visited:
            for ran in s.successors:
                for sp in s.successors[ran]:
                    copies[s].add_successor(ran, copies[sp])
                    
        # Get accepting states
        accepting = set()
        for s in visited:
            if s in self.accepting:
                accepting.add(copies[s])
                
        return Automaton(copies[self.initial], accepting)



# Lambda character
LAMBDA = '<lambda>'


class State:
    """
    A State represents a state of an automaton.
    
    It has a list of successors. Every successor is reachable through a
    transition labelled with a character.
    
    The transition relation is represented by a dictionary where the keys
    are the characters ranges and the elements are sets of successor states.
    Only one copy of each state is stored such that adding twice the same state
    has no effect.
    
    Simon Busard <simon.busard@gmail.com>
    30 - 05 - 2012
    """
    
    def __init__(self, successors = None):
        self.successors = successors or {}
        
    def add_successor(self, ran, succ):
        """
        Adds succ as a successor for this state, reachable through
        the characters or range ran. ran is a list of string, each string
        being considered as a character.
        If succ is already reachable through this range, nothing changes.
        """
        if ran not in self.successors:
            self.successors[ran] = set([succ])
        else:
            self.successors[ran].add(succ)
            
    def remove_successor(self, char, succ):
        """
        Removes succ from successors of this state through the character char.
        If succ is not reachable through char from this state, does nothing.
        """
        for ran in [r for r in self.successors if char in ran]:
            self.successors[ran].remove(succ)
            
    def __str__(self):
        rep = "state(" + str(self.successors) + ")"
        return rep
        
            
    def get_possible_chars(self):
        """
        Returns the set of characters for which there is successor
        in this state.
        """
        return {char for ran in self.successors for char in ran}
        
        
    def get_successors(self):
        """
        Returns the set of successors of this state.
        """
        return {s for ran in self.successors for s in self.successors[ran]}
        
    
    def get_successors_by_char(self, char):
        """
        Returns the set of states reachable from this state
        through a transition labeled by char.
        """
        
        return {s   for ran in self.successors
                    if char in ran
                    for s in self.successors[ran]}



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
        return {c for s in stateset for c in s.get_possible_chars()}
        
    
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
    #       - take the next subset
    #       - add transitions for this subset
    #           - for each character,
    #               - get the union of the successors
    #                   of the states of the subset
    #               - if this new subset has no corresponding state,
    #                   - create it and add the subset to the stack
    #                   - add it to accepting ones if one of them is accepting
    #               - add a transition with this character from the new
    #                   state of the subset to the corresponding state
    
    ss0 = frozenset([automaton.initial])
    pending = [ss0]
    mapping = {ss0:State()}
    accepting = set()
    if automaton.initial in automaton.accepting:
        accepting.add(mapping[ss0])
    
    transitions = {}
    while len(pending) > 0:
        ss = pending.pop()
        cc = _get_chars(ss)
        for c in cc:
            succs = set()
            for s in ss:
                succs = succs | s.get_successors_by_char(c)
            succs = frozenset(succs)
            if succs not in mapping:
                mapping[succs] = State()
                pending.append(succs)
                if len(succs & automaton.accepting) > 0:
                    accepting.add(mapping[succs])
            if (ss, succs) not in transitions:
                transitions[(ss, succs)] = set()
            transitions[(ss, succs)] |= {c}
            
    for (s, sp) in transitions:
        mapping[s].add_successor(frozenset(transitions[(s, sp)]), mapping[sp])
            
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
            for s in s0.get_successors_by_char(LAMBDA):
                reachable |= {s}
                if s not in visited:
                    pending.append(s)
                
        return reachable
            
    
    # Copy the automaton, then
    # for each state (use a stack and a visited set to compute all states once)
    #   - get all states reachable from lambda transitions
    #       (use a stack and a set, check the set to avoid looping)
    #   - for each of these states, for each character except lambda,
    #       add a transition with this character from the current state
    #       to the reached one
    #   - remove all lambda transitions from the current state
    
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
        
        # Add a transition for each transition from a LAMBDA reachable state
        for s in reachable:
            for ran in s.successors:
                for sp in s.successors[ran]:
                    s0.add_successor(ran, sp)
            if s in automaton.accepting:
                automaton.accepting.add(s0)
                
        # Add all unvisited successors to pending
        for s in s0.get_successors():
            if s not in visited:
                pending.append(s)
                
        # Remove LAMBDAs
        for ran in [r for r in s0.successors if LAMBDA in r]:
            if len(ran) == 1:   # ran contains only LAMBDA
                del s0.successors[ran]
            else:
                # Remove LAMBDA from ran. To do this, remove the transition,
                # compute the new range (ran - LAMBDA) and re-add the transition
                succs = s0.successors[ran]
                del s0.successors[ran]
                ranp = frozenset(ran - {LAMBDA})
                s0.add_successor(ranp, succs)
        
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
        #   => create a dictionary where keys are states, values are ranges
        # For each state, get the sub-wordtree of depth-1
        # Create the new wordtree with the correct ranges
        
        if depth <= 0:
            return Wordtree({}, state in accepting)
        
        successors = {}
        for ran in state.successors:
            for s in state.successors[ran]:
                if (s, depth - 1) in built:
                    successors[ran] = built[(s, depth - 1)]
                else:
                    successors[ran] = _automaton_to_wordtree(built, accepting,
                                                             s, depth - 1)
        wt = Wordtree(successors)
        built[(state, depth)] = wt
        return wt
        
    
    # Warning: only wordtree with depth 0 have to be accepting, and only if
    # the corresponding state of automaton is accepting.
    # This ensures to recognize only words of length depth instead of words
    # of length at most depth.
    
    return _automaton_to_wordtree(  {}, automaton.accepting,
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
    
    # Get a copy of the original automaton
    automaton = automaton.copy()
    
    # Starts with a copy of automaton.initial
    s0 = State()
    currentStage = {s0 : automaton.initial}
    currentCopy = {automaton.initial : s0}
    nextStage = {}
    
    # For each stage
    for i in range(minlen):
        # For each unrolled state, get its corresponding state of automaton
        for s in currentStage:
            for ran in currentStage[s].successors:
                for sp in currentStage[s].successors[ran]:
                    # unroll it, i.e.
                    #   create a copy of each of its successors,
                    #   if this copy does not exist yet,
                    if sp not in currentCopy:
                        news = State()
                        currentCopy[sp] = news
                    else:
                        news = currentCopy[sp]
                    #   add the existing transitions
                    s.add_successor(ran, news)
                    # and keep the copy for the next stage
                    nextStage[news] = sp
        currentStage = nextStage
        currentCopy = {}
        nextStage = {}
        
    # Get final states and set them as accepting
    accepting = currentStage.keys()
    
    # Add a lambda transition from every accepting state to autcopy initial
    # FIXME We cannot do that! 'abcD' is accepted
    # while the original does not accept 'D' after 'c'!
    for s in accepting:
        s.add_successor(frozenset({LAMBDA}), currentStage[s])
        
    # Return the new automaton, composed of the unrolling above and the copy
    return Automaton(s0, set(accepting) | automaton.accepting)