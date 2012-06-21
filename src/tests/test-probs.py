from mepgen.regex.regex import *
from mepgen.regex.transformation import regex_to_automaton
from mepgen.automaton.transformation import remove_lambdas, determinize, automaton_to_wordtree
from mepgen.wordtree.transformation import remove_empty_subtrees
from mepgen.automaton.automaton import Automaton
from mepgen.automaton.state import State, LAMBDA


# >s0   -a,c>   s1  -a>     s2
#       -b>     s3  -a,b>   (s4)
#       -d>     s5  -d>     (s6)

s0,s1,s2,s3,s4,s5,s6 = State(),State(),State(),State(),State(),State(),State()

s0.add_successor('a', s1)
s0.add_successor('c', s1)
s0.add_successor('b', s3)
s0.add_successor('d', s5)

s1.add_successor('a', s2)

s3.add_successor('a', s4)
s3.add_successor('b', s4)

s5.add_successor('d', s6)


aut = Automaton(s0, set([s4,s6]))
aut = determinize(remove_lambdas(aut))

wt = automaton_to_wordtree(aut, 2)
#wt = remove_empty_subtrees(wt)

#   >s0 -a,c>   s1  -a>     (s2)
#   4           1           1
#       a:1/4       a:1
#       c:1/4
#       -b>     s3  -a,b>   (s4)
#               2           1
#       b:1/2       a:1/2
#                   b:1/2

# aa -> 1/4
# ca -> 1/4
# ba -> 1/4
# bb -> 1/4


# Other example

#   >s0 -a,c>   s1  -a>     (s2)
#   5           1           1
#       a:1/5       a:1
#       c:1/5
#       -b>     s3  -a,b>   (s4)
#               2           1
#       b:2/5       a:1/2
#                   b:1/2
#       -d>     s5  -d>     (s6)
#               1           1
#       d:1/5       d:1

# aa -> 1/5
# ca -> 1/5
# ba -> 1/5
# bb -> 1/5
# dd -> 1/5


words = {}
for i in range(1000000):
    word = wt.randomrun()
    if word not in words:
        words[word] = 0
    words[word] += 1
    
    if i % 1000 == 0:
        print(words)
print(words)