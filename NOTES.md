This document explains the theoretical concepts used by MePGen. It explains the main assumption of MePGen - that memorable passwords can be defined with a regular expression, and how we can generate a random word from such a regex. It also goes further by showing how to provide more memorable words based on a given text and describes the final solution of MePGen.


# Memorable passwords as a regular expression

MePGen is based on the assumption that a memorable password can be defined using a regular expression. Being the full set of possible passwords, a regex defines a subset of these possible words; the ones that are human memorable.

For example, we could define the set of memorable passwords as the words accepted by the following regular expression (written as a grammar)
```
PSWD := WORD (SEPA WORD)*
WORD := cons vowe (cons vowe)*
SEPA := digi | punc
```
where `cons` and `vowe` define the sets of consonants and the set of vowels, respectively, and `digi` and `punc` are the sets of digits and punctuation marks, respectively. Here, we define a memorable password as a list of words separated by separators, where words are lists of consonant-vowel couples and separators are digits or punctuation marks.

This example is here to illustrate the concept, but MePGen uses a slightly different regex to generate its passwords.


## From regular expressions to random words

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

A potential concern about wordtrees is the following: when unfolding an automaton, some subtrees of the corresponding wordtree can accept no word, in the case where some leaves do not accept any word. The resulting wordtree thus contains some useless parts since they can not produce any word. This is in fact not a big concern since the choice among possible successors is weighted by the number of possible words produced by these successors, the empty subtrees will never be chosen. It is however possible to remove empty subtrees, resulting into an equivalent, smaller wordtree.


# Defining a memorable word with a regex is not easy

The regular expression given above gives an example of possible regex for memorable passwords. However, this regex seems a bit too restrictive since it can not generate passwords like `shetro4biggar`, while it is obviously memorable. The regex could be modified to replace the `WORD` rule with, for example,
```
WORD := SYLL SYLL*
SYLL := cons cons vowe | cons vowe | cons vowe cons | vowe cons cons | vowe cons
```
but such a regex would be to permissive since it accepts `txarvnfo2acrnxa`, that seems not very memorable.
In fact, a memorable word - not a full password but just a word - seems difficult to describe with a regular expression, contradicting with the main assumption of MePGen.


## From text to automaton

To tackle this problem of describing a memorable word with a regular expression, we can take advantages of existing natural languages texts like dictionaries, books, etc.

The assumption here is that if character **c** is often followed by character **i** in natural languages texts, then **c** should be followed by **i** in a memorable randomly generated word. Using this idea, is then possible from the words **dictionary** and **beautiful** to generate the memorable word **dictiful**.

As we have a way to extract a random word from a given automaton, we have to find a way to get an automaton from a given text; we call this text the *source text*. The way MePGen does it is by getting, from the given text, for each character **c** of the text, the set of possible next characters, i.e. the set of characters that follow **c** in any word of the text. We store this information into a 2D matrix where the *i*th element of the **j**th row stores the number of time that **i**th character follows  **j**th character.

From this matrix we can build an automaton that recognizes any word **w** composed of characters of the matrix such that **w** starts with any character and for every pair of successive characters **c** and **d** of **w**, the **(c, d)** entry of the matrix is not zero, i.e. **d** follows **c** at least one time in the source text. To build this automaton, we construct one state by character **c** of the alphabet representing the state we reach when we traverse a transition labelled with **c**, and one special initial state. From the initial state, we can reach all the other states in one step, through the corresponding transition. Furthermore, from any state of character **c**, we can traverse a transition to state of character **d** (thus the transition is labelled with **d**) if and only if the **(c, d)** entry of the matrix is not zero.

The result is then, from a given source text, we produce an automaton that accepts any word of any length that is composed of characters of the source text and such that any character of the word is followed by a character that follows it in a word of the source text.


## Integrating an automaton into a regex


## Customizing the resulting language


### Rejecting short words


### Threshold mechanism

% Explain the mechanism

% Discuss adequateness of threshold mechanism


# MePGen solution


## Advantages

% no reduction of the word space
%   describe the problem
%   show that is no more a problem when using texts
%       in appearance
%       do not disclose your text
% a password in your language
%   quid digits and punctuation?

