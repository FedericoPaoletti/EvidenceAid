# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 14:16:42 2017

@author: federicopaoletti
"""
from __future__ import division
import os
import string
import pandas as pd
import nltk, pylab, sys
from nltk.probability import FreqDist
from pylab import *
from random import *

def preprocess(SR):
    SR = ''.join(SR)  # join all dataframe row entries into a single string
    SR = SR.replace('.', ' ') # replace '.' with spaces
    SR = SR.lower() # convert all words to lowercase
    SR = SR.translate(None, string.punctuation) # remove all punctuation
    SR = SR.translate(None, '0123456789')  # remove all numbers
    SR = SR.split()  # tokenise 
    #print SR
    return SR
    
def total_word_frequency(SR_dataframe, word_length):
    SRlist = []

    for index, row in SR_dataframe.iterrows():
        currentSR = [x for x in SR_dataframe.iloc[index,:]]
        SRlist += currentSR
    
    print SRlist
    SRlist = preprocess(SRlist)
    word_freq = FreqDist([words for words in SRlist if words.isalpha() and len(words) > int(word_length)])
    return word_freq
 
def generate_labelled_SRlist(SR_dataframe, label):
    labelled = []
    for index, row in SR_dataframe.iterrows():
        currentSR = [x for x in SR_dataframe.iloc[index,:]]
        processedSR = preprocess(currentSR)
        labelledSR = (processedSR, str(label))
        labelled.append(labelledSR)
    #print labelled
    return labelled
    
def generate_randomly_labelled_trainset(trainset, labels):
    labelled = []
    for features, label in trainset:
        labelledSR = (features, str(choice(labels)))
        labelled.append(labelledSR)
    #print labelled
    return labelled
    
def generate_total_wordlist(labelled_SR_list):
    SR_word_list = [words for (words, label) in labelled_SR_list] 
    total_word_list = []
    for words in SR_word_list:
        total_word_list += words
    return total_word_list
    
def generate_SR_features(SR_wordlist, myword_features):
    SR_words = set(SR_wordlist)
    #print SR
    #print set(SR)
    features = {}
    for word in myword_features:
        features['contains(%s)' % word] = (word in SR_words)
    return features
   
def generate_word_features(wordlist, min_wordlength, number_of_words):
    
    word_freq = FreqDist([words for words in wordlist if words.isalpha() and len(words) > int(min_wordlength)])
    sorted_word_freq = sorted(word_freq, reverse=True, key=word_freq.get)
    word_features = sorted_word_freq[:number_of_words]
    return word_features
    
def perform_error_analysis(classifier, develpment_test_set, word_features, featureset, labelled_SRs):
    errors = [];
    for (SRwords, label) in develpment_test_set:
        guess = classifier.classify(SRwords)
        if guess != label:
            errors.append((label, guess, labelled_SRs[featureset.index((SRwords, label))]))

    for (label, guess, abstract) in sorted(errors):
        print 'correct=%-8s guess=%-8s abstract=%-30s' % (label, guess, labelled_SRs.index(abstract))
    return errors
    
def calculate_false_positive_rate(errorlist, featurelabel_list):
    false_positive_list = [label for (label, guess, abstractnumber) in errorlist if label == 'NR']
    true_negative_list = [label for (features, label) in featurelabel_list if label == 'NR']
    print '\n'
    print 'Number of false positives in devtest set: ', len(false_positive_list)
    print '\n'
    print 'Number of true negatives in devtest set: ', len(true_negative_list)

    false_positive_rate = len(false_positive_list) / len(true_negative_list)
    return false_positive_rate
    
def calculate_false_negative_rate(errorlist, featurelabel_list):
    false_negative_list = [label for (label, guess, abstractnumber) in errorlist if label == 'R']
    true_positive_list = [label for (features, label) in featurelabel_list if label == 'R']
    print '\n'
    print 'Number of false negatives in devtest set: ', len(false_negative_list)
    print '\n'
    print 'Number of true positives in devtest set: ', len(true_positive_list)    
    
    false_negative_rate = len(false_negative_list) / len(true_positive_list)
    return false_negative_rate
        
def run_algorithm(NumberOfNRs, Word_Length, 
                  Word_Frequency_Cutoff, NR_total, R_total):
    ### DATA labelling and shuffling ###
    print '\n'
    print '############ Preparing Data Set ... ############'
    print '\n'
    
    NR_total_labelled = generate_labelled_SRlist(NR_total, 'NR')
    NR_total_labelled = sample(NR_total_labelled, len(NR_total_labelled))
    
    NR_total_labelled = NR_total_labelled[:NumberOfNRs]
    print 'Number of NR Abstracts', len(NR_total_labelled) 
    
    R_total_labelled = generate_labelled_SRlist(R_total, 'R')
    print 'Number of R Abstracts', len(R_total_labelled)
    
    all_SRs_labelled = NR_total_labelled + R_total_labelled #We chose to balance the R and NR data sets i.e. 176 Rs and 176 NRs.
    print 'Total Number of Abstracts', len(all_SRs_labelled)
    
    shuffled_SRs_labelled = sample(all_SRs_labelled, len(all_SRs_labelled))
    
    
    
    ### Definition of word features ###
    
    
    
    tot_wordlist = generate_total_wordlist(shuffled_SRs_labelled)
    
    
    
    ### Generate SR features, divide training and test sets, train Naive Bayes Classifier ###
    
    
    
    myword_features = generate_word_features(tot_wordlist, int(Word_Length), int(Word_Frequency_Cutoff))
    
    featuresets = [(generate_SR_features(SR, myword_features), label) for (SR, label) in shuffled_SRs_labelled]
    #print featuresets
    
    #UNCOMMENT TO RETURN TO ORIGINAL TRAIN. DEVTEST. TEST SETTING:
    #train_set, devtest_set, test_set = featuresets[200:], featuresets[100:200], featuresets[:100]
    
    train_set, devtest_set = featuresets[100:], featuresets[:100]
    print '\n'
    print '############ Training Naive Bayes Classifier... ############'
    print '\n'
    
    classifier1 = nltk.NaiveBayesClassifier.train(train_set) 
    
    print 'size of training set: ', len(train_set)
    
    
      
    ### Classify Develpoment Test Set ###
      
      
      
    print '\n'
    print '############ Classifying Dev-Test Set... ############'
    print '\n'
    
    print 'size of devtest set: ', len(devtest_set)   
    print 'classifier accuracy for devtest set: ', nltk.classify.accuracy(classifier1, devtest_set)
    classifier1.show_most_informative_features(50)
    
    
    
    ### Error Analysis ###
    
    
    
    print '\n'
    print '############ Error Analysis ############'
    print '\n'
    
    errors1 = perform_error_analysis(classifier1, devtest_set, myword_features, featuresets, shuffled_SRs_labelled)
    
    devtest_set_accuracy = nltk.classify.accuracy(classifier1, devtest_set)
    fpr = calculate_false_positive_rate(errors1, devtest_set)
    fnr = calculate_false_negative_rate(errors1, devtest_set)
    print 'classifier false positive rate for devtest set: ', fpr
    print 'classifier false negative rate for devtest set: ', fnr
    
    
    
#    ### Classify Test Set ###
#    print '\n'
#    print 'classifier accuracy for test set: ', nltk.classify.accuracy(classifier1, test_set)
#    print '\n'
    
    
    
    
#    ### Validation: what happens if we assign random labels to the training data set? ###
#    print '\n'
#    print '############ Validation: What Happens If We Assign Random Labels To The Training Data Set? ############'
#    print '\n'
#    print 'Before label scrambling: '
#    
#    for features, label in train_set[:5]:
#        print label
#    
#    train_set_random = generate_randomly_labelled_trainset(train_set, ['R', 'NR'])
#    
#    print 'After label scrambling: '  
#    for features, label in train_set_random[:5]:
#        print label
#        
#    classifier2 = nltk.NaiveBayesClassifier.train(train_set_random)
#    print 'size of devtest set: ', len(devtest_set)   
#    print 'classifier accuracy for devtest set: ', nltk.classify.accuracy(classifier2, devtest_set)
#    
#    classifier2.show_most_informative_features(10)
#    
    
    
    
#    ### Error Analysis - Randomly Labelled Training Data Set ###
#    
#    
#    
#    
#    print '\n'
#    print '############ Error Analysis - Randomly Labelled Training Data Set ############'
#    print '\n'
#    
#    errors2 = perform_error_analysis(classifier2, devtest_set, myword_features, featuresets, shuffled_SRs_labelled)
#    
#    print 'classifier false positive rate for devtest set: ', calculate_false_positive_rate(errors2, devtest_set)
#    print 'classifier false negative rate for devtest set: ', calculate_false_negative_rate(errors2, devtest_set)   
    
    return (fpr, fnr, devtest_set_accuracy)
