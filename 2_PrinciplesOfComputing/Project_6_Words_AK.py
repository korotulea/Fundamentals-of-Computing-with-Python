"""
Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    list_final = []
    for list_new in list1:
        if list_new not in list_final:
            list_final.append(list_new)
    return list_final

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    list_final = []
    for list_new in remove_duplicates(list1):
        if list_new in list2:
            list_final.append(list_new)
    return list_final

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """   
    if len(list1) == 0 and len(list2) > 0:
        return list2
    if len(list2) == 0 and len(list1) > 0:
        return list1
    if len(list1) == 0 and len(list2) == 0:
        return []
    #if list1[0] == list2[0]:
     #   return list1[:1] + list2[:1] + merge(list1[1:], list2[1:])
    if list1[0] < list2[0]:
        return list1[:1] + merge(list1[1:], list2)
    else:
        return list2[:1] + merge(list1, list2[1:])
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) <= 1:
        return list1
    mid = len(list1)/2
    return merge(merge_sort(list1[:mid]), merge_sort(list1[mid:]))

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
#    1. Split the input word into two parts: the first character (first) 
#    and the remaining part (rest).
    #print word
    if len(word) == 0:
        return [""]
    
    first = word[0]
    rest = word[1:]
    
#    2. Use gen_all_strings to generate all appropriate strings for rest. 
#    Call this list rest_strings.
    rest_strings = gen_all_strings(rest)

#    3. For each string in rest_strings, generate new strings by inserting 
#    the initial character, first, in all possible positions within the string.
    first_all = []
    for strings_in_rest in rest_strings:
        len_rest = len(strings_in_rest)
        #print 'l_rest ', l_rest
        for position in range(len_rest+1):
            new_word = list(strings_in_rest)
            new_word.insert(position, first)
            #print 'position', position, 'new_word', new_word
            first_all.append(''.join(new_word)) 

#    4. Return a list containing the strings in rest_strings as well 
#    as the new strings generated in step 3.    
    
    return rest_strings + first_all #+ list(first)

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    word_list = []
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)
    for line in netfile.readlines():
        word_list.append(line)
    return word_list

def run():
    """
    Run game.
    """
    words = load_words('assets_scrabble_words3.txt')
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
#run()

#word = 'ab'
#print gen_all_strings(word)
#
#print merge(['a', 'b'], ['c', 'd'])
#print merge([1, 2, 3], [4, 5, 6])

#print gen_all_strings('a')
#print gen_all_strings('ab')

#print merge([3, 4, 5], [3, 4, 5]) 
#print merge([], []) 
#words = load_words('assets_scrabble_words3.txt')
#print words[:3]

#for i in range(10):
#    print words[i]
    
    
