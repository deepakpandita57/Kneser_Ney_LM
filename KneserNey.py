#!/usr/bin/python2

# Author: Deepak Pandita
# Date created: 29 Sep 2017

import math
import numpy as np

train_file = '/pos/train'
test_file = '/pos/test'
d = 0.5

#Read train file
print 'Reading file: '+train_file
f = open(train_file)
all_sentences = f.readlines()

#unigrams = {}
bigrams = {}
trigrams = {}

num_wordi2_wordi1_star = {}	#N1+(word_i-2 word_i-1 *)
num_star_wordi1_wordi = {}	#N1+(* word_i-1 word_i)
num_star_wordi1_star = {}	#N1+(* word_i-1 *)
num_wordi1_star = {}	#N1+(word_i-1 *)
num_star_wordi = {}	#N1+(* word_i)


for line in all_sentences:
	tokens = line.strip().split(' ')[1:]
	words = [y for x,y in enumerate(tokens) if x%2 == 0]
	
	#Compute bigram and trigram frequencies
	for i,word in enumerate(words):
		#unigrams[word] = unigrams.get(word,0) + 1
		
		if i==0:
			bigrams['<S>',word] = bigrams.get(('<S>',word),0) + 1
			trigrams['<S>','<S>',word] = trigrams.get(('<S>','<S>',word),0) + 1
		if i>0:
			bigrams[words[i-1],word] = bigrams.get((words[i-1],word),0) + 1
		if i==1:
			trigrams['<S>',words[i-1],word] = trigrams.get(('<S>',words[i-1],word),0) + 1
		if i>1:
			trigrams[words[i-2],words[i-1],word] = trigrams.get((words[i-2],words[i-1],word),0) + 1

for key in trigrams:
	num_wordi2_wordi1_star[key[0],key[1],'<star>'] = num_wordi2_wordi1_star.get((key[0],key[1],'<star>'),0) + 1
	num_star_wordi1_wordi['<star>',key[1],key[2]] = num_star_wordi1_wordi.get(('<star>',key[1],key[2]),0) + 1
	num_star_wordi1_star['<star>',key[1],'<star>'] = num_star_wordi1_star.get(('<star>',key[1],'<star>'),0) + 1
	
for key in bigrams:
	num_wordi1_star[key[0],'<star>'] = num_wordi1_star.get((key[0],'<star>'),0) + 1
	num_star_wordi['<star>',key[1]] = num_star_wordi.get(('<star>',key[1]),0) + 1

#function to calculate unigram probability
def PKN1(wordi):
	if (num_star_wordi.get(('<star>',wordi),0))==0:
		p=1
	else:
		p = float(num_star_wordi.get(('<star>',wordi)))/len(bigrams)
	return p

#function to calculate bigram probability
def PKN2(wordi,wordi1,d):
	if (num_wordi1_star.get((wordi1,'<star>'),0))==0:
		p=1
		return p
		
	denominator = num_star_wordi1_star.get(('<star>',wordi1,'<star>'),0)
	if denominator==0:
		p = PKN1(wordi)
		return p
		
	p = (max(0,(num_star_wordi1_wordi.get(('<star>',wordi1,wordi),0) - d)) + (d*num_wordi1_star.get((wordi1,'<star>'))*PKN1(wordi)))/num_star_wordi1_star.get(('<star>',wordi1,'<star>'))
	return p

#function to calculate trigram probability
def PKN3(wordi,wordi2,wordi1,d):
	
	if (num_wordi2_wordi1_star.get((wordi2,wordi1,'<star>'),0))==0:
		p=1
		return p
	
	denominator = bigrams.get((wordi2,wordi1),0)
	if denominator==0:
		p = PKN2(wordi,wordi1,d)
		return p
	
	#Kneser Ney trigram probability
	p = (max(0,(trigrams.get((wordi2,wordi1,word),0) - d)) + d*(num_wordi2_wordi1_star.get((wordi2,wordi1,'<star>')))*PKN2(wordi,wordi1,d))/bigrams.get((wordi2,wordi1))
	return p

#print unigrams
print 'No. of Bigrams '+str(len(bigrams))
print 'No. of Trigrams '+str(len(trigrams))

#Read test file
print 'Reading file: '+test_file

#probability of test set
totalProb = 0
N=0

with open(test_file) as tf:
	for line in tf:
		tokens = line.strip().split(' ')[1:]
		words = [y for x,y in enumerate(tokens) if x%2 == 0]
		N+=len(words)
		
		#probability for the current sentence (we will use log probability)
		prob = 0
		for i,word in enumerate(words):
			PKN = 0
			if i==0:
				PKN = PKN3(word,'<S>','<S>',d)
			if i==1:
				PKN = PKN3(word,'<S>',words[i-1],d)
			if i>1:
				PKN = PKN3(word,words[i-2],words[i-1],d)
			prob+=math.log(PKN)
		#print prob
		totalProb+=prob

#Calculate perplexity
print 'N: ' + str(N)
l = totalProb/N
print l
perplexity = math.exp(-l)
print 'd: '+str(d)+'\tPerplexity: ' + str(perplexity)