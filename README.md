MePGen is a memorable password generator.

MePGen uses two techniques to generate memorable passwords. First, it uses a regular expression to define a password easily remembered. This regular expression is composed of words and separators, where words are composed of letters and separators of digits and punctuation.

Second, MePGen relies on a given text to produce prossible words. It is in fact much more easy to produce a memorable word (in contrast to any word, like 'xfgarrzl') when taking as examples real words instead of trying to design the correct regular expressions of (english) words.


# Usage
=======

```
usage: mepgen.py [-h] [-v] [-s SIZE] [-n COUNT] [-t TEXT] [-b THRESHOLD]
                 [-l MINLEN]

A memorable passwords generator

optional arguments:
  -h, --help    show this help message and exit
  -v            verbose mode

passwords related arguments:
  -s SIZE       size of the generated passwords (default: 16)
  -n COUNT      number of generated passwords (default: 10)

source text related arguments:
  -t TEXT       source text (default: None)
  -b THRESHOLD  threshold to keep characters from source file (default: 0.0)
  -l MINLEN     minimum length for text generated words (default: 4)
```

In addition to the common optional arguments `-h` and `-v` to get help and to activate verbose mode, respectively, MePGen comes with several arguments.

The "passwords related arguments" are related to the finally generated memorable passwords. `-s` specifies the size of the generated password(s) while `-n` defines the number of generated ones.

The "source text related arguments" are related to the text and the parameters to extract new words from this text. The `-t` argument provides the path to the text to use and the `-l` argument specifies the minimum size of the words generated to produce a password. Finally, the `-b` argument defines a threshold to ignore some possible words from the text.

In short, if the words composing the generated passwords (the subparts composed of letters) are not memorable enough, try to increase the `-b` argument. If MePGen says that no word can be generated, try to decrease it.

In more details, to produce a word, MePGen extracts, from the given text, the set of pairs *(c, d)* of characters such that *c* is followed by *d* in any word. In addition, it counts the number of each *(c, d)* in the text. With this set of pairs, it can produce a word such that every character *c* of the word is followed by a character *d* that originally follows *c* in the text. Furthermore, MePGen can also restrict the set of possible words by rejecting too short words.

In this context, it is also possible to reject some *(c, d)* pairs. If a pair is not sufficiently present in the original text, the `-l` parameter will reject it. In more detail, let *M* be the 2D matrix of characters successors such that *M[c][d]* is the number of times *d* follows *c* in the given text. Then if *d* does not follow *c* sufficiently often, i.e. if *M[c][d] < sum(M[c]) * b*, where *b* is the value of the `-b` argument, then *d* is discarded from the possible successors of *c* and no produced words will contain the substring *cd*.

For more information on how MePGen works and what is the underlying theory, see the NOTES.md file.


## Default values
-----------------

Each MePGen argument has a default value. By default, it generates 10 passwords of length 16. In the same way, the default threshold for discarding rare characters successors from the given text is 0; so, given a text, every pair *(c, d)* present in the words of the text are kept for the word generation.

Finally, the default text is `None`; in this case, as no word can be extracted from an empty text, MePGen uses an internal regular expression for words instead. This regular expression simply allows any word, i.e. any string of any length composed of letters. In this case, the generated passwords are no more memorable since they can be any string composed of letters, digits and punctuation.