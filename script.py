# -*- coding: utf-8 -*-

import json
import datetime
def fileopen():
    filenames=[]
    for i in range(0,fileRange):
        if(i<10):
            file_name = "part-0000" + str(i)
        if(10<i<100):
            file_name = "part-000" + str(i)
        if(100<i<1000):
            file_name = "part-00" +str(i)
        if(1000<i<10000):
            file_name = "part-0" +str(i)
        filenames.append(file_name)
    return filenames

#need to append urlCount as 2nd column of result matrix for doc2vec    
def urlCount():
    url_count_dict={}
    countUrl=0
    line_error=0
    filenames=fileopen()
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
                url_count_dict[url]=countUrl
                countUrl=countUrl+1
            url_count_dict=dict()
    return countUrl

def yearRange():
    years=[]
    datetime.MINYEAR=1996
    datetime.MAXYEAR=2017
    intyears= range(datetime.MINYEAR,datetime.MAXYEAR)
    for e in intyears:
        years.append(str(e))
    return years
    
def toVector():
    url_dict={}
    words_dict={}
    data_word = {}  
    numberUrl=0
    numberWord=0
    line_error=0
    filenames=fileopen()
    years=yearRange()
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
                url_dict[url]=numberUrl
                numberUrl=numberUrl+1
            for year in years:
                if year in json_obj:        
                    for wordItem in json_obj[year]:
                        wordItem = wordItem.lower()
                    #word dictionary word, number
                        if wordItem not in words_dict:
                            words_dict[wordItem]=numberWord
                            numberWord=numberWord+1
                    #counting the frequency of word and assigns url,word key to data_matrix dictionary    
                        if (url,wordItem) in data_word:
                            data_word[(url,wordItem)] += 1
                        else:
                            data_word[(url,wordItem)] = 1
            # to write the matrix to the file    
            for key in data_word:
                    out_Matrix.write("{}\t\t\t{}\t\t\t{}\n".format(url_dict.get(key[0]), words_dict.get(key[1])+countUrl, data_word[key]))
                    out_Words.write("{}\t\t\t{}\t\t\t{}\t\t\t{}\n".format(url_dict.get(key[0]), key[0].encode('ascii', 'ignore'), words_dict.get(key[1])+countUrl, key[1].encode('ascii', 'ignore')))
            # to free up the memory
            data_word = dict()
    #need this count for doc2vec implmentation
    print len(words_dict)+len(url_dict)
    out_Matrix.close()
    out_Words.close()
    return

if __name__ == "__main__":
    out_Matrix = open('result.txt', 'w+')
    out_Words = open('resultWords.txt','w+')
    fileRange = input('Enter the number of input files: ')
    countUrl=urlCount()
    toVector()