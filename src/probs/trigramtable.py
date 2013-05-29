import random

def trigramtable(words):
    """
    Compute the set of trigrams (with number of occurrences) of words
    and return a list containing these numbers of occurrences.
    """
    tgt = {}
    for word in words:
        addtrigram(tgt, word)
    return tgt
        
        
def addtrigram(tgt, word):
    """
    Compute and store in tgt the set of trigrams of word.
    """
    for trigram in zip(word, word[1:], word[2:]):
        trigram = "".join(trigram)
        if trigram not in tgt:
            tgt[trigram] = 0
        tgt[trigram] += 1
    

def tgrndword(tgt, length):
    """
    Extract a random word of length from trigrams of tgt.
    length >= 3 !!!
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
    
    # First trigram
    word = random.choice(list(tgt.keys()))
    
    while(len(word) < length):
        # Get all possible trigrams and choose randomly (with weights of occ)
        trigrams = {k : v for k, v in tgt.items() if k[:2] == word[-2:]}
        # If no possibility, choose a new random trigram and take the last
        # letter
        if len(trigrams) <= 0:
            word = word + random.choice(list(tgt.keys()))[-1]
        else:
            word = word + random_item(trigrams)[-1]
    return word
    

def check_totality(tgt):
    """
    Check that the trigram table tgt is total, that is, for each trigram,
    there is another trigram strating with the two last letters of
    the previous one.
    """
    pass


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

    if len(sys.argv) <= 1:
        print("[ERROR] Need text path.")
    else:
        filename = sys.argv[1]
        text = get_text_from_filename(filename)
        text = text.lower()
        text = "".join(filter(lambda x : x.isalpha() or x.isspace(), text))
        words = text.split()
        tgt = trigramtable(words)
        for i in range(nbwords):
            print(tgrndword(tgt, wordlen))