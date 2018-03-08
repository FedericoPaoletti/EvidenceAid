## NT 17/02/2018

import numpy as np
import pandas as pd
import nltk
import nltk.corpus  
from nltk.text import Text
from nltk.tokenize import sent_tokenize, word_tokenize
import matplotlib.pyplot as plt

def SRstruct(SR):
	idx_apprStudy = SR.columns.get_loc("Appropriate study type")
	idx_nStudies = SR.columns.get_loc("Number of studies")
	idx_nPart = SR.columns.get_loc("Number of participants")
	idx_nDB = SR.columns.get_loc("Approximate number of databases")
	idx_nReview = SR.columns.get_loc("Number of independent reviewers")
	idx_rofb = SR.columns.get_loc("Risk of bias assessment")
	return idx_apprStudy, idx_nStudies, idx_nPart, idx_nDB, idx_nReview, idx_rofb




#########################################
# 		MAIN SCRIPT STARTS HERE			#
#########################################

# Import dataframes
SR_rel = pd.read_csv('/Users/federicopaoletti/Desktop/Evidence Aid/Classification Resources/Data Sets/Relevant_ID_QualitySorted.csv')
SR_nonrel = pd.read_csv('/Users/federicopaoletti/Desktop/Evidence Aid/Classification Resources/Data Sets/NonRelevant_ID_QualitySorted.csv')

nRel = len(SR_rel)
#nNonrel = nRel
nNonrel = len(SR_nonrel);

# Get important indeces
RELidx_apprStudy, RELidx_nStudies, RELidx_nPart, RELidx_nDB, RELidx_nReview, RELidx_rofb = SRstruct(SR_rel)
NONRELidx_apprStudy, NONRELidx_nStudies, NONRELidx_nPart, NONRELidx_nDB, NONRELidx_nReview, NONRELidx_rofb = SRstruct(SR_nonrel)

## Get data from SRs and remove NaNs

#apprStudy

apprStudy_rel = np.array(SR_rel.iloc[:,RELidx_apprStudy])
apprStudy_nonrel = np.array(SR_nonrel.iloc[:,NONRELidx_apprStudy])
#apprStudy_rel = [i for i in apprStudy_rel if not np.isnan(i)]
#apprStudy_nonrel = [i for i in apprStudy_nonrel if not np.isnan(i)]

# Calculate percentage 'Yes'

napprStudy_rel = 0
for i in apprStudy_rel:
	if i == 'Yes':
		napprStudy_rel = napprStudy_rel + 1
papprStudy_rel = 100* napprStudy_rel / nRel

napprStudy_nonrel = 0
for i in apprStudy_nonrel:
    if i == 'Yes':
        napprStudy_nonrel = napprStudy_nonrel + 1
papprStudy_nonrel = 100* napprStudy_nonrel / nNonrel

# nStudies
nStudies_rel = np.array(SR_rel.iloc[:,RELidx_nStudies])
nStudies_nonrel = np.array(SR_nonrel.iloc[:,NONRELidx_nStudies])
nStudies_rel = [i for i in nStudies_rel if not np.isnan(i)]
nStudies_nonrel = [i for i in nStudies_nonrel if not np.isnan(i)]

#nParticipants
nPart_rel = np.array(SR_rel.iloc[:,RELidx_nPart])
nPart_nonrel = np.array(SR_nonrel.iloc[:,NONRELidx_nPart])
nPart_rel = [i for i in nPart_rel if not np.isnan(i)]
nPart_nonrel = [i for i in nPart_nonrel if not np.isnan(i)]

#nDB
nDB_rel = np.array(SR_rel.iloc[:,RELidx_nDB])
nDB_nonrel = np.array(SR_nonrel.iloc[:,NONRELidx_nDB])
nDB_rel = [i for i in nDB_rel if not np.isnan(i)]
nDB_nonrel = [i for i in nDB_nonrel if not np.isnan(i)]

#nReview
nReview_rel = np.array(SR_rel.iloc[:,RELidx_nReview])
nReview_nonrel = np.array(SR_nonrel.iloc[:,NONRELidx_nReview])
nReview_rel = [i for i in nReview_rel if not np.isnan(i)]
nReview_nonrel = [i for i in nReview_nonrel if not np.isnan(i)]
	# Calculate percentage >= 2
highQual_rel = [i for i in nReview_rel if i >= 2]
pReview_rel = 100* len(highQual_rel) / nRel
highQual_nonrel = [i for i in nReview_nonrel if i >= 2]
pReview_nonrel = 100* len(highQual_nonrel) / nNonrel

#ROB
ROB_rel = SR_rel.iloc[:,RELidx_rofb]
ROB_nonrel = SR_nonrel.iloc[:,NONRELidx_rofb]
	# Calculate percentage 'Yes'

