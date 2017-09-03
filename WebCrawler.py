# -*- coding: utf-8 -*-

#A simple webcrawler script that pulls all the original systematic review 
#urls from the Evidence Aid Resources website.

#Federico Paoletti 3/9/2017

import nltk
import urllib
from bs4 import BeautifulSoup
import copy
from copy import deepcopy

def list_webpage_urls(url): #Generates a list of all URLs from a specific webpage (the variable "url") 
    conn = urllib.urlopen(url)
    html = conn.read()
    soup = BeautifulSoup(html, 'lxml')
    links = soup.find_all('a')

    webpage_urls = []
    for tag in links:
        link = tag.get('href', None)
        if link is not None:
            #print link
            webpage_urls.append(link)
    return webpage_urls
  
def find_SR_textlink(url):  #Finds the original URL for the systematic review, from the Evidence Aid systematic review webpage
    conn = urllib.urlopen(url)
    html = conn.read()
    soup = BeautifulSoup(html, 'lxml')
    links = soup.find_all('a')
    #print links
    
    key_strings = ['Read the full review here', 'Read the full review', 'Read the full article', 'Leer el artículo completo']
    for tag in links:
        #print tag
        if tag.get_text() in key_strings:
            #print tag.get('href', None)
            return tag.get('href', None)
            
print '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'

myurl = 'http://www.evidenceaid.org/health-issues/'
SR_EAlinks = list_webpage_urls(myurl)

SR_EAlinks_cleaned = []
flag = 0
for link in SR_EAlinks: #Arbitrary conditions to clean up the SR_EAlinks list
    #print link
    if link == 'http://www.evidenceaid.org/the-methods-and-outcomes-of-cultural-adaptations-of-psychological-treatments-for-depressive-disorders/':
        flag = 1
        
    if link == 'http://www.evidenceaid.org/los-equipos-de-proteccion-individual-para-prevenir-el-contagio-de-enfermedades-muy-infecciosas-al-personal-sanitario-a-consecuencia-de-la-exposicion-a-fluidos-corporales-infectados/':
        flag = 0
        break
    
    if flag == 1:   
        SR_EAlinks_cleaned.append(link)
        #print 'Added this url.'   
       
#Remove "#" from the SR_EAlinks list:      
SR_EAlinks_cleaned2 = [url for url in SR_EAlinks_cleaned if url != '#']

SR_weblinks = []
for derived_url in SR_EAlinks_cleaned2: #Builds a list of all systematic review URLs from the Evidence Aid website
    print derived_url
    if find_SR_textlink(derived_url) != None:
        print 'Found the link:'
        print find_SR_textlink(derived_url)
        SR_weblinks.append(find_SR_textlink(derived_url))
    else:
        print 'Could not find the link.'
    print '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% \n'
    
#print SR_weblinks