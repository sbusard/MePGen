This document explains the theoretical concepts used by MePGen. It explains the main assumption of MePGen - that memorable passwords can be defined with a regular expression, and how we can generate a random word from such a regex. It also goes further by showing how to provide more memorable words based on a given text and describes the final solution of MePGen.

This document assumes familiarities with regular expressions, regular languages and finite word automata.


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

The assumption here is that if character **c** is often followed by character **i** in natural languages texts, then **c** should be followed by **i** in a memorable randomly generated word. Using this idea, is then possible from the words `dictionary` and `beautiful` to generate the memorable word `dictiful`.

As we have a way to extract a random word from a given automaton, we have to find a way to get an automaton from a given text; we call this text the *source text*. The way MePGen does it is by getting, from the given text, for each character **c** of the text, the set of possible next characters, i.e. the set of characters that follow **c** in any word of the text. We store this information into a 2D matrix where the **i** th element of the **j** th row stores the number of time that **i** th character follows  **j** th character.

From this matrix we can build an automaton that recognizes any word **w** composed of characters of the matrix such that **w** starts with any character and for every pair of successive characters **c** and **d** of **w**, the **(c, d)** entry of the matrix is not zero, i.e. **d** follows **c** at least one time in the source text. To build this automaton, we construct one state by character **c** of the alphabet representing the state we reach when we traverse a transition labelled with **c**, and one special initial state. From the initial state, we can reach all the other states in one step, through the corresponding transition. Furthermore, from any state of character **c**, we can traverse a transition to state of character **d** (thus the transition is labelled with **d**) if and only if the **(c, d)** entry of the matrix is not zero.

The result is then, from a given source text, we produce an automaton that accepts any word of any length that is composed of characters of the source text and such that any character of the word is followed by a character that follows it in a word of the source text.


## Integrating an automaton into a regular expression

Having an automaton accepting any memorable word is not sufficient since we want memorable passwords that are composed of words, but also of digits and punctuation marks. It is necessary to integrate such an automaton into a bigger one that can generate memorable passwords. To achieve this, we can integrate it as an element of a regular expression. Since regular expressions are then transformed into automata, the transformation is already done with these special regex.

Finally, note that the automaton could be transformed into a regular expression, but since this regex would then be transformed back to an automaton to build the corresponding wordtree, it is completely useless.


## Customizing the resulting language

Extracting an automaton from a given source text as explained above is not always satisfactory.

First, the automaton accepts words of any length. The final result, when integrating this automaton into a regex and producing words of this regex, then produces passwords composed of possibly empty words, leading to words not memorable anymore. For example, we can take the regular expression of memorable words given at the beginning of this document, where `WORD` is replaced by the automaton corresponding to a given source text. With this language, as a `WORD` can have any length, it can produces the word `563()!40weca32!` where a lot of separators can follow each others. To tackle this problem, it is possible to restrict the automaton to words of a given minimal length.

Second, while `x` is sometimes followed by `f` in some english words, this does not constitute sufficient habits to consider these two characters as successors. Some experiments with source text-based word generation showed that it is useful to consider only characters that are often successors. For example, if `x` is followed three times by `f` in a given text but followed 25 times by `e`, we can discard `f` and only keep `e`. This is achieved in MePGen by applying, on the matrix of a given source text, a threshold to remove rare successors.


### Rejecting short words

To restrict an automaton to words of a given minimal length **l**, we can unfold the automaton **l** times from the initial state. This means that we create a copy of the initial state, constituting the current-level states set, and, **l** times, we create a copy of all successors of the states of the current-level states set, add the corresponding transition, and set the current-level states set as the set of the copies of these successors. Finally, all the lastly created states have transitions to the corresponding original successors.

Using this mechanism, we can build a new automaton **A'** from an automaton **A** and a bound **l** such that **A'** accepts all words accepted by **A** that are at least **l** characters long.

Thanks this mechanism, we can introduce, into a regular expression, words that have a minimal given length.


### Threshold mechanism

As explained above, if we keep every successing pairs in words of a given source text, this may lead to rare cases that are not very memorable. This is due to the fact that, from the matrix of successors, we consider all possible next characters equally while in the text, some of them are really rarer than others.

To tackle this problem, we can, given a threshold, remove all possible next characters that do not occur sufficiently often, compared to the threshold. In more details, given a matrix **m** storing, for each pair **(c, d)** the number of times **c** is followed by **d** in a given source text, and given a threshold **t**, the threshold mechanism of MePGen removes, for each characters **c**, all the characters **d** such that **m[c][d] < sum(m[c]) * threshold**. For example, let **c** have three possible successors **d1**, **d2** and **d3** in the source text, such that **m[c][d1] = 4**, **m[c][d2] = 5** and **m[c][d3] = 1**, meaning that **d1** follows **c** four times in the source text, **d2** five times and **d3** only one time. If we apply a threshold of O.2, only **d1** and **d2** will be kept, by **d3** will be discarded.

Using this mechanism, we can keep only successors that occur sufficiently often in the source text and discard the successors that are too rare.


# MePGen solution


## Advantages

% no reduction of the word space
%   describe the problem
%   show that is no more a problem when using texts
%       in appearance
%       do not disclose your text
% a password in your language
%   quid digits and punctuation?

