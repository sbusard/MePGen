import random

class ProbWordTree():
    """
    A ProbWordTree is a tree of n-gram successors:
      - each state corresponds to an n-gram;
      - each successor su of a state st is an n-gram such the n-1 last 
        characters
        of st are the n-1 first characters of su;
      - each edge between two states is weighted.
      - Finally, there are beginning n-grams states and finishing n-grams 
        states.
        
    A ProbWordTree is just a list of States representing the beginning n-grams
    of the tree.


    A walk of length l in a ProbWordTree is a path in the tree from
    a beginning n-gram, to a finishing n-gram, such that the resulting word
    has length l and is composed of the beginning n-gram, followed by all
    single characters that the corresponding states of the path add. The path 
    has thus length l-n+1 nodes, since the n first characters belong to the 
    beginning n-gram and then every other state adds one character to the word.

    For example, let's consider the following path:
        abc->bce->cel->eli->lin->ing
    This is a correct path since every successor shares n-1 (n = 3 here) 
    characters with its predecessor. Furthermore, consider that abc is a 
    beginning 3-gram and that ing is a finishing one.
    This path defines the word "abceling" of length 8.


    A random walk of length l in a ProbWordTree is a walk in the tree such that
    the successor of a state is randomly chosen through all its successors,
    with a distribution given by the weights of the corresponding edges.

    Note that for a random walk to be efficiently computed (by generating a 
    straight random path of the tree, without backtracking), we have to prune 
    the tree such that the only remaining paths effectively end in a finishing 
    n-gram after l-n+1 steps. In this framework, we only build a tree for given 
    and fixed l and n values.
    """
    
    def __init__(self, begngrams):
        """
        Initalize a ProbWordTree.
        
        begngrams -- a set of beginning n-grams states.
        """
        self.initials = begngrams
        
        
    def randomword(self, length):
        """
        Return a random word of length.
        length >= n, where n is the length of n-grams of this tree.
        """        
        first = random.choice(list(self.initials))
        ngram = first.ngram 
        return ngram[:-1] + first.randomword(length-len(ngram[:-1]))
        
    
class ProbState():
    """
    A ProbState is a state of a ProbWordTree. It is composed of a n-gram and
    a dictonary of successor => weight pairs. Furthermore, it can be finishing
    or not.
    """
    
    def __init__(self, ngram, successors=None, finishing=False):
        """
        Initialize a state.
        
        ngram -- the n-gram of this state;
        successors -- a dictionary of successor => weight pairs;
        finishing -- whether or not the n-gram is a finishing n-gram.
        """
        self.ngram = ngram
        self.successors = successors if successors else {}
        self.finishing = finishing
        
    def randomword(self, length):
        """
        Return a random word from this state and its successors.
        """
        
        def weighted_choice(weights):
            rnd = random.random() * sum(weights)
            for i, w in enumerate(weights):
                rnd -= w
                if rnd < 0:
                    return i

        def random_item(weightsdict):
            """
            Return a random key of weightsdict. The distribution is given by the
            values of keys in the dictionary.
            """
            keyvals = [(k, v) for k, v in weightsdict.items()]
            vals = [v for k, v in keyvals]
            return keyvals[weighted_choice(vals)][0]
        
        if length <= 0:
            return ""
        else:
            if len(self.successors) <= 0:
                print("[WARNING] No sucessor.")
                return self.ngram[-1]
            else:
                next = random_item(self.successors)
                return self.ngram[-1] + next.randomword(length - 1)
        

def ngramtable_to_probwordtree(ngt, n, length):
    """
    Build a ProbWordTree from the given n-gram table.
    
    ngt -- the n-gram table;
    n -- the length of the n-grams;
    length -- the intended word length.
    """
    # Get all n-grams of ngt
    ngrams = ngt.keys()
    allngrams = set()
    for ngram in ngrams:
        allngrams.add(ngram)
        for succ in ngt[ngram]:
            allngrams.add(succ)
    
    # Build one empty state per n-gram in ngt
    states = {}
    for ngram in allngrams:
        states[ngram] = ProbState(ngram) # TODO mark finishing states
        # TODO Get beginning states
    
    # for each such a state, build its successors
    for state in states.values():
        successors = {}
        if state.ngram in ngt:
            for ngram, occ in ngt[state.ngram].items():
                successors[states[ngram]] = occ
        state.successors = successors
        
    return ProbWordTree(states.values())


def ngramtable(words, n):
    """
    Compute the set of n-grams (with number of occurrences) of words
    and return a list containing these numbers of occurrences.
    n >= 1 !
    """
    
    def addngram(ngt, word, n):
        """
        Compute and store in ngt the set of n-grams of word.
        n >= 1 !
        """
        shifted = []
        for i in range(n+1):
            shifted.append(word[i:])
        for ngram in zip(*shifted):
            ngram = "".join(ngram)
            prev = ngram[:-1]
            next = ngram[1:]
            if prev not in ngt:
                ngt[prev] = {}
            if next not in ngt[prev]:
                ngt[prev][next] = 0
            ngt[prev][next] += 1
            
    ngt = {}
    for word in words:
        addngram(ngt, word, n)
    return ngt


def check_totality(ngt):
    """
    Check that the ngram table ngt is total, that is, for each ngram,
    there is another ngram strating with the n-1 last letters of
    the previous one.
    """
    for prev in ngt:
        for next in ngt[prev]:
            if next not in ngt:
                return False
    return False


import sys
if __name__ == "__main__":
    
    def get_text_from_filename(filename):
        """Return the content of filename"""
        f = open(filename,"r")
        text = f.read()
        f.close()
        return text

    nbwords = 10
    wordlen = 10
    n = 3

    if len(sys.argv) <= 1:
        print("[ERROR] Need text path.")
    else:
        filename = sys.argv[1]
        text = get_text_from_filename(filename)
        text = text.lower()
        text = "".join(filter(lambda x : x.isalpha() or x.isspace(), text))
        words = text.split()
        ngt = ngramtable(words, n)
        pwt = ngramtable_to_probwordtree(ngt, n, wordlen)
        for i in range(nbwords):
            print(pwt.randomword(wordlen))