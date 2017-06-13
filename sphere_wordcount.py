import nltk, pylab
from nltk.probability import FreqDist
from nltk.corpus import PlaintextCorpusReader
from pylab import *

corpus_root = '/Users/federicopaoletti/Desktop/Evidence Aid/Scripts/TextDirectory'
wordlists = PlaintextCorpusReader(corpus_root, 'Sphere_Handbook_2011_English.pdf_ONLINECONVERSION.*')
sphere_wordlist = wordlists.words()

sphere_freq = FreqDist([mean_words.lower() for mean_words in sphere_wordlist if mean_words.isalpha() and len(mean_words) > 6])
sphere_freq.plot(50)
