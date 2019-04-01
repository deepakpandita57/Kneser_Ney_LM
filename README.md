# Implement a Kneser Ney trigram language model


Task
=============================================================================================================
To implement a Kneser Ney trigram language model using the train and test data.


Instructions for running "KneserNey.py"
=============================================================================================================
To run the script "KneserNey.py" change the values of "train_file", "test_file" and "tag_file" variables in the script.
We also have to specify the value for 'd' that we want to use.


Description
=============================================================================================================
Trigram, bigram and other counts like N1+(* word_i) are computed from the training data. Then, the probabilities
for the test sentences is computed based on these counts using Kneser Ney trigram language model.


Perplexity:
=============================================================================================================
Perplexity values for different values of d are as follows:

d: 0.4  Perplexity: 62.251
d: 0.5  Perplexity: 56.863
d: 0.6  Perplexity: 53.242
d: 0.7  Perplexity: 50.866
d: 0.8  Perplexity: 49.573
d: 0.9  Perplexity: 49.644


References
=============================================================================================================
This was done as a homework problem in the Statistical Speech and Language Processing class (CSC 448, Fall 2017) by Prof. Daniel Gildea (https://www.cs.rochester.edu/~gildea/) at the University of Rochester, New York.