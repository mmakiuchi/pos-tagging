"""
    Name: pos_helpers.py

    Function: Helper functions for the pos_baseline.py
    script. The functions presented here are used to read/save
    text files and manipulate/transform the textual data.
    
    Date: October 12, 2019
    Author: Mariana Makiuchi
"""

# to use regular expressions
import re

# read the lines from a text file
def read_lines(file_name):
    with open(file_name) as f:
        lines = f.readlines()
    return lines

# transform all lines to remove chunk tags and make them lower case
def transf_lines(original_lines):
    line_list = []
    for line in original_lines:
        if line.strip(): # considers not empty lines
            new_line = re.sub(r' [\w-]+\n',' ', line) # remove the last column (the chunk tags)
            lower_line = new_line.lower() # lower case
            line_list.append(lower_line) # save the transformed line to the list
    
    # order the list
    line_list = sorted(line_list)
    
    return(line_list)

# get the frequencies for each pair of word-POS
def get_frequency_list(line_list):
    freq = 1
    prev_line = -1
    freq_list = []

    # count the frequency of each line
    for line in line_list:
        if not prev_line == -1: # if not first line
            if line == prev_line:
                freq += 1
            else:
                freq_list.append(freq)
                freq = 1
        prev_line = line
    freq_list.append(freq) # append the frequency of the last word
    
    return(freq_list)

# delete the less frequent ocurrences of a POS for each word
def get_most_frequent_pos(pos_freq):
    prev_word = -1
    max_freq = 0
    pos_freq_list = []
    word_list = []
    pos_list = []
    for n in pos_freq:
        splits = n[0].split()
        freq = n[1] # frequency of the POS
        word = splits[0] # word
        pos = splits[1] # pos
        if not prev_word == -1: # if not first line
            if word == prev_word:
                if freq > max_freq:
                    max_freq = freq
                    line = n
            else:
                pos_freq_list.append(line) # append previous line
                word_list.append(word)
                pos_list.append(pos)
                max_freq = freq
                line = n
        else:
            line = n
        prev_word = word

    pos_freq_list.append(line) # append the last line
    word_list.append(word)
    pos_list.append(pos)
    pos_dict = dict(zip(word_list, pos_list))

    return(pos_freq_list, pos_dict)


# save the frequency of the pairs word/POS
def save_file(file_name, pos_list):
    with open(file_name, 'w') as f:
        for n in pos_list:
            f.write(str(n[0]) + ' ' + str(n[1]) + '\n')


# prepare the data for the POS tagging
def prepare_data(test_data):
    # get the list of words
    word_list = []
    gold_standard = []

    # transform all words in the file and get the golden POS
    for line in test_data:
        if line.strip(): # considers not empty lines
            splits = line.split()
            word = splits[0] # get only the word
            pos = splits[1] # get the gold-standard pos
            lower_case = word.lower() # lower case
            word_list.append(lower_case) # save the transformed word to the list
            gold_standard.append(pos.lower()) # save in lower case for future comparison

    return(word_list, gold_standard)