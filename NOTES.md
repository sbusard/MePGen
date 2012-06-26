This document explains the theoretical concepts used by MePGen. It explains the main assumption of MePGen - that memorable passwords can be defined with a regular expression, and how we can generate a random word from such a regex. It also goes further by showing how to provide more memorable words based on a given text and describes the final solution of MePGen. Finally, it speaks about the reduction of the word space induced by the restrictions to memorable passwords and why this is not a concern anymore thanks to text-based words.


# Main assumption: memorable passwords can be defined with a regular expression

MePGen is based on the assumption that a memorable password can be defined using a regular expression. Being the full set of possible passwords, a regex defines a subset of these possible words; the ones that are human memorable.

For example, we could define the set of memorable passwords as the words accepted by the following regular expression (written as a grammar)
```
PSWD := WORD (SEPA WORD)*
WORD := cons vowe (cons vowe)*
SEPA := digi | punc
```
where `cons` and `vowe` define the sets of consonants and the set of vowels, respectively, and digi and punc are the sets of digits and punctuation marks, respectively. Here, we define a memorable password as a list of words separated by separators, where words are lists of consonant-vowel couples and separators are digits or punctuation marks.

This example is here to illustrate the concept, but MePGen uses a slightly different regex to generate its passwords.


# From regular expressions to random words

Given a regular expression accepting a set of variable-length words, we have to produce a word of a given length. Furthermore, to avoid a bias, the produced word has to be chosen uniformly randomly among the possible words.

Since we fix the length of the produced word, it is possible to compute the number of such words and to choose one randomly, with uniform probability of choice.

To achieve this uniformly random choice, the regular expression defining the possible words is first transformed into a finite automaton. A transformation from a regex to an automaton is possible such that a word is accepted by the automaton if and only if it is accepted by the regex.

We have then an automaton accepting the possible variable-length words. From this automaton we can extract a tree, that we call a *wordtree*, by unfolding the automaton from its initial state, upto a given length **l**. By setting the leaves of this tree as accepting only if the corresponding automaton state is accepting, we get a tree that accepts all words of length **l** accepted by the original automaton.

Finally, from this tree, it is possible to produce a random word, accepted by the tree, with a uniform probability. First, for each state of the tree, we can compute the set of words that can be accepted by the state: if the state is a leaf, it accepts one word, if it is accepting, or none otherwise; if it is not a leaf, for each of its successors, if the successor accepts **n** words, then the current state accepts **n * c** words, where **c** is the number of possible characters leading to this successor.

When the number of accepted words is computed for each state of the *wordtree*, it is possible to produce a uniformly random accepted word by weighting each transition with the number of possible words of the successors.

We have shown here how to produce, from a given regex, a random word of a given length accepted by the regex. 


## Lambda-free deterministic automata

The transformation from an automaton to a wordtree is not correct in general. In fact, there are two concerns.

First, if the given automaton contains some lambda transitions, i.e. transitions that consume no character, the wordtree corresponding to an unfolding of the automaton upto a given length will not accept only words of the given length, since a transition does not mean a character anymore. To tackle this problem, the automaton has to be transformed into an equivalent lambda-free automaton.

Second, if the given automaton is not deterministic, it is possible to produce the same word by two different paths in the corresponding wordtree, leading to a bias in the probability of producing a given word. To tackle this problem, the automaton produced by the regex has to be determinized before unfolding it into a wordtree.

Finally, note that the two necessary transformations - removing empty transitions and determinizing the automaton - are possible for any automaton. There is so no further limitation in the approach.


## Empty subtrees of wordtrees

A concern about wordtrees is the following: when unfolding an automaton, some subtrees of the corresponding wordtree can accept no word, in the case where some leaves do not accept any word. The resulting wordtree thus contains some useless parts since they can not produce any word. This is in fact not a concern since the choice among possible successors is weighted by the number of possible words produced by these successors, the empty subtrees will never be chosen. It is however possible to remove empty subtrees, resulting into an equivalent, smaller wordtree.


# Problem: it is not easy to define a memorable word with a regex
# From text to automaton
# Final solution
# Reduction of the word space and Using texts tackle the problem of reduced words space