nROB_rel = 0
for i in ROB_rel:
	if i == 'Yes':
		nROB_rel = nROB_rel+1
pROB_rel = 100* nROB_rel / nRel

nROB_nonrel = 0
for i in ROB_nonrel:
	if i == 'Yes':
		nROB_nonrel = nROB_nonrel+1
pROB_nonrel = 100* nROB_nonrel / nNonrel

## PLOT THE RESULTS
xbins = range(6)
# Number of studies


fig1 = plt.figure(1)
weights_nStudiesrel = np.ones_like(nStudies_rel)/(float(len(nStudies_rel)) / 100)
weights_nStudiesnonrel = np.ones_like(nStudies_nonrel)/(float(len(nStudies_nonrel)) / 100)


plt.hist(nStudies_rel, weights=weights_nStudiesrel, range=[0, 100], bins=100, alpha=0.5, label='Relevant SRs')
plt.hist(nStudies_nonrel, weights=weights_nStudiesnonrel, range=[0, 100], bins=100, alpha=0.5, label='Non-relevant SRs')
plt.legend(loc='upper right')
plt.title("Frequency of number of studies included (% of SRs)")
plt.xlabel('Number of studies')
plt.ylabel('Percent')
fig1.savefig('/Users/federicopaoletti/Desktop/Evidence Aid/Final Report - Classification and Quality Assessment/Figure4_Plots/Figure1.pdf', format='pdf')
#plt.show()

# Number of participants


fig2 = plt.figure(2)
weightsPart_rel = np.ones_like(nPart_rel)/(float(len(nPart_rel)) / 100)
weightsPart_nonrel = np.ones_like(nPart_nonrel)/(float(len(nPart_nonrel)) / 100)


plt.hist(nPart_rel, weights=weightsPart_rel, range=[0, 20000], bins=100,  alpha=0.5, label='Relevant SRs')
plt.hist(nPart_nonrel, weights=weightsPart_nonrel, range=[0, 20000], bins=100,  alpha=0.5, label='Non-relevant SRs')
plt.legend(loc='upper right')
plt.title("Frequency of number of participants included (% of SRs)")
plt.xlabel('Number of participants')
plt.ylabel('Percent')
plt.ylim(0,25)
fig2.savefig('/Users/federicopaoletti/Desktop/Evidence Aid/Final Report - Classification and Quality Assessment/Figure4_Plots/Figure2.pdf', format='pdf')
#plt.show()

# Number of databases
fig3 = plt.figure(3)
weights_nDBrel = np.ones_like(nDB_rel)/(float(len(nDB_rel)) / 100)
weights_nDBnonrel = np.ones_like(nDB_nonrel)/(float(len(nDB_nonrel)) / 100)

plt.hist(nDB_rel, weights=weights_nDBrel, range=[0, 25],bins=25, alpha=0.5, label='Relevant SRs')
plt.hist(nDB_nonrel, weights=weights_nDBnonrel, range=[0, 25], bins=25, alpha=0.5, label='Non-relevant SRs')
plt.legend(loc='upper right')
plt.title("Frequency of number of databases searched (% of SRs)")
plt.xlim(0,25)
plt.xlabel('Number of databases')
plt.ylabel('Percent')
fig3.savefig('/Users/federicopaoletti/Desktop/Evidence Aid/Final Report - Classification and Quality Assessment/Figure4_Plots/Figure3.pdf', format='pdf')
#plt.show()



ind = np.arange(3)
width = 0.2

# Percentage more than 2 reviewers
fig4,ax = plt.subplots()
pReview_pROB_papprStudy_rel = ax.bar(ind, (pReview_rel,pROB_rel,papprStudy_rel), width)
pReview_pROB_papprStudy_nonrel = ax.bar(ind + width, (pReview_nonrel,pROB_nonrel,papprStudy_nonrel), width)
ax.set_ylabel('Percent')

ax.set_title('Relevant and Non-Relevant SRs (%)')
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(('2 or + independent reviewers', 'ROB assessment', 'High quality studies'))
ax.legend((pReview_pROB_papprStudy_rel[0], pReview_pROB_papprStudy_nonrel[0]), ('Relevant SRs', 'Non-relevant SRs'))
plt.ylim(0,100)

def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % float(height),
                ha='center', va='bottom')

autolabel(pReview_pROB_papprStudy_rel)
autolabel(pReview_pROB_papprStudy_nonrel)

fig4.savefig('/Users/federicopaoletti/Desktop/Evidence Aid/Final Report - Classification and Quality Assessment/Figure4_Plots/Figure4.pdf', format='pdf')
