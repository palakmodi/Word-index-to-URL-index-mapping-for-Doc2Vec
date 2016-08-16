# -*- coding: utf-8 -*-

"""
Created on Tue Jul 26 16:01:28 2016
@author: palak
"""

import json
import collections
import numpy as np
import math
from collections import Counter

def fileopen():
    filenames = []
    
    for i in range(0 , fileRange):
        if(i < 10) :
            file_name = "part-0000" + str(i)
            
        if(10 < i <100):
            file_name = "part-000" + str(i)
            
        if(100 < i < 1000):
            file_name = "part-00" +str(i)
            
        if(1000 < i < 10000):
            file_name = "part-0" +str(i)
            
        filenames.append(file_name)
        
    return filenames

#need to append urlCount as 2nd column of result matrix for doc2vec    
def urlCount():
    url_count_dict = {}
    countUrl = 0
    line_error = 0
    filenames = fileopen()
    
    for file_name in filenames:
        for line in open(file_name):
            try:
                line_error += 1
                json_obj = json.loads(line)
            except ValueError:
                print "JSON error at line " + str(line_error)
                continue
            url = json_obj["company_url"]
            if url not in url_count_dict:
                url_count_dict[url] = countUrl
                countUrl = countUrl + 1
    return len(url_count_dict)

    
def yearRange():
    years = []
    intyears = range(minyear,maxyear + 1)
    for e in intyears:
        years.append(str(e))
    return years

def toVector():
    url_dict = collections.OrderedDict()
    words_dict = collections.OrderedDict()
    data_word = collections.OrderedDict()
    finaldict = collections.OrderedDict()
    numberUrl = 0
    line_error = 0
    countUrl = urlCount()
    filenames = fileopen()
    years = yearRange()
    LoL = []
    for file_name in filenames:
        for line in open(file_name):
            #to handle invalid JSONs
            try:
                line_error += 1
                json_obj = json.loads(line)
            except ValueError:
                print "JSON error at line " + str(line_error)
                continue
            url = json_obj["company_url"]
            #url dicitonary url,number
            if url not in url_dict:
                url_dict[url] = numberUrl
                numberUrl = numberUrl+1
            for year in years:
                if year in json_obj:        
                    for wordItem in json_obj[year]:
                        wordItem = wordItem.lower()
                        if wordItem not in words_dict:
                            words_dict[wordItem] = countUrl
                            countUrl = countUrl + 1
                        if (url,wordItem) in data_word:
                            data_word[(url,wordItem)] += 1
                        else:
                            data_word[(url,wordItem)] = 1
                            
 # to write the matrix to the file   
            for key in data_word:
                    #out_Matrix.write("{}\t\t\t{}\t\t\t{}\n".format(url_dict.get(key[0]), words_dict.get(key[1]), data_word[key]))
                    
                    out_Words.write("{}\t\t\t{}\t\t\t{}\t\t\t{}\n".format(url_dict.get(key[0]), key[0].encode('ascii', 'ignore'), words_dict.get(key[1]), key[1].encode('ascii', 'ignore')))
            # to free up the memory
            data_word = dict()
            
    #need this count for doc2vec implementation
    #print len(words_dict) + len(url_dict)
    for k,v in url_dict.items():
        outu.write("{}\t\t\t\t\t{}\n".format(k,v))
        
 #   for k,v in words_dict.items():
  #      outw.write("{}\t\t\t\t\t{}\n".format(k,v))
        
    #out_Matrix.close()
    out_Words.close()
    
    with open('resultWords.txt','r') as f:
        #LoL=[x.strip().split('\t\t\t') for x in f]   
        for line in f:
            LoL.append(line.strip().split('\t\t\t'))
        LoL=np.transpose(LoL)
    #print LoL[3]
    #ddict= Counter(LoL[2])
    cc = urlCount()
    for x in LoL[3]:
        x = x.lower()
    wdict = Counter(LoL[3])
    upper = int(math.ceil(0.2*cc))
    
    for k,v in sorted(wdict.items()):
        if(v in range(2,upper)):
            finaldict[k] = cc
            cc = cc + 1
#    print finaldict

    for k,v in sorted(wdict.items()):
        outfreq.write("{}\t\t\t\t\t{}\n".format(k,v))
    for k,v in sorted(finaldict.items()):
        outn.write("{}\t\t\t\t\t{}\n".format(k,v))
   
    finalprint(finaldict)
    return

def finalprint(finaldict):
    filenames = fileopen()
    years = yearRange()
    line_error = 0
    numberUrl = 0
    url_dict = collections.OrderedDict()
    data_word =collections.OrderedDict()
    for file_name in filenames:
        for line in open(file_name):
            #to handle invalid JSONs
            try:
                line_error += 1
                json_obj = json.loads(line)
            except ValueError:
                print "JSON error at line " + str(line_error)
                continue
            url = json_obj["company_url"]
            #url dicitonary url,number
            if url not in url_dict:
                url_dict[url] = numberUrl
                numberUrl = numberUrl+1
            for year in years:
                if year in json_obj:        
                    for word in json_obj[year]:
                        word = word.lower()
                        if word in finaldict:
                            if (url,word) in data_word:
                                data_word[(url,word)] += 1
                            else:
                                data_word[(url,word)] = 1
            for key in data_word:
                    out_Matrix1.write("{}\t\t\t{}\t\t\t{}\n".format(url_dict.get(key[0]), finaldict.get(key[1]), data_word[key]))
                    
#                    out_Words1.write("{}\t\t\t{}\t\t\t{}\t\t\t{}\n".format(url_dict.get(key[0]), key[0].encode('ascii', 'ignore'), finaldict.get(key[1]), key[1].encode('ascii', 'ignore')))
            # to free up the memory
            data_word = dict()
    print len(finaldict) + len(url_dict)
    
    return
            
    
if __name__ == "__main__":
    #out_Matrix = open('result.txt', 'w+')
    out_Words = open('resultWords.txt','w+')
    out_Matrix1 = open('result1.txt', 'w+')
    #out_Words1 = open('resultWords1.txt','w+')
    outu = open('url','w+')
    #outw = open('words','w+')
    outn = open('nicewords','w+')
    outfreq = open('newnew','w+')
    fileRange = input('Enter the number of input files: ')
    minyear = input('Enter the year from which you want the data ')
    maxyear = input('Enter the year upto which you want the data ')
#    countUrl = urlCount()
toVector()
