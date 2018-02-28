#!/usr/env python

# https://github.com/dwyl/english-words
# https://forums.macrumors.com/threads/dictionary-files-in-macos-high-sierra-10-13.2079925/
# https://reverseengineering.stackexchange.com/questions/9426/how-to-read-nscr1000-data-files
# https://www.collinsdictionary.com/sitemap.xml

import re

NO_OCCURENCE = -1

def get_first_occurence_index(word, letter, ignore_index):
    for i, l in enumerate(word):
        if i == ignore_index:
            break
        if letter == l:
            return i
    return NO_OCCURENCE

# returns a regex to match words based on the letters provided in a(lphabet)
def get_regex_for_word(word, a):
    ret = word[:]

    for n, l in enumerate(word):
        if l in a.values():
            ret[n] = "({})".format(ret[n])
            continue

        if l in a.keys():
            # temptative letter already found
            ret[n] = '({})'.format(a[l])
        else:
            # check if already in word
            occurence_index = get_first_occurence_index(word, l, n)
            if occurence_index != NO_OCCURENCE:
                # replace with \#
                ret[n] = '(\\{})'.format(occurence_index + 1)
            else:
                if n == 0:
                    ret[n] = '(.)'
                else:
                    ret[n] = '((?!{}).)'.format('|'.join(['\{}'.format(x) for x in xrange(1, n+1)]))
    return "^{}$".format("".join(ret))

def get_words_matching_regex(dictionary, regex_string, word_length):
    r = re.compile(regex_string, re.IGNORECASE)
    return filter(r.match, dictionary[word_length])

def get_words_matching_word_list(word_num_list, dictionary, alphabet):
    return get_words_matching_regex(dictionary, get_regex_for_word(word_num_list, alphabet), len(word_num_list))

def get_entropy_level(word_num_list, dictionary, alphabet):
    e = len(get_words_matching_word_list(word_num_list, dictionary, alphabet))
    if not e:
        raise ValueError('No words possible for {}'.format(word_num_list))
    return e

def order_by_entropy(words, dictionary, alphabet):
    return sorted(words, key=lambda x: get_entropy_level(x, dictionary, alphabet))

def get_alphabet_dict_from_word(word_num_list, word):
    return { word_num_list[i] : word[i] for i in xrange(0, len(word_num_list)) }

def merge_two_dicts_w_o_clash(d1, d2):
    d3 = d1.copy()
    for k1, v1 in d1.items():
        for k2, v2 in d2.items():
            if ((k1 == k2 and v1.lower() != v2.lower())
                or (k1 != k2 and v1 == v2)):
                raise ValueError('Clashing dictionaries: {} ---- {}'.format(d1, d2))
            d3[k2] = v2
    return d3

def solver(dictionary, words, alphabet=dict()):
    # no more unknown words... Mission accomplished!
    if not words:
        return alphabet

    print 'Ordering by entropy: ({} words left)'.format(len(words))

    try:
        # sort the words from lowest to highest entropy
        s_words = order_by_entropy(words, dictionary, alphabet)
    except ValueError as e: 
        # Used to reduce entropy calculations time
        print e
        return {}
    else:
        # take the first word from the list and find all possible words
        c_word = s_words.pop(0)
        c_word_matches = get_words_matching_word_list(c_word, dictionary, alphabet)
        count_f_words = len(c_word_matches)
        for i, f_word in enumerate(c_word_matches):
            # add all the letters to the temp_alphabet
            temp_alphabet = get_alphabet_dict_from_word(c_word, f_word)

            # Using try - except to check for clash and merge at the same time
            try:
                m_dict = merge_two_dicts_w_o_clash(temp_alphabet, alphabet)
            except Exception as e:
                # if dicts have clashing pairs
                # they are invalid so go to next word
                print e
                continue
            else:
                print "{}/{}. {}".format(i+1, count_f_words, m_dict)
                new_alpha = solver(dictionary, s_words, m_dict)

            if new_alpha:
                return new_alpha

        return {} # second base case : no words match the alphabet/dictionary

def word_list_to_word_length_dict(d):
    ret = dict()
    for word in d:
        l_w = len(str(word))
        if l_w in ret:
            ret[l_w] += [str(word)]
        else:
            ret[l_w] = [str(word)]
    return ret

def main():
    words = [
        # horizontal words
        [17, 10, 8, 18, 17],
        [17, 12, 19, 5, 11],
        [12, 2, 15, 7, 20, 21, 9],
        [7, 8, 25, 5, 20, 15, 17],
        [20, 6, 20, 18, 19, 25, 12],
        [15, 8, 17, 20],
        [5, 2, 18, 17],
        [3, 19, 25, 22, 2],
        [9, 2, 1],
        [7, 19, 9],
        [19, 5, 5, 2, 6, 19, 4, 20, 17],
        [3, 2, 3],
        [8, 25, 25],
        [17, 19, 6, 17, 19],
        [19, 24, 6, 20],
        [20, 19, 12, 17],
        [3, 8, 17, 20, 5, 12, 17],
        [19, 5, 5, 2, 1, 25, 12],
        [15, 20, 10, 2, 1, 25, 4],
        [23, 20, 15, 17, 20],
        [11, 25, 8, 12, 17],

        # vertical words
        [17, 12, 19, 15],
        [19, 18, 19, 15],
        [8, 5, 9],
        [3, 2, 24],
        [10, 2, 15, 11, 17],
        [6, 1, 5, 15, 20],
        [20, 13, 1, 19, 3, 6, 20],
        [18, 14, 20, 20],
        [3, 1, 25, 17],
        [21, 6, 19, 3],
        [17, 11, 8, 25],
        [4, 9, 20],
        [19, 15, 2, 26, 19],
        [17, 12, 9],
        [18, 1, 25],
        [6, 8, 20],
        [17, 7, 19],
        [22, 20, 19, 25, 17],
        [5, 15, 9],
        [8, 25, 12, 2],
        [19, 25, 12, 20],
        [12, 8, 25, 12],
        [17, 10, 19, 25],
        [5, 19, 7, 17, 8, 16, 20],
        [19, 4, 1, 6, 12],
        [18, 1, 9],
        [25, 1, 12],
        [19, 17, 11, 17],
        [17, 1, 4, 17]
    ]

    dict_path = './combined.txt'

    with open(dict_path) as f:
        d = f.read().split('\n')

    # order the dictionary by word length to increase solving speed
    d = word_list_to_word_length_dict(d)

    print "FINAL ALPHABET:\n{}".format(solver(d, words))

if __name__ == '__main__':
    main()