# *Codeword // letterless-xword-solver*
____

Python program used to solve codeword puzzles where there are no definitions and the letter squares have a number representing a letter.


> A codeword puzzle complete crossword grid where each letter of the alphabet is substituted for a number (usually 1-26). There is a minimum one occurrence of each letter of the alphabet.

To play codewords: https://simplydailypuzzles.com/daily-codeword/

## Usage

1. Replace the words array in the main function of solve-xword.py with your own grid (each entry being one of the words in the puzzle)
2. run `python solve-xword.py`
3. The alphabet will be printed and you can use it to fill in your codeword

## Limitations and Breaking points
___
- The `combined.txt` file contains the list of "words" used. It is possible that the words used in the crossword are not part of the `combined.txt` list and therefore won't find any solution to a possibly valid crossword.
- The program assumes that two unique numbers can't represent the same letter
- The list of "words" only contains english words
- Code is not optimal but should find a solution in only a few seconds

## Credits
___
The `combined.txt` words list is a combination of [dwyl/english-words](https://github.com/dwyl/english-words) and `/usr/share/dict/words`
