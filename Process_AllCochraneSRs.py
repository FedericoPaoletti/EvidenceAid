"""
Created on Mon Nov 20 10:21:54 2017

@author: pante_000
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 23:12:28 2017

@author: pante_000
"""
from bs4 import BeautifulSoup
#import string
import pandas as pd

# fnd desired text string
def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

    # main function 
def PreProcess(Fl_name):
    #create list for parsing
    Ab_list=["Background:","Objectives:","Search methods:","Selection criteria:",\
    "Data collection and analysis:", "Main results:","Authors' conclusions:", "US:"] 
    #create list for data frame names
    Ab_list2=["ID","Title","Background","Objectives","Search methods","Selection criteria",\
    "Data collection and analysis", "Main results","Authors' conclusions",  "US"]
    #Fl_name= full path name -set in All-files
    #file = open(Fl_name,'r',encoding="utf8")
    file = open(Fl_name,'r',encoding="latin-1")
    Raw_Doc=file.read()    
    #remove html characters
    Document1 = BeautifulSoup(Raw_Doc,"lxml").text
     #create dataframe
    df = pd.DataFrame(columns=[Ab_list2[0:len(Ab_list2)-1]])
    # create conditional argument
    temp_var=0; temp_var2=0; empty_var=0;temp_start=0; temp_end=0;
    counter=0 # indicate starting review
    counter2=0 # dataframe row counter to add each review
    Upper_loop_limit=counter+10000# indicate ending review or set to  > max
    
    while (True):

#            # Get Abstract
        #temp_var=find_nth(Document1, "ID:", counter+1);
        if (empty_var==1):
            temp_var2=temp_end-10
        temp_start=Document1.find("Record #", temp_var2); #locate the next ID
        temp_var=Document1.find("ID:", temp_start); temp_var2= Document1.find("AU:", temp_var);  
          
        Identity=Document1[temp_var+len("ID:"):temp_var2].strip()
        
        temp_var=Document1.find("TI:", temp_var2);  temp_var2= Document1.find("SO:", temp_var);     
        Title=Document1[temp_var+len("TI:"):temp_var2].strip()
        #Title+="."
        temp_var=Document1.find(Ab_list[0], temp_var2); temp_var2= Document1.find(Ab_list[1], temp_var); 
        BackGround=Document1[temp_var+len(Ab_list[0]):temp_var2].strip()
        temp_var=temp_var2; temp_var2= Document1.find(Ab_list[2], temp_var);  
        Objective=Document1[temp_var+len(Ab_list[1]):temp_var2].strip()
        
        temp_var=temp_var2; temp_var2= Document1.find(Ab_list[3], temp_var);  
        S_methods=Document1[temp_var+len(Ab_list[2]):temp_var2].strip()
        
        temp_var=temp_var2; temp_var2= Document1.find(Ab_list[4], temp_var);  
        S_criteria=Document1[temp_var+len(Ab_list[3]):temp_var2].strip()
        
        temp_var=temp_var2; temp_var2= Document1.find(Ab_list[5], temp_var);  
        D_col=Document1[temp_var+len(Ab_list[4]):temp_var2].strip()
        
        temp_var=temp_var2; temp_var2= Document1.find(Ab_list[6], temp_var);  
        M_results=Document1[temp_var+len(Ab_list[5]):temp_var2].strip()
        
        temp_var=temp_var2; temp_var2= Document1.find(Ab_list[7], temp_var);  
        A_Conclusion=Document1[temp_var+len(Ab_list[6]):temp_var2].strip()
        
        if (temp_var2==-1 or counter==Upper_loop_limit):
            print (counter)
            break
        else:
#        #create a matrix of output variables
            output_mat=[Identity,Title,BackGround,Objective,S_methods,S_criteria,D_col,M_results,A_Conclusion]    
            temp_end=Document1.find("Record #", temp_start+10);
            if temp_var2>temp_end and temp_end>0:
                output_mat=[Identity,"empty","empty","empty","empty","empty","empty","empty","empty"]
                empty_var=1
            for ii in range (len(Ab_list2)-1):
                df.loc[counter2,Ab_list2[ii]]=output_mat[ii]
        counter+=1
        counter2+=1
        #print (A_Conclusion)
    #save to dataframe
    df.to_csv('C:/Users/pante_000/Desktop/DataFrame1.csv')

#add full file name + path
Fl_name = 'C:/Users/pante_000/Desktop/All_Cochrane_Reviews.txt' # All_Cochrane_Reviews, SearchString2_Result
PreProcess(Fl_name)

##Apply the script to all files in the rootdir folder
#def All_Files(): 
#    rootdir = 'C:/Users/pante_000/Desktop/non_rel'  # ADD HERE THE PATH WHERE THE RAW FILES ARE PRESENT
#
#    for subdir, dirs, files in os.walk(rootdir):
#        for file in files:
#            Fl_name=os.path.join(subdir, file)           
#            PreProcess(Fl_name,file)
#            break     
#All_Files()
