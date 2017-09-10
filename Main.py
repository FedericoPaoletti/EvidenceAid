# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 16:59:35 2017

@author: federicopaoletti
"""
import urllib
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
SR_weblink_list = generate_weblink_list(SR_EAlinks_cleaned2[:15])
print SR_weblink_list

#extract text from weblink 14 in the SR_weblink_list

if SR_weblink_list[14] != None:
    print SR_weblink_list[14]
    conn = urllib.urlopen(SR_weblink_list[14])
    html = conn.read()
    soup = BeautifulSoup(html, 'lxml')
    #print soup
    SR_text = soup.get_text()
    print SR_text
        
# save to .txt file       
        
with open('CD_test1.txt', mode='wt') as file:
    file.write(SR_text.encode('utf8'))
    
        
