# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 13:40:37 2018

@author: mxg635
"""


import os
import tkinter as tk
from tkinter import filedialog
import datetime as dt



root = tk.Tk()
root.withdraw()

infilename = filedialog.askopenfilename(title = "Pick the txt file to parse")
dir_path = filedialog.askdirectory(title = "pick the file directory") #pick 2018 or 2017



qelist = ['QE1', 'QE2', 'QE3', 'QE4', 'QE5', 'QE6', 'QE7', 'QE8', 'QE9', 'QE10']

cleanrecs = dict()
for keys in qelist:
    cleanrecs[keys]=[]#Using lists as values to keep order
injectlist = dict()#Why did I not call this injectdict?...
for keys in qelist:
    injectlist[keys]=[]


infile = open(infilename,'r') #Cleaning records
firstline = infile.readline().split('\t')
for key in cleanrecs:
    for i in range(len(firstline)):
        if firstline[i] == key:
            print(firstline[i+1])
            cleanrecs[key].append(dt.datetime.strptime(firstline[i+1], '%d-%b-%y'))#Convert to datetime since the formats differ.
    

for line in infile:
    for i in range(len(line.split('\t'))):
        
        
        for key in cleanrecs:
            if (firstline[i] == key) and (len(line.split('\t')[i+1]) > 4):
                cleanrecs[key].append(dt.datetime.strptime(line.split('\t')[i+1], '%d-%b-%y'))#All cleaning dates are now saved in the dict.

#extracting injections


for qe in qelist:
    for folder in os.listdir(dir_path):
        for secfolder in os.listdir(dir_path+'/'+folder):
            if (secfolder == qe) or (secfolder == 'MNT'):
                for files in os.listdir(dir_path+'/'+folder+'/'+secfolder):
                    if files.split('_')[1] == qe:#Need this if it goes into the MNT folder.
                        try:
                            injectlist[qe].append((dt.datetime.strptime(files.split('_')[0][:8],'%Y%m%d')))#reformat date
                        except(ValueError):
                            pass


#Counting//Printing:
outfile = open(infilename[:-4]+'2018_11_19_injrecout4.txt', 'w+')
for qe in qelist:
    outfile.write(qe+'\t'+'Cleaning date'+'\t'+'Injections since last'+'\t'+'Days since last'+'\t') #column names
outfile.write('\n')                        
                        
for keys in cleanrecs:#First cleaning // installation dates
    outfile.write('\t'+cleanrecs[keys][0].strftime('%Y%m%d')+'\t'+'\t'+'\t')
outfile.write('\n')    
   


for i in range(1,len(cleanrecs[max(cleanrecs, key= lambda x: len(cleanrecs[x]))])): #This feels so dirty :-/ - Gets length of longest valuelist from the dict
    x = 0
    for key in qelist:
        y=0
        
        if len(cleanrecs[key])>i:
            for values in injectlist[key]:
                if (values < cleanrecs[key][i]) and (values > cleanrecs[key][i-1]):#counting injections
                    y+=1        
            if x > 0:
                for k in range(x):
                    outfile.write('\t'+'\t'+'\t'+'\t')
                    x = 0
            outfile.write('\t'+str(cleanrecs[key][i].strftime('%Y%m%d'))+'\t'+str(y)+'\t'+str((cleanrecs[key][i]-cleanrecs[key][i-1]).days)+'\t') #Output format date %Y%m%d
        else:
            x += 1
    outfile.write('\n')






            
outfile.close()
infile.close()


"""
Output should be file with injections, days and dates between cleanings.
"""
