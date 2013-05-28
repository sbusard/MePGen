import random

def presuftable(words):
    """
    Compute the set of prefixes and suffixes (with number of occurrences)
    of words and return a table containing these numbers of occurrences.
    """
    pst = {}
    for word in words:
        addpresuf(pst, word)
    return pst
        
        
def addpresuf(pst, word):
    """
    Compute and store in pst the set of prefixes and suffixes of word.
    """    
    for i in range(len(word)-1): # For all positions in word
        for p in range(i+1): # For all prefixes of word[:i+1]
            prefix = word[p:i+1]
            
            if prefix not in pst:
                pst[prefix] = {}
            
            for s in range(i+1,len(word)): # For all suffixes of word[i+1:]
                suffix = word[i+1:s+1]
                
                if suffix not in pst[prefix]:
                    pst[prefix][suffix] = 0
                
                pst[prefix][suffix] += 1
                

def psrndword(pst, length, maxpre=0, maxsuf=0):
    """
    Extract a random word of length from prefixes and suffixes of pst.
    Only maxpre-long prefixes are considered, if greater than 0.
    Only maxsuf characters are added every round, if greater than 0.
    """
    
    def weighted_choice(weights):
        rnd = random.random() * sum(weights)
        for i, w in enumerate(weights):
            rnd -= w
            if rnd < 0:
                return i
    
    # First letter
    word = random.choice(list(k for k in pst.keys() if len(k) <= 1))
    
    while(len(word) < length):
        # Get longest prefix
        for p in range(len(word) - maxpre if maxpre > 0 else 0, len(word)):
            prefix = word[p:]
            if prefix in pst:
                # Randomly choose next character
                keyvals = [(k, v) for k, v in pst[prefix].items()
                           if len(k) <= min(length - len(word),
                                           maxsuf if maxsuf > 0 else len(word))]
                vals = [v for k, v in keyvals]
                next = keyvals[weighted_choice(vals)][0]
                word += next
                break
    return word


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
    maxpre = 3
    maxsuf = 3
    
    if len(sys.argv) <= 1:
        print("[ERROR] Need text path.")
    else:
        filename = sys.argv[1]
        text = get_text_from_filename(filename)
        text = text.lower()
        text = "".join(filter(lambda x : x.isalpha() or x.isspace(), text))
        words = text.split()
        pst = presuftable(words)
        for i in range(nbwords):
            print(psrndword(pst, wordlen, maxpre, maxsuf))