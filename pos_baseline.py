"""
    Name: pos_baseline.py

    Function: Apply the baseline code for POS tagging
    to the conll2000 text files available at:
    https://www.clips.uantwerpen.be/conll2000/chunking/
    
    Date: October 12, 2019
    Author: Mariana Makiuchi
"""

# helper functions
import pos_helpers as helper

# to generate random intervals for cross-validation
import random

# file names
file_name = "train.txt"
# freq_pos_file_name = "POStags.txt" # output file with most frequent POS

# applies the baseline POS tagging
def pos_tagging(word_list, tag_dict):
    pos_tags = [] # tags for each word in the file
    
    # make a list of pos tags
    for word in word_list:
        # search the word in the tag_dict
        if word in tag_dict.keys():
            pos_tag = tag_dict[word] # get our POS prediction
        else:
            pos_tag = -1 # when the word was not found
        
        pos_tags.append(pos_tag)

    # return the predicted POS tags
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

    print('Accuracy: ', float("{0:.2f}".format(100*correct/(correct + wrong))), "%")

    return(correct/(correct + wrong))


if __name__ == "__main__":
    # k-fold cross validation
    k = 10

    # read the file
    line_list = helper.read_lines(file_name)
    num_lines = len(line_list)

    random.seed()
    cross_val_acc = 0

    for i in range(k):
        print('Trial ', i+1)

        # the test partition will be 20% of the total file
        test_start = random.randint(0, (num_lines - (num_lines // 5)) )
        test_end = test_start + num_lines // 5

        # separate train and test partitions
        train_part = line_list[0:test_start] + line_list[test_end:]
        test_part = line_list[test_start:test_end]

        # transform the train lines
        train_lines = helper.transf_lines(train_part)

        # get frequency of each word/POS pair
        freq_list = helper.get_frequency_list(train_lines)

        # remove the duplicates from the train partition
        train_list = list(dict.fromkeys(train_lines))

        # create a list with the frequency and the lines
        pos_freq = list(zip(train_list, freq_list))

        # order the list in alphabetic order
        pos_freq = sorted(pos_freq)

        # get the most frequent tag for each word
        pos_freq_list, pos_dict = helper.get_most_frequent_pos(pos_freq)

        # prepare the data for the pos tagging
        test_word_list, gold_standard = helper.prepare_data(test_part)

        # get the POS tags after the tagging according to the baseline
        pos_tags = pos_tagging(test_word_list, pos_dict)

        # compare the prediction to the gold standard
        accuracy = compare_gold_standard(pos_tags, gold_standard)

        cross_val_acc += accuracy

    cross_val_acc = cross_val_acc/k
    print(k,'-fold cross-validation accuracy: ', float("{0:.2f}".format(100*cross_val_acc)), '%')