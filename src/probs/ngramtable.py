import random

def ngramtable(words, n):
    """
    Compute the set of n-grams (with number of occurrences) of words
    and return a list containing these numbers of occurrences.
    n >= 1 !
    """
    tgt = {}
    for word in words:
        addngram(tgt, word, n)
    return tgt
        
        
def addngram(tgt, word, n):
    """
    Compute and store in tgt the set of n-grams of word.
    n >= 1 !
    """
    shifted = []
    for i in range(n):
        shifted.append(word[i:])
    for ngram in zip(*shifted):
        ngram = "".join(ngram)
        if ngram not in tgt:
            tgt[ngram] = 0
        tgt[ngram] += 1
    

def tgrndword(tgt, length):
    """
    Extract a random word of length from ngrams of tgt.
    tgt is an n-gram trable
    length >= n !
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
    
    # First ngram
    word = random.choice(list(tgt.keys()))
    
    while(len(word) < length):
        # Get all possible ngrams and choose randomly (with weights of occ)
        ngrams = {k : v for k, v in tgt.items() if k[:-1] == word[len(word)-len(k)+1:]}
        # If no possibility, choose a new random ngram and take the last
        # letter
        if len(ngrams) <= 0:
            word = word + random.choice(list(tgt.keys()))[-1]
        else:
            word = word + random_item(ngrams)[-1]
    return word
    

def check_totality(tgt):
    """
    Check that the ngram table tgt is total, that is, for each ngram,
    there is another ngram strating with the two last letters of
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
    wordlen = 5
    n = 3

    if len(sys.argv) <= 1:
        print("[ERROR] Need text path.")
    else:
        filename = sys.argv[1]
        text = get_text_from_filename(filename)
        text = text.lower()
        text = "".join(filter(lambda x : x.isalpha() or x.isspace(), text))
        words = text.split()
        tgt = ngramtable(words, n)
        for i in range(nbwords):
            print(tgrndword(tgt, wordlen))