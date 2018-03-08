"""
Created on Thu Mar  8 10:59:43 2018

@author: federicopaoletti
"""

import numpy as np
import pandas as pd
import nltk
import nltk.corpus  
from nltk.text import Text
from nltk.tokenize import sent_tokenize, word_tokenize

def SRstruct(SR):
	nSR = len(SR)

	# Append new columns for quality criteria and retrieve indeces of columns
	newColumn = np.empty(nSR)
	newColumn[:] = np.nan
	SR['Appropriate study type'] = pd.Series(newColumn	,	index = SR.index)
	SR['Number of studies'] = pd.Series(newColumn	,	index = SR.index)
	SR['Number of participants'] = pd.Series(newColumn	,	index = SR.index)
	SR['Approximate number of databases'] = pd.Series(newColumn	,	index = SR.index)
	SR['Number of independent reviewers'] = pd.Series(newColumn	,	index = SR.index)
	SR['Risk of bias assessment'] = pd.Series(newColumn	,	index = SR.index)
	
	# Get indeces for columns
	idx_selCrit = SR.columns.get_loc("Selection criteria")
	idx_search = SR.columns.get_loc("Search methods")
	idx_main = SR.columns.get_loc("Main results")
	idx_DA = SR.columns.get_loc("Data collection and analysis")
	idx_concl = SR.columns.get_loc("Authors' conclusions")

	idx_apprStudy = SR.columns.get_loc("Appropriate study type")
	idx_nStudies = SR.columns.get_loc("Number of studies")
	idx_nPart = SR.columns.get_loc("Number of participants")
	idx_nDB = SR.columns.get_loc("Approximate number of databases")
	idx_nReview = SR.columns.get_loc("Number of independent reviewers")
	idx_rofb = SR.columns.get_loc("Risk of bias assessment")
	return SR, idx_selCrit, idx_search, idx_main, idx_DA, idx_apprStudy, idx_nStudies, \
				idx_nPart, idx_nDB, idx_nReview, idx_rofb, idx_concl, nSR

def word2num(number):
	wordDict = {'0?': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, \
 'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15, 'sixteen': 16, 'seventeen': 17, 'eighteen': 18, 'nineteen': 19, \
 'twenty-one': 21, 'twenty-two': 22, 'twenty-three': 23, 'twenty-four': 24, 'twenty-five': 25, 'twenty-six': 26, 'twenty-seven': 27, 'twenty-eight': 28, 'twenty-nine': 29, \
  'thirty-one': 31, 'thirty-two': 32, 'thirty-three': 33, 'thirty-four': 34, 'thirty-five': 35, 'thirty-six': 36, 'thirty-seven': 37, 'thirty-eight': 38, 'thirty-nine': 39, \
  'fourty-one': 41, 'fourty-two': 42, 'fourty-three': 43, 'fourty-four': 44, 'fourty-five': 45, 'fourty-six': 46, 'fourty-seven': 47, 'fourty-eight': 48, 'fourty-nine': 49, \
  'forty-one': 41, 'forty-two': 42, 'forty-three': 43, 'forty-four': 44, 'forty-five': 45, 'forty-six': 46, 'forty-seven': 47, 'forty-eight': 48, 'forty-nine': 49,   
  'fifty-one': 51, 'fifty-two': 52, 'fifty-three': 53, 'fifty-four': 54, 'fifty-five': 55, 'fifty-six': 56, 'fifty-seven': 57, 'fifty-eight': 58, 'fifty-nine': 59, \
  'sixty-one': 61, 'sixty-two': 62, 'sixty-three': 63, 'sixty-four': 64, 'sixty-five': 65, 'sixty-six': 66, 'sixty-seven': 67, 'sixty-eight': 68, 'sixty-nine': 69, \
  'seventy-one': 71, 'seventy-two': 72, 'seventy-three': 73, 'seventy-four': 74, 'seventy-five': 75, 'seventy-six': 76, 'seventy-seven': 77, 'seventy-eight': 78, 'seventy-nine': 79, \
  'eighty-one': 81, 'eighty-two': 82, 'eighty-three': 83, 'eighty-four': 84, 'eighty-five': 85, 'eighty-six': 86, 'eighty-seven': 87, 'eighty-eight': 88, 'eighty-nine': 89, \
  'ninety-one': 91, 'ninety-two': 92, 'ninety-three': 93, 'ninety-four': 94, 'ninety-five': 95, 'ninety-six': 96, 'ninety-seven': 97, 'ninety-eight': 98, 'ninety-nine': 99, \
			'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, \
   'Eleven': 11, 'Twelve': 12, 'Thirteen': 13, 'Fourteen': 14, 'Fifteen': 15, 'Sixteen': 16, 'Seventeen': 17, 'Eighteen': 18, 'Nineteen': 19, \
 'Twenty-one': 21, 'Twenty-two': 22, 'Twenty-three': 23, 'Twenty-four': 24, 'Twenty-five': 25, 'Twenty-six': 26, 'Twenty-seven': 27, 'Twenty-eight': 28, 'Twenty-nine': 29, \
  'Thirty-one': 31, 'Thirty-two': 32, 'Thirty-three': 33, 'Thirty-four': 34, 'Thirty-five': 35, 'Thirty-six': 36, 'Thirty-seven': 37, 'Thirty-eight': 38, 'Thirty-nine': 39, \
  'Fourty-one': 41, 'Fourty-two': 42, 'Fourty-three': 43, 'Fourty-four': 44, 'Fourty-five': 45, 'Fourty-six': 46, 'Fourty-seven': 47, 'Fourty-eight': 48, 'Fourty-nine': 49, \
    'Forty-one': 41, 'Forty-two': 42, 'Forty-three': 43, 'Forty-four': 44, 'Forty-five': 45, 'Forty-six': 46, 'Forty-seven': 47, 'Forty-eight': 48, 'Forty-nine': 49, \
  'Fifty-one': 51, 'Fifty-two': 52, 'Fifty-three': 53, 'Fifty-four': 54, 'Fifty-five': 55, 'Fifty-six': 56, 'Fifty-seven': 57, 'Fifty-eight': 58, 'Fifty-nine': 59, \
  'Sixty-one': 61, 'Sixty-two': 62, 'Sixty-three': 63, 'Sixty-four': 64, 'Sixty-five': 65, 'Sixty-six': 66, 'Sixty-seven': 67, 'Sixty-eight': 68, 'Sixty-nine': 69, \
  'Seventy-one': 71, 'Seventy-two': 72, 'Seventy-three': 73, 'Seventy-four': 74, 'Seventy-five': 75, 'Seventy-six': 76, 'Seventy-seven': 77, 'Seventy-eight': 78, 'Seventy-nine': 79, \
  'Eighty-one': 81, 'Eighty-two': 82, 'Eighty-three': 83, 'Eighty-four': 84, 'Eighty-five': 85, 'Eighty-six': 86, 'Eighty-seven': 87, 'Eighty-eight': 88, 'Eighty-nine': 89, \
  'Ninety-one': 91, 'Ninety-two': 92, 'Ninety-three': 93, 'Ninety-four': 94, 'Ninety-five': 95, 'Ninety-six': 96, 'Ninety-seven': 97, 'Ninety-eight': 98, 'Ninety-nine': 99, \
			'twenty': 20, 'thirty': 30, 'fourty': 40, 'forty': 40, 'fifty': 50, 'sixty': 60, 'seventy': 70, 'eighty': 80, 'ninety': 90, 'thousand': 1000, 'million': 1000000, 'none': 0, \
			'Twenty': 20, 'Thirty': 30, 'Fourty': 40, 'Forty': 40, 'Fifty': 50, 'Sixty': 60, 'Seventy': 70, 'Eighty': 80, 'Ninety': 90, 'Thousand': 1000, 'Million': 1000000, 'None': 0, 'both': 2, 'Both': 2}
	if number in wordDict:
         N = float(wordDict[number])
	else:
         if number.find(',') != -1:
             number = number.replace(',','')
             N = float(number)
         if '/' in number:
             number = number[number.find('/') - 1]
             N = float(number)
         else:
             number2 = number.replace('a', '')
             number3 = number2.replace('b', '')
             number4 = number3.replace('s', '')
             number5 = number4.replace('did', '')
             number6 = number5.replace('P', '')
             number7 = number6.replace('mg', '')
             number8 = number7.replace('g', '')
             number9 = number8.replace('?', '')
             number10 = "".join(i for i in number9 if ord(i)<128)
             N = float(number10)
	return N

def studyTypes(SR,iSR,idx_selCrit,idx_apprStudy):
	# Note 1: I'm omitting first letters to avoid having to care about case sensitivity
	# Note 2: I'm omitting the ending of study/studies to avoid having to care about singular/plural
	# Note 3: When looking for 'andomised controlled trial', I will also find 'non-randomised controlled trial',
	# 			'cluster randomised trial' --> Redundancy in wording of studies on the list is taken into account here
	#Note 4: Use these 2 first lines not to miss the randomised clinical studies:
			# study_accept = ["andomised controlled", "andomized controlled", "RCT", "NRCT", \
			#	"andomised","andomized", \

	study_accept = ["andomised controlled trial", "andomized controlled trial", "RCT", "NRCT", \
					"andomised trial","andomized trial", \
					"efore-after stud", "CBA", \
					"nterrupted-time-series stud", "ITS", \
					"epeated measures stud", "pinion paper", "on-comparative stud", \
					"etrospective case-control stud", "rospective case-control stud", \
					"etrospective cohort stud"] 
	
	relevantField_studyType = SR.iloc[iSR,idx_selCrit]
	for study in study_accept:
		hit = relevantField_studyType.find(study)
		if hit != -1:
			SR.iloc[iSR,idx_apprStudy] = 'Yes'
			break
		SR.iloc[iSR,idx_apprStudy] = 'No'
	return SR

def rofb(SR, iSR, idx_DA, idx_main, idx_concl):
	relevantField = SR.iloc[iSR,idx_DA]
	hit = relevantField.find('isk of bias')
	if hit != -1:
		SR.iloc[iSR,idx_rofb] = 'Yes'
	else:
		relevantField = SR.iloc[iSR,idx_main]
		hit = relevantField.find('isk of bias')
		if hit != -1:
			SR.iloc[iSR,idx_rofb] = 'Yes'
		else:
			relevantField = SR.iloc[iSR,idx_concl]
			hit = relevantField.find('isk of bias')
			if hit != -1:
				SR.iloc[iSR,idx_rofb] = 'Yes'
			else:
				SR.iloc[iSR,idx_rofb] = 'No'
	return SR

def nDB(SR, iSR, idx_search, idx_nDB):
	relevantField = SR.iloc[iSR,idx_search]
	relevantField_sent = nltk.sent_tokenize(relevantField)
	nDatabases = 1
	for iSent in relevantField_sent:
		if iSent.find('search') != -1:
			nComma = iSent.count(',')
			nDatabases = nDatabases + nComma + 1 # Very approximate number ...
			SR.iloc[iSR,idx_nDB] = nDatabases
			break
	return SR

def reviewers(SR,iSR,idx_DA,idx_nReview):
	relevantField_nReview = SR.iloc[iSR,idx_DA]
	reviewerRefs = ['review','reviewer','reviewers','author','authors','investigator','investigators','researcher','researchers']
	# Split and tag words in the relevant field
	field_wordList = nltk.word_tokenize(relevantField_nReview)
	field_wordList = [i for i in field_wordList if (i != '.' and i != ',' and i != '(' and i != ')' and i != '%')]
	tags = nltk.pos_tag(field_wordList)
	iTag = 0
	hitReviewers = 0
	
	while iTag < (len(tags) - 1): 										#in range(len(tags)):
	 	if (tags[iTag][1] == "CD" or tags[iTag][0] == "both" or tags[iTag][0] == "Both"): #and hitReviewers == 0:				#and iTag < len(tags)-1: # ... to identify numerals	
	 		nextWord_idx = iTag+1
	 		nextWord = tags[nextWord_idx][0]								
	 		nextTag = tags[nextWord_idx][1]
	 		while nextWord_idx <= len(tags)-1:
	 			if nextTag.find("NN") != -1:												# Find the next noun after the numeral
	 				if 	nextWord in reviewerRefs:
	 					SR.iloc[iSR,idx_nReview] = word2num(tags[iTag][0])
	 					iTag += 1
	 					break
	 				else:
	 					iTag += 1
	 					break
	 			elif nextTag.find("NN") == -1 and nextWord_idx <= len(tags)-2:
	 				nextWord_idx += 1
	 				nextWord = tags[nextWord_idx][0]									
	 				nextTag = tags[nextWord_idx][1]
	 			else:
	 				break
	 	else: 
	 		iTag += 1
	 	break
	return SR

def nStudPart(SR,iSR,idx_main, idx_nPart, idx_nStudies):
	relevantField_nStudies = SR.iloc[iSR,idx_main]
	trialRefs = ['trials','studies','RCT','RCTs','ITS']
	partRefs = ['participants','people','adults','children','patients','infants','individuals','specimens','soldiers']
	field_wordList = nltk.word_tokenize(relevantField_nStudies)					
	field_wordList = [i for i in field_wordList if (i != '.' and i != ',' and i != '(' and i != ')' and i != '%')]
	tags = nltk.pos_tag(field_wordList)
	iTag = 0
	hitStudies = 0
	hitParticipants = 0
	
	while iTag in range(len(tags)):
	 	if hitStudies == 0 or hitParticipants == 0:
	 		if tags[iTag][1] == "CD" and tags[iTag][0].find(".") == -1 and iTag < len(tags)-1: # ... to identify numerals	
	 			nextWord_idx = iTag+1
	 			nextWord = tags[nextWord_idx][0]									
	 			nextTag = tags[nextWord_idx][1]
	 			while nextWord_idx <= len(tags)-1:
	 				if nextTag.find("NN") != -1:
	 					if hitStudies == 0 and (nextWord in trialRefs):
	 						SR.iloc[iSR,idx_nStudies] = word2num(tags[iTag][0])
	 						hitStudies = 1
	 						iTag += 1
	 						break
	 					elif hitParticipants == 0 and (nextWord in partRefs):
	 						SR.iloc[iSR,idx_nPart] = word2num(tags[iTag][0])
	 						hitParticipants = 1
	 						iTag += 1
	 						break
	 					else:
	 						iTag += 1
	 						break
	 				elif nextTag.find("NN") == -1 and nextWord_idx <= len(tags)-2:
	 					nextWord_idx += 1
	 					nextWord = tags[nextWord_idx][0]									
	 					nextTag = tags[nextWord_idx][1]
	 				else:
	 					hitParticipants = 1
	 					hitStudies = 1
	 					break
	 		else: 
	 			iTag += 1
	 	else:
	 		break
	return SR
