from .wordtree import Wordtree

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
    