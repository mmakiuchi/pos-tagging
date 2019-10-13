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
train_file_name = "train.txt"
test_file_name = "test.txt"
freq_pos_file_name = "POStags.txt" # output file with most frequent POS

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


# performs the cross validation on a given partition
def cross_validation(word_partition, pos_dict, gold_partition):

    # send the word partition to be POS tagged
    pos_tags = pos_tagging(word_partition, pos_dict)

    # compare the prediction to the gold standard
    accuracy = compare_gold_standard(pos_tags, gold_partition)

    return(accuracy)

# generates 10 random partitions and perform the cross validation
def ten_fold_cross_val(word_list, pos_dict, gold_standard):
    
    cross_val_acc = 0 
    random.seed()
    max_size = len(word_list)
    print('Number of words is:', max_size)
    print('Each partition will have size: ', max_size // 10)

    for i in range(10):
        print('Trial ', i+1)
        part_start = random.randint(0, (max_size - (max_size // 10)) )

        # get a random partition of the word list of size max_size // 10
        word_partition = word_list[part_start:part_start+(max_size // 10)]

        # get the corresponding gold_standard for that partition
        gold_partition = gold_standard[part_start:part_start+(max_size // 10)]

        # perform the cross-validation on the partition
        accuracy = cross_validation(word_partition, pos_dict, gold_partition)

        cross_val_acc += accuracy

    cross_val_acc = cross_val_acc/10

    print('Ten-fold cross-validation accuracy: ', float("{0:.2f}".format(100*cross_val_acc)), '%')


if __name__ == "__main__":
    line_list = helper.read_lines(train_file_name)
    transformed_lines = helper.transf_lines(line_list)

    # get frequency of each word/POS pair
    freq_list = helper.get_frequency_list(transformed_lines)

    # remove the duplicates from the transformed lines
    line_list = list(dict.fromkeys(transformed_lines))

    # create a list with the frequency and the lines
    pos_freq = list(zip(line_list, freq_list))

    # order the list in alphabetic order
    pos_freq = sorted(pos_freq)

    # get the most frequent tag for each word
    pos_freq_list, pos_dict = helper.get_most_frequent_pos(pos_freq)
    
    # save the most frequent POS tag for each word
    helper.save_file(freq_pos_file_name, pos_freq_list)

    # get the data to make the POS tagging
    test_data = helper.read_lines(test_file_name)

    # prepare the data for the pos tagging
    print('Preparing data for tagging')
    word_list, gold_standard = helper.prepare_data(test_data)

    # get the POS tags after the tagging according to the baseline
    print('Making the POS tagging')
    tag_list = pos_tagging(word_list, pos_dict)

    # compare predictions with gold standard
    print('Ten fold cross-validation')
    ten_fold_cross_val(word_list, pos_dict, gold_standard)
    