## NT 17/02/2018
# -*- coding: UTF-8 -*-
import numpy as np
import pandas as pd
import nltk
import nltk.corpus  
from nltk.text import Text
from nltk.tokenize import sent_tokenize, word_tokenize
from Quality_Functions import SRstruct, word2num, studyTypes, rofb, nDB, reviewers, nStudPart

#########################################################
#				MAIN SCRIPT STARTS HERE 				#
#########################################################
# Import the .csv file with all relevant SR
SR = pd.read_csv('/Users/federicopaoletti/Desktop/Evidence Aid/Classification Resources/Data Sets/NonRelevant_ID.csv', encoding='utf-8')
#SR = pd.read_csv('/Users/NCT/Work/evidence_aid_project/quality_criteria/code/NonRelevant_ID.csv')


# Append additional columns and get the indeces for various columns
SR, idx_selCrit, idx_search, idx_main, idx_DA, idx_apprStudy, idx_nStudies, \
				idx_nPart, idx_nDB, idx_nReview, idx_rofb, idx_concl, nSR = SRstruct(SR)

# Searching for study type keywords in Selection criteria
for iSR in SR.index:
	SR_ID = SR["ID"][iSR]
	#SR_ID = SR["ID"][iSR]			# NOTE: Use this line for relevant reviews because different index
	print("Searching:	" + SR_ID + "	(" + str(iSR+1) + "/" + str(nSR) + ")")

	# Search for study types in 'Selection criteria'
	SR = studyTypes(SR,iSR,idx_selCrit,idx_apprStudy)

	# Search for risk of bias assessment in 'Data collection and analysis'
	SR = rofb(SR, iSR, idx_DA, idx_main, idx_concl)

	# Search for number of databases searched in 'Search methods'
	SR = nDB(SR, iSR, idx_search, idx_nDB)

	# Searching for number of reviewers in 'Data collection and analysis'
	SR = reviewers(SR,iSR,idx_DA,idx_nReview)

	# Searching for number of studies and participants in 'Main results'
	SR = nStudPart(SR,iSR,idx_main, idx_nPart, idx_nStudies)

# Export SR as .csv file
SR.to_csv('/Users/federicopaoletti/Desktop/Evidence Aid/Classification Resources/Data Sets/NonRelevant_ID_QualitySorted.csv', encoding='utf-8', index=False)
