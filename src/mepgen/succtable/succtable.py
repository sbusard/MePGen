import collections
import random

class SuccTable(collections.MutableMapping):
    """
    A successor table is a dictionary where keys are characters and values
    are dictionaries where keys are also characters and values are integers.
    A SuccTable represents a table of successors for characters.
    For any characters a and b, the higher SuccTable[a][b], the more probable
    a is followed by b; if SuccTable[a][b] does not exists, a is never
    followed by b.
    In addition to standard dictionary features, a SuccTable has also
    methods to perform operations particular to successors tables:
    getting a random word, checking totality of the table, etc.
    
    See http://stackoverflow.com/a/3387975/1714590 regarding
    the implementation of dictionary-related methods.
    """

    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs)) # use the free update to set keys

    def __getitem__(self, key):
        return self.store[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self.store[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self.store[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __keytransform__(self, key):
        return key
        
    
    def check_totality(self):
        """
        Returns whether every character of this SuccTable has at least one
        successor. That is, it is always possible to build an infinite word,
        whatever the first character is.
        
        """
        characters = set()
        for k, chars in self.items():
            characters.add(k)
            for char in chars.keys():
                characters.add(char)
        for char in characters:
            if char not in self.keys():
                return False
        return True


    def randomword(self, length):
        """
        Return a random word of length, composed of characters of this
        SuccTable, where weights of this table are used to weight
        probabilities of next character.
        
        """
        
        def weighted_choice(weights):
            """
            Return a random index of weights, with probability weighted
            by the values of weight.
            
            """
            rnd = random.random() * sum(weights)
            for i, w in enumerate(weights):
                rnd -= w
                if rnd < 0:
                    return i
            
        word = random.choice(list(self.keys()))
        for i in range(length - 1):
            keyvals = [(k, v) for k, v in self[word[-1]].items()]
            vals = [v for k, v in keyvals]
            letter = keyvals[weighted_choice(vals)][0]
            word += letter
        return word
        

import sys
import pickle
import os
if __name__ == "__main__":
    length = 10
    wordcount = 10

    if len(sys.argv) <= 1:
        print("[ERROR] Need table path.")
    else:
        table_path = sys.argv[1]
        table = pickle.load(open(table_path, "br"))
        print("Table", os.path.basename(table_path),
              "is" + ("" if table.check_totality() else " not"), "total.")
        for i in range(wordcount):
            print(table.randomword(length))