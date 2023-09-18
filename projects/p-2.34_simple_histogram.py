"""
P-2.34: Write a Python program that inputs a document and then outputs a bar-chart plot of the
frequencies of each alphabet character that appears in that document.

Do we treat each upper and lower case a separate frequency or together? 
It would simplify and make it easier to count the occurences if we just consider upper and lower case characters to be the same when printing out the list count.
"""

import os
filepath = os.path.join(os.path.dirname(__file__), 'input\\wizoz10.txt')
letter_freq = {} # use this data structure to count the number of characters
MAX_WIDTH = 20 # maximum number of width-wise characters the console can print
# Helper function
def is_valid_character(char):
    """Check if the character is an upper or lowercase letter."""
    return ord('a') <= ord(char) <= ord('z') or ord('A') <= ord(char) <= ord('Z')

# open the file and lazily read in each line just in case we have a very large file and we don't want to place it all in memory at once
# then for each line, we parse each character in the string (since it's an iterable) and do something with it, in this case count how many occurences
with open(filepath, 'r') as file:
    for line in file:
        for char in line:
            lower_char = char.lower() # for the sake of simplicity we will count upper and lower case characters the same
            if is_valid_character(lower_char):
                 # assign the current count then increment if the key exists, otherwise assign it to 0 then increment
                letter_freq[lower_char] = letter_freq.get(lower_char, 0) + 1

# print out the results
for i in range(len(letter_freq)):
    char_idx = chr(i + ord('a')) # calculate the current character to be printed
    print("{character}: {frequency_count}".format(character=char_idx, frequency_count='*' * int(letter_freq.get(char_idx) / MAX_WIDTH)))