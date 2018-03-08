Created on Sun Sep 10 16:59:35 2017

@author: federicopaoletti
"""
import urllib
import os
from bs4 import BeautifulSoup
from WebCrawlerFunctions import list_webpage_urls, generate_weblink_list

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
print len(SR_EAlinks_cleaned2)
SR_weblink_list = generate_weblink_list(SR_EAlinks_cleaned2)
print SR_weblink_list

#extract text from weblink 23 in the SR_weblink_list

CD_SR_weblink_list = []
nonCD_SR_weblink_list = []

for link in SR_weblink_list:
    if link is not None:  #check whether list entry is type NONE
        if '.CD' in link and 'onlinelibrary.wiley.com' in link: #check whether it is a CD link
            if 'abstract' in link:
                mod_link = link.replace('abstract', 'full') #obtain link to full article, not to abstract
                CD_SR_weblink_list.append(mod_link)
            else:
                CD_SR_weblink_list.append(link)
        else:
           nonCD_SR_weblink_list.append(link)
          
for link in nonCD_SR_weblink_list:
    if 'articles/CD' in link:
        #CD_SR_identifier = link[link.find('CD'):link.find('CD') + 8]
        #new_link = 'http://onlinelibrary.wiley.com/doi/10.1002/14651858.' + CD_SR_identifier + '.pub2/full'
        CD_SR_weblink_list.append(link)      #THESE SR LINKS ONLY CONTAIN ABSTRACTS
        
nonCD_SR_weblink_list_revised = []    
for link in nonCD_SR_weblink_list:
    if 'articles/CD' not in link:
        nonCD_SR_weblink_list_revised.append(link)
        
print CD_SR_weblink_list
counter = 0
directory_path = '/Users/federicopaoletti/Desktop/Evidence Aid/Scripts/Extracted_CDs'

for link in CD_SR_weblink_list:
    counter += 1
    conn = urllib.urlopen(link)
    html = conn.read()
    soup = BeautifulSoup(html, 'lxml')
    SR_text = soup.get_text()
    SR_text_filename = 'CD_test' + str(counter) + '.txt'
    with open(os.path.join(directory_path, SR_text_filename), mode='wt') as file:
        file.write(SR_text.encode('utf8'))
        
#conn = urllib.urlopen('http://onlinelibrary.wiley.com/doi/10.1002/14651858.CD006589.pub4/full')
#html = conn.read()
#soup = BeautifulSoup(html, 'lxml')
#    #print soup
#SR_text = soup.get_text()
#print SR_text
        
# save to .txt file       
        
#with open('CD_test25.txt', mode='wt') as file:
#    file.write(SR_text.encode('utf8'))
