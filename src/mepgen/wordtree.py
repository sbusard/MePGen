from random import random

class Wordtree:
    """
    A Wordtree is a tree recognizing a word.
    It is a state with a set of successors, reachable through a range of
    characters. Furthermore, a Wordtree may be accepting, and is also labeled
    with the number of different words it can recognize.
    
    Simon Busard <simon.busard@gmail.com>
    04 - 06 - 2012
    """
    
    def __init__(self, successors, accepting = False):
        """
        Creates a new Wordtree.
        
        successors is a dictonary with frozensets of characters as keys
        and Wordtrees as values. successors[{c1,c2,...,cn}] = wt means that
        wt is reachable from this Wordtree through characters c1 to cn.
        
        For the tree words count to be correct,
        the set of keys must be disjoint, meaning that
        no character is in two different sets. This is not verified.
        """
        self.successors = successors
        self.accepting = accepting
        self.wordscount = accepting and 1 or 0
        for ranges in successors:
            self.wordscount += len(ranges) * successors[ranges].wordscount
        
            
    def __str__(self):
        pass # TODO
        
        
    def copy(self):     
        def _copy(visited, wordtree):
            """
            Copies the given wordtree by using visited as a dictionary of
            already copied sub-wordtrees.
            """
            
            if len(wordtree.successors) <= 0:
                wt = Wordtree({}, wordtree.accepting)
                visited[wordtree] = wt
                return wt

            else:
                successors = {}
                for ranges in wordtree.successors:
                    wtr = wordtree.successors[ranges]
                    if wtr in visited:
                        successors[ranges] = visited[wtr]
                    else:
                        successors[ranges] = _copy(visited, wtr)
                wt = Wordtree(successors, wordtree.accepting)
                visited[wordtree] = wt
                return wt
                
        return _copy({}, self)      
            
            
    def accepts(self, word):
        """
        Returns whether the given word is accepted by this wordtree.
        
        A word is accepted iff there is a run this tree that accepts the word.
        A run accepts the word if it ends in an accepting state.
        """
        
        if word == '':
            return self.accepting
            
        else:
            for ranges in self.successors:
                if word[0] in ranges:
                    if self.successors[ranges].accepts(word[1:]):
                        return True
                        
        return False
    
    
    def randomrun(self):
        """
        Returns a random accepting run of this tree.
        The result is a random word accepted by this tree.
        This tree must accept at least one word.
        """
        
        if self.wordscount <= 0:
            print("[ERROR] Cannot produce a randomrun since no word is possible!")
        
        # We have to select a possible next character
        # First, select a range, based on number of words for successors
        # Then, in the selected range, select uniformly the next character
        
        if len(self.successors) <= 0:
            return ''
            
        # Select the range:
        # we have to select a range r_i
        # of n_i characters to a state of m_i characters
        # with a probability of n_i * m_i / sum_j(n_j * m_j)
        
        # to select a range with the specified probability,
        # save for each range, two bounds, (last-bound, last-bound + n_i*m_i)
        # then select between 0 and last-bound, and select the range
        # surrounding the value

        lastbound = 0
        bounds = {}
        for ranges in self.successors:
            newbound=lastbound+self.successors[ranges].wordscount*len(ranges)
            bounds[(lastbound,newbound)] = (ranges, self.successors[ranges])
            lastbound = newbound
            
        ranid = int(random() * lastbound)
        
        for (beg, end) in bounds:
            if beg <= ranid and ranid < end:
                ran, state = bounds[(beg, end)]
                # Select the character:
                # the next character is uniformly selected in the selected range
                charid = int(random() * len(ran))
                return list(ran)[charid] + state.randomrun()
           
                
    def get_alphabet(self):
        """
        Returns the alphabet of this wordtree.
        The alphabet of this wordtree is the set of possible characters this
        wordtree uses. It only consider characters leading to children
        recognizing some words.
        """
        
        alphabet = set()
        for ran in self.successors:
            if self.successors[ran].wordscount > 0:
                alphabet |= ran
        return alphabet



def remove_empty_subtrees(wordtree):
    """
    Returns a copy of wordtree where all subtrees of wordtree
    that recognize no word are removed.
    Returns None if wordtree recognizes no word.
    """
    
    def _remove_empty_subtrees(visited, wordtree):
        """
        Removes empty substrees of wordtree, i.e. subtrees that recognize no
        words.
        wordtree is modified in place.
        wordtree must recognize some words.
        visited is a dictionary from wordtree nodes to their copy without
        empty subtrees.
        """
        
        succs = {}
        for ranges in wordtree.successors:
            wt = wordtree.successors[ranges]
            if wt.wordscount != 0:
                if wt in visited:
                    succs[ranges] = visited[wt]
                else:
                    succs[ranges] = _remove_empty_subtrees(visited, wt)
        w = Wordtree(succs, wordtree.accepting)
        visited[wordtree] = w
        return w
        
    
    if wordtree.wordscount == 0:
        return None

    return _remove_empty_subtrees({}, wordtree)