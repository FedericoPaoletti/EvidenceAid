# -*- coding: utf-8 -*-

#A simple webcrawler script that pulls all the original systematic review 
#urls from the Evidence Aid Resources website. Need to modify final urls to point
#to the full article webpage. Think about using this script to pull non-relevant 
#systematic reviews as well.

#Federico Paoletti 3/9/2017

from __main__ import *
import nltk
import urllib
from bs4 import BeautifulSoup
import copy
from copy import deepcopy

def list_webpage_urls(url): 
    
#Generates a list of all URLs from a specific webpage (the variable "url") 
    
    conn = urllib.urlopen(url)
    html = conn.read()
    soup = BeautifulSoup(html, 'lxml')
    tag_list = soup.find_all('a')

    webpage_urls = []
    for tag in tag_list:
        link = tag.get('href', None)
        if link is not None:
            #print link
            webpage_urls.append(link)
    return webpage_urls
  
def find_SR_weblink(url):  
    
#Finds the original URL for the systematic review, 
#from the Evidence Aid systematic review webpage
    
    conn = urllib.urlopen(url)
    html = conn.read()
    soup = BeautifulSoup(html, 'lxml')
    tag_list = soup.find_all('a')
    #print links
    
    key_strings = ['Read the full review here', 'Read the full review',  
    'Read the full article', 'Read the full article here','Read full article', 
    'Read the full paper', 'Read the full Review', 'Leer el artículo completo', 
    'Read the full article on EPPI and PLOS']
    
    for tag in tag_list:
        #print tag
        if tag.get_text() in key_strings:
            #print tag.get('href', None)
            return tag.get('href', None)
            
def generate_weblink_list(textlinks) :
    
#iterates find_SR_textlink over list of 
#webpage urls derived from list_webpage_urls
    
    weblinks = [None] * 1000
    for i in range(len(textlinks)): #Builds a list of all systematic review URLs from the Evidence Aid website
        print i        
        print textlinks[i]
        pin = find_SR_weblink(textlinks[i])
        if pin != None:
            print 'Found the link:'
            print pin
            if pin not in weblinks:
                weblinks[i] = pin
        else:
            print 'Could not find the link.'
            print '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% \n'
    return weblinks
            


#for SR_weblink in SR_weblink_list[:10]:
 #   if SR_weblink != None:
  #      conn = urllib.urlopen(SR_weblink)
   #     html = conn.read()
   #     soup = BeautifulSoup(html, 'lxml')
   #     #print soup
   #     SR_text = soup.get_text()
   #     print SR_text
   



#print SR_weblinks
