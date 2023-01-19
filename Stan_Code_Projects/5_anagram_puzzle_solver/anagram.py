"""
File: anagram.py
Name: 蔡霖
----------------------------------
This program recursively finds all the anagram(s)
for the word input by user and terminates when the
input string matches the EXIT constant defined
at line 19

If you correctly implement this program, you should see the
number of anagrams for each word listed below:
    * arm -> 3 anagrams
    * contains -> 5 anagrams
    * stop -> 6 anagrams
    * tesla -> 10 anagrams
    * spear -> 12 anagrams
"""

import time                   # This file allows you to calculate the speed of your algorithm
from campy.gui.events.timer import pause

# Constants
FILE = 'dictionary.txt'       # This is the filename of an English dictionary
EXIT = '-1'                   # Controls when to stop the loop


def main():
    """
    print out the anagram of the input word in a list with a searching animation
    """
    print("Welcome to stanCode Anagram Generator(or -1 to quit)")
    while True:
        s = input("Find anagrams for: ").lower()
        if s == EXIT:
            break
        # Searching animation
        print("Searching", end="")
        pause(700)
        print(f" the anagram of", end="")
        pause(700)
        print(f" ({s})", end="")
        pause(700)
        print(". . . . ", end="")
        pause(700)
        print(". . . . ", end="")
        pause(700)
        print(". . . . ")
        pause(700)
        # Start calculation counting
        start = time.time()
        find_anagrams(s)
        end = time.time()
    print('----------------------------------')
    print(f'The speed of your anagram algorithm: {end-start} seconds.')


def read_dictionary(s, ch_counter):
    """
    :param s:
    :param ch_counter:
    :return:
    """
    lst = []
    with open(FILE, "r") as f:
        for line in f:
            if len(line.strip()) == len(s) and qty_cmp(ch_counter, line.strip()):
                lst.append(line.strip())
    return lst


def find_anagrams(s):
    """
    :param s:
    :return:
    """
    count_lst = [0]
    answer = []
    ch_counter = check_qty(s)
    w_lst = read_dictionary(s, ch_counter)
    find_anagrams_helper(s, ch_counter, "", answer, count_lst, w_lst)
    print("-" * 20, "Searching Completed!", "-" * 20)
    print(f"Found {count_lst[0]} anagrams by word ({s}): {answer}")


def find_anagrams_helper(s, ch_counter, curr_s, answer, count, w_lst):
    """
    :param s:
    :param ch_counter:
    :param curr_s:
    :param answer:
    :param count:
    :param w_lst:
    :return:
    """
    if len(curr_s) == len(s):
        print("Found: ", curr_s)
        print("Searching . . . . . . . . . . . . . . ")
        answer.append(curr_s)
        count[0] += 1
    else:
        for alpha in s:
            # Chose
            curr_s += alpha
            # Pruning
            # 1. Early stopping by comparing if current string (curr_s) characters qty exceed original string (s)
            # 2. Early stopping by checking if current string (curr_s) appear as answer before
            # 3. Early stopping by checking current sub_s in dictionary
            if curr_s not in answer and has_prefix(curr_s, w_lst):
                # print(curr_s) <- just for debug
                # Explore
                find_anagrams_helper(s, ch_counter, curr_s, answer, count, w_lst)
            # Un-chose
            curr_s = curr_s[:-1]


def has_prefix(sub_s, lst):
    """
    :param sub_s:
    :param lst:
    :return:
    """
    for word in lst:
        if word.startswith(sub_s):
            return True
    return False


def check_qty(s):
    """
    :param s:
    :return:
    """
    ch_counter = {}
    for ch in s:
        if ch in ch_counter:
            ch_counter[ch] += 1
        else:
            ch_counter[ch] = 1
    return ch_counter


def qty_cmp(ch_counter, dict_s):
    """
    :param ch_counter:
    :param dict_s:
    :return:
    """
    curr_counter = {}
    for ch in dict_s:
        if ch in curr_counter:
            curr_counter[ch] += 1
        else:
            curr_counter[ch] = 1
        if ch not in ch_counter:
            return False
        elif curr_counter[ch] > ch_counter[ch]:
            return False
    return True


if __name__ == '__main__':
    main()
