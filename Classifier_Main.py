# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 16:38:47 2018

@author: federicopaoletti
"""

from __future__ import division
import os
import string
import pandas as pd
import nltk, pylab, sys, numpy
from nltk.probability import FreqDist
from pylab import *
from random import *
from ProcessingAndClassifier_Functions import *

#seed(1)    
os.chdir('/Users/federicopaoletti/Desktop/Evidence Aid/Classification Resources/Data Sets')

#### DATA loading and merging ###

all_SRs = pd.read_csv('All_Cochrane_ID.csv')
print all_SRs.iloc[:,0]
print all_SRs.shape

R_total = pd.read_csv('Relevant_ID.csv')
print R_total.iloc[:,0]
print R_total.shape

counter = 0
R_indices = []
for i in range(all_SRs.shape[0]):
    if all_SRs.iloc[i,0] in set(R_total.iloc[:,0]):
        print all_SRs.iloc[i,0]
        R_indices.append(i)
        counter += 1
        print counter
   # for j in range(R_total.shape[0]):
      #  if all_SRs.iloc[i,0] == R_total.iloc[j,0]:
      #      print all_SRs.iloc[i,0]
      #      R_indices.append(i)
      #      counter += 1
      #      print counter
    
print R_indices, len(R_indices)

NR_total = all_SRs.drop(R_indices)
NR_total.to_csv('NonRelevant_ID.csv', encoding='utf-8', index=False)
NR_total = pd.read_csv('NonRelevant_ID.csv')

def sample_hyperparameter(NR_multiple, word_length, word_frequency_cutoff):  #calculates fpr, fnr and accuracy of Naive Bayes Classifier 
#given a set of hyperparameters and randomly allocated training, devtest and test data sets
    
    results_list = [run_algorithm(int(171 * NR_multiple), word_length, 
                                  word_frequency_cutoff, NR_total, R_total) for x in range(10)]
    print results_list

    devtest_false_negative_rate_list = []
    devtest_false_positive_rate_list = []
    devtest_accuracy_list = []

    for results_tuple in results_list:
        devtest_false_negative_rate_list.append(results_tuple[1])
        devtest_false_positive_rate_list.append(results_tuple[0])
        devtest_accuracy_list.append(results_tuple[2])

    false_negative_rate_array = numpy.array([devtest_false_negative_rate_list])

    print 'Mean false negative rate:'
    print numpy.mean(false_negative_rate_array)
    print 'False negative rate standard deviation:'
    print numpy.std(false_negative_rate_array)

    FN_dataframe = pd.DataFrame({'DevTest False Negative Rates': devtest_false_negative_rate_list, 
                                 'DevTest False Positive Rates': devtest_false_positive_rate_list, 
                                 'DevTest Accuracy': devtest_accuracy_list})
                                 
    filename = 'FN-FP-Accuracy Runs/FN_FP_Accuracy_run_moretrainingdata_infFeatures' + str(NR_multiple) + '_' + str(word_length) + '_' + str(word_frequency_cutoff) + '.csv'
    FN_dataframe.to_csv(filename)
 
NR_multiples = [1] #[1, 2, 3, 4, 6, 7, 8, 9, 10]
minimum_word_lengths = [8] #[4, 5, 6, 7, 8, 9, 10]
word_frequency_cutoffs = [2600] #list(numpy.linspace(200, 4000, 20)) 

for multiple in NR_multiples:
    for wordlength in minimum_word_lengths:
        for cutoff in word_frequency_cutoffs:
            sample_hyperparameter(multiple, wordlength, cutoff)
    
    
