*letterless-xword-solver*
____

Python program used to solve crossword puzzles where there are no definitions and the letter squares have a number representing a letter.

Example
____
![Letterless xword example](<to add>)
![Solution alphabet](<to add>)

Limitations and Breaking points
___
- The `combined.txt` file contains the list of "words" used. It is possible that the words used in the crossword are not part of the `combined.txt` list and therefore won't find any solution to a possibly valid crossword.
- The program assumes that two unique numbers can't represent the same letter
- The list of "words" only contains english words
- and more...

Credits
___
The `combined.txt` words list is a combination of [dwyl/english-words](https://github.com/dwyl/english-words) and `/usr/share/dict/words`
