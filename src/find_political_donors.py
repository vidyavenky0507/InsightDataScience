# -*- coding: utf-8 -*-
from __future__ import with_statement
from datetime import datetime
"""
Created on Sun Oct 29 20:41:26 2017

@author: vidya

input file is pipe delimited, therefore following are the fields
CMTE_ID: fields[0]
ZIP_CODE: fields[10]
TRANSACTION_DT: fields[13]
TRANSACTION_AMT: fields[14]
OTHER_ID:fields[15] we care about recods with this field empty

"""
import sys
import bisect
import statistics
import csv

#function that checks the validity of the TRANSACTION_DT field
maxyear = datetime.today().year

def is_date(string):
    try:
        if int(string[4:])>maxyear:
            raise ValueError
        string=string[:2]+"/"+string[2:4]+"/"+string[4:]
        datetime.strptime(string,'%m/%d/%Y')
        return True
    except ValueError:
        return False


#reading the input text file
WORDLIST_FILENAME = sys.argv[1]
fileHandle = open(WORDLIST_FILENAME, 'r')
#fields_1 is a dictionary for the medianvals_by date to store CMTE_ID+' '+date as a key
fields_1={}
#fields_2 is a dictionary for the medianvals_by zip to store CMTE_ID+' '+zip_code as a key
fields_2={}
#dictlist_zip has the list to be printed out to the outfile medianvals_by_zip
dictlist_zip=[]
#reads each line of the input file
for line in fileHandle:
    fields = line.split('|')
    #for part 1 
    if fields[15] == "" and len(fields[10])>5:
        # m is used as key CMTE_ID+' '+ZIP_CODE
        k=fields[0]+' '+fields[10][:5]
        if k in fields_2.keys():
            #increments the number of transactions
            fields_2[k][1]+=1
            #increments the total amount of transaction
            fields_2[k][2]+=int(fields[14])
            #adds the current amount to the list to calculate median
            
            bisect.insort(fields_2[k][3], int(fields[14]))    
   
            #calculates running median
            position=len(fields_2[k][3]);
            if len(fields_2[k][3])%2==1:
                fields_2[k][0]=round(fields_2[k][3][int(position/2)])
            else:
                fields_2[k][0]=round((fields_2[k][3][int(position/2)]+fields_2[k][3][int(position/2)-1])/2)
            #spliting the key to get CMTE_ID and ZIP_CODE
            parts=k.split(' ')
            #list (CMTE_ID,ZIP_CODE,running median,number of transactions,total amount)
            dictlist_zip.append((parts[0],parts[1],fields_2[k][0],fields_2[k][1],fields_2[k][2]))
            
        else:
	    #fields[key]=[running median,number of transaction,amount of tansaction,list of transaction amounts]
            fields_2[k]=[int(fields[14]),1,int(fields[14]),[int(fields[14])]]
	    #spliting the key to get CMTE_ID and ZIP_CODE
            parts=k.split(' ')
            #list (CMTE_ID,ZIP_CODE,running median,number of transactions,total amount)
            dictlist_zip.append((parts[0],parts[1],fields_2[k][0],fields_2[k][1],fields_2[k][2]))
     
    #for part 2    
    if fields[15] == "" and is_date(fields[13]) :
        # m is used as key CMTE_ID+' '+TRANSACTION_DT
        m=fields[0]+' '+fields[13]
        if m in fields_1.keys():
            #increments the number of transactions
            fields_1[m][0]+=1
            #increments the total amount of transactions
            fields_1[m][1]+=int(fields[14])
            #adds the current amount to the list to calculate median
            fields_1[m][2].append(int(fields[14]))
                                
        else:
            #fields[key]=[number of transactions,amount of tansaction,list of transaction amounts]
            fields_1[m]=[1,int(fields[14]),[int(fields[14])]]
                       
fileHandle.close()
#print(dictlist)

dictlist_date=[]
sortedList=[]
#convert the dictionary to list and sort the list
for key, value in fields_1.items():
    parts=key.split(' ')
    k=round(statistics.median(value[2]))
    dictlist_date.append((parts[0],parts[1], k,value[0],value[1]))
    
from operator import itemgetter
sortedList=sorted(dictlist_date, key=itemgetter(0,1))
#print(sortedList)

#writing list the out file(pipe delimited file)
with open(sys.argv[2],"w") as f:
    wr = csv.writer(f,delimiter='|')
    wr.writerows(dictlist_zip)
#writing the out file(pipe delimited file
with open(sys.argv[3],"w") as f:
    wr = csv.writer(f,delimiter='|')
    wr.writerows(sortedList)


    
    
    
