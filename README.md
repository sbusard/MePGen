MePGen is a memorable password generator.

MePGen uses two techniques to generate memorable passwords. First, it uses a regular expression to define a password easily remembered. This regular expression is composed of words and separators, where words are composed of letters and separators of digits and punctuation.

Second, MePGen relies on a given text to produce prossible words. It is in fact much more easy to produce a memorable word (in contrast to any word, like `xfgarrzl`) when taking as examples real words instead of trying to design the correct regular expressions of (english) words.

MePGen is composed of two tools. First mepgen.py generates memorable passwords defined through a regular expression and a given successor table for words. Second, meptable.py generates successor tables from given texts.


# mepgen.py - Generating passwords

```
usage: mepgen.py [-h] [-v] [-s SIZE] [-n COUNT] [-t TABLE] [-b THRESHOLD]
                 [-l MINLEN]

Generate memorable passwords

optional arguments:
  -h, --help    show this help message and exit
  -v            verbose mode

passwords related arguments:
  -s SIZE       size of the generated passwords (default: 16)
  -n COUNT      number of generated passwords (default: 10)

source text related arguments:
  -t TABLE      successor table (default: None)
  -b THRESHOLD  threshold to keep characters from source file (default: 0.0)
  -l MINLEN     minimum length for text generated words (default: 4)
```

In addition to the common optional arguments `-h` and `-v` to get help and to activate verbose mode, respectively, mepgen.py comes with several arguments.

The "passwords related arguments" are related to the finally generated memorable passwords. `-s` specifies the size of the generated password(s) while `-n` defines the number of generated ones.

The "source text related arguments" are related to the successor table and the parameters to extract new words from this table. The `-t` argument provides the path to the table to use and the `-l` argument specifies the minimum size of the words generated to produce a password. Finally, the `-b` argument defines a threshold to ignore some possible words from the table.

In short, if the words composing the generated passwords (the subparts composed of letters) are not memorable enough, try to increase the `-b` and `-l` arguments. If MePGen says that no word can be generated, try to decrease `-b`.

In more details, to produce a word, MePGen uses the successor table. This table contains the set of pairs **(c, d)** of characters such that **c** is followed by **d** in any word of a given source text. In addition, it counts the number of each **(c, d)** in the text. With this set of pairs, it can produce a word such that every character **c** of the word is followed by a character **d** that originally follows **c** in the text. Furthermore, MePGen can also restrict the set of possible words by rejecting too short words.

In this context, it is also possible to reject some **(c, d)** pairs. If a pair is not sufficiently present in the successor table, the `-l` parameter will reject it. In more detail, let **M** be the successor table such that **M[c][d]** is the number of times **d** follows **c** in the given text. Then if **d** does not follow **c** sufficiently often, i.e. if **M[c][d] < sum(M[c]) * b**, where **b** is the value of the `-b` argument, then **d** is discarded from the possible successors of **c** and no produced words will contain the substring **cd**.

For more information on how MePGen works and what is the underlying theory, see the NOTES.md file.

Each MePGen argument has a default value. By default, it generates 10 passwords of length 16. In the same way, the default threshold for discarding rare characters successors from the given text is 0; so, given a successor table, every pair **(c, d)** present in the table is kept for the word generation.

Finally, the default successor table is `None`; in this case, as no word can be extracted from an empty table, MePGen uses an internal regular expression for words instead. This regular expression simply allows any word, i.e. any string of any length composed of letters. In this case, the generated passwords are no more memorable since they can be any string composed of letters, digits and punctuation.


# meptable.py - Generating successor table

```
usage: meptable.py [-h] [-v] [-b THRESHOLD] SOURCE DEST

Generate successor tables from texts

positional arguments:
  SOURCE        source text
  DEST          destination file

optional arguments:
  -h, --help    show this help message and exit
  -v            verbose mode
  -b THRESHOLD  threshold to keep characters from source file (default: 0.0)
```

meptable.py is used to extract, from a given text, the corresponding successor table. The `SOURCE` argument must be any text file and the `DEST` argument is the path to the newly created table. Note that any already created `DEST` file will be automatically and silently overwritten. The `-b` argument, specifying the threshold for the generated table, has exactly the same utility as explained above. You can thus either create a table with already filtered rare successors, or let mepgen.py deal with that and filter nothing; you can even specify a threshold when generating the table and when generating passwords.

Note that meptable.py only cares about words in the given text. A filter is applied on all characters of the text such that words are composed of letters (characters recognized as letters by Python) and separated by everything else. Your text can simply be a list of words.

Finally, generated tables are not intended to be human-readable. They are the result of pickling the corresponding matrix from Python. Any change to the table will cause mepgen.py to crash.