Created on Thu Oct 19 23:12:28 2017

@author: pante_000
"""
from bs4 import BeautifulSoup
import string
import os
import pandas as pd

# fnd desired text string
def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

    # main function 
def PreProcess_Rel(Fl_name):
    #Fl_name= full path name -set in All-files
    file = open(Fl_name,'r',encoding="utf8")
    printable = set(string.printable)
    printable.add('≤'); printable.add('≥');printable.add('®')
    Raw_Doc=file.read()
    
    #remove html characters
    #PrintDoc=''.join(list(filter(lambda x: x in printable, Raw_Doc)))
    Document1 = BeautifulSoup(Raw_Doc,"lxml").text
    
    # Get Title
    Title=Document1[0:Document1.find(' -')].strip();
      
    # Get Abstract
    Ab_list=["Background","Objectives","Search methods","Selection criteria",\
    "Data collection and analysis", "Main results","Authors' conclusions", "Plain language summary"]
   
    #separate Abstract
    Identity=Document1[ find_nth(Document1, ".CD", 1)+1: find_nth(Document1, ".CD", 1)+9].strip();
    
    test_var=  find_nth(Document1, Ab_list[2], 1) -  find_nth(Document1, Ab_list[0], 2);
    test_var2=find_nth(Document1, Ab_list[0], 2)
    if test_var<0 or test_var2==-1:
         var1=1; var2=1;   
    else:
        var1=1; var2=2; 
       
    BackGround=Document1[find_nth(Document1, Ab_list[0], var2)+len(Ab_list[0]):find_nth(Document1, Ab_list[1], var2)].strip();
    Objective=Document1[find_nth(Document1, Ab_list[1], var2)+len(Ab_list[1]):find_nth(Document1, Ab_list[2], var1)].strip();
    S_methods=Document1[find_nth(Document1, Ab_list[2], var1)+len(Ab_list[2]):find_nth(Document1, Ab_list[3], var1)].strip();
    S_criteria=Document1[find_nth(Document1,Ab_list[3], var1)+len(Ab_list[3]):find_nth(Document1, Ab_list[4], var1)].strip();
    D_col=Document1[find_nth(Document1, Ab_list[4], var1)+len(Ab_list[4]):find_nth(Document1, Ab_list[5], var1)].strip();
    M_results=Document1[find_nth(Document1, Ab_list[5], var1)+len(Ab_list[5]):find_nth(Document1, Ab_list[6], var2)].strip();
    A_Conclusion=Document1[find_nth(Document1, Ab_list[6], var2)+len(Ab_list[6]):find_nth(Document1, Ab_list[7], var1)-1].strip();
    
    # find where foreign letters start
    for i in range(len(A_Conclusion)):
        if A_Conclusion[i] not in printable:
            #print (A_Conclusion[i])
            break
    #get conclusion 
    A_Conclusion2= Document1[find_nth(Document1, Ab_list[6], var2)+len(Ab_list[6]):\
    find_nth(Document1, Ab_list[6], var2)+len(Ab_list[6])+i].strip();
    
    #remove .excess
    A_Conclusion2=A_Conclusion2[0:A_Conclusion2.rfind('.')];
    
    #create a matrix of output variables
    All_vars=[Identity,Title,BackGround,Objective,S_methods,S_criteria,D_col,M_results,A_Conclusion2]
    #print (A_Conclusion2)
    return All_vars

# example of running the function 
PreProcess_Rel('C:/Users/pante_000/Desktop/Evidence_aidPython/RelevantRaw/CD_test192.txt')

# test139
#Apply the script to all files in the rootdir folder

def All_Files(): 
    rootdir = 'C:/Users/pante_000/Desktop/Evidence_aidPython/RelevantRaw'  # ADD HERE THE PATH WHERE THE RAW FILES ARE PRESENT
    Ab_list=["Identity","Title","Background","Objectives","Search methods","Selection criteria",\
    "Data collection and analysis", "Main results","Authors' conclusions", "Plain language summary"]
    counter=0
    #create dataframe
    df = pd.DataFrame(columns=[Ab_list[0:len(Ab_list)-1]])
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            Fl_name=os.path.join(subdir, file) 
            output_mat=PreProcess_Rel(Fl_name)
            #print(output_mat[7],'\n',file)
            for ii in range (len(Ab_list)-1):
                df.loc[counter,Ab_list[ii]]=output_mat[ii]
            print (Fl_name,counter)
            counter+=1
     # ADD HERE THE OUTPUT FILE  PATH  
    df.to_csv('C:/Users/pante_000/Desktop/Evidence_aidPython/DataFrame1.csv')
    #returns the dataframe
    print (counter)
    return df 
All_Files()
