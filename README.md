# Word-index-to-URL-index-mapping-for-Doc2Vec

script.py takes input from text files which are in JSON format. The aim of the script is to output in a text file unique indices(starting from 0 to n-1) for each unique url, unique indices(starting from 0 to n-1) for unique words across all URLs+number of unique urls across all input files, frequency of each word in each URL. The output is redirected to 2 files, result.txt and resultWords.txt which has the follwing format

result.txt
urlindex    wordindex+number of unique URLs     frequency
32		45					3
32		2					10
108		2					15

resultWords.txt
url Index	url				wordindex+number of unique urls		word
32		https://www.google.com		45					search
32		https://www.google.com		2					images
108		https://www.facebook.com/	2					images

result.txt contains the relationship between the urls, words and frequency all in numeric format. result.txt is used as a input for an implemetation of word2vec/doc2vec by Linhong Zhu https://github.com/linhongseba's word2vec/doc2vec. resultWords.txt is used to map back the numeric representation to actual values of urls and words respectively.

Usage:
script.py: Python script file for Word-index-to-URL-index-mapping-for-Doc2Vec
result.txt: Output file in matrix form, as described above
resultWords.txt: Output file with (key, value) pair as described above
