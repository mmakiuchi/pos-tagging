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
    for n in pos_freq:
        splits = n[0].split()
        freq = n[1] # frequency of the POS
        word = splits[0] # word
        if not prev_word == -1: # if not first line
            if word == prev_word:
                if freq > max_freq:
                    max_freq = freq
                    line = n
            else:
                pos_freq_list.append(line) # append previous line
                max_freq = freq
                line = n
        else:
            line = n
        prev_word = word
    pos_freq_list.append(line) # append the last line
    return(pos_freq_list)


# save the frequency of the pairs word/POS
def save_file(file_name, pos_list):
    with open(file_name, 'a') as f:
        for n in pos_list:
            f.write(str(n[0]) + ' ' + str(n[1]) + '\n')


# prepare the data for the POS tagging
def prepare_data(test_data):
    # get the list of words
    word_list = []
    gold_standard = []

    # transform all words in the file and get the correct POS
    for line in test_data:
        if line.strip(): # considers not empty lines
            strips = line.strip()
            word = strips[0] # get only the word
            pos = strips[1] # get the gold-standard pos
            lower_case = word.lower() # lower case
            word_list.append(lower_case) # save the transformed word to the list
            gold_standard.append(pos.lower()) # save in lower case for future comparison

    return(word_list, gold_standard)


def pos_tagging(word_list, tag_dict):
    pos_tags = [] # tags for each word in the file

    # make a list of pos tags
    for word in word_list:
        pos_tag = -1 # when the word was not found
        
        # search the word in the tag_dict
        for n in tag_dict:
            splits = n[0].split()
            pos_word = splits[0] # word in pos list
            pos_tag = splits[1] # get our pos prediction
            if word == pos_word:
                break # the word was found
        pos_tags.append(pos_tag)

    # return the POS tags
    return(pos_tags)

# compare with the gold standard
def compare_gold_standard(pos_tag, gold_standard):
    correct = 0
    wrong = 0

    for tag, gold_tag in zip(pos_tag, gold_standard):
        if(tag == gold_tag):
            correct += 1
        else:
            wrong += 1

    print('Correct: ', 100*correct/(correct + wrong))
    print('Wrong: ', 100*wrong/(correct + wrong))


if __name__ == "__main__":
    line_list = read_lines("train.txt")
    transformed_lines = transf_lines(line_list)

    # get frequency of each word/POS pair
    freq_list = get_frequency_list(transformed_lines)

    # remove the duplicates from the transformed lines
    line_list = list(dict.fromkeys(transformed_lines))

    # create a list with the frequency and the lines
    pos_freq = list(zip(line_list, freq_list))

    # order the list in alphabetic order
    pos_freq = sorted(pos_freq)

    # get the most frequent tag for each word
    pos_freq_list = get_most_frequent_pos(pos_freq)
    
    # save the most frequent POS tag for each word
    save_file("POS-freq.txt", pos_freq_list)

    # get the data to make the POS tagging
    test_data = read_lines("train.txt")

    # prepare the data for the pos tagging
    print('Preparing data for tagging')
    word_list, gold_standard = prepare_data(test_data)

    # get the POS tags after the tagging according to the baseline
    print('Making the POS tagging')
    tag_list = pos_tagging(word_list, pos_freq_list)

    # compare predictions with gold standard
    print('Compare results with the baseline')
    compare_gold_standard(tag_list, gold_standard)
    