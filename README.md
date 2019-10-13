README
=======

## Problem

The goal of this project is to solve the part of speech (POS) tagging by applying the traditional baseline.
The baseline consists in simply tagging each word with their most frequent part of speech.
These frequencies can be determined by using a part-of-speech annotated corpus and, then,
further applied to the text which we would like to tag.

The performance of this project is evaluated in a cross-validation manner.

This project was developed for a Natural Language Processing lecture.

## Files

* `pos_baseline.py` : main file with all the functions required to execute the baseline for the POS tagging
* `pos_helpers.py` : helper functions to read/save text files and to manipulate the text data
* `train.txt` : train file acquired from [1]
* `test.txt` : train file acquired from [1]

# How to run

To run the code, simply save all the files in the same directory and run `python3 pos_baseline.py`.

## References

[1] https://www.clips.uantwerpen.be/conll2000/chunking/