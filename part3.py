#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import re
import sys
import csv
import math
import collections
from stemming.porter2 import stem

# In[ ]:

def getfreq(docid, s):

    ex = 0
    n = 0
    did = 0
    freq = 0

    for i in range(len(s)):
        if (s[i].isnumeric()):
            rem = int(s[i]) % 10
            n *= 10
            n += rem

        if (s[i] == ':'):
            did = n
            n = 0

        if (s[i] == '\t'):
            freq = n
            n = 0
            if (did == docid):
                return freq
        else:
            ex = 0

    return 0        


def open_invertIndex(offset):

    file = open('term_index.txt')
    file.seek(offset)

    lst = file.readline()

    file.close()
    
    return lst

def getOffset(tid):
    
    lst = []
    with open('term_info.txt', newline = '') as files:                                                                                          
            lines = csv.reader(files, delimiter='\t')
            for line in lines:
                lst.append(line)
                if int(line[0]) == int(tid):
                    return int(line[1])    

    print("Term not found!")
    return -1

def open_docID():

    lst = []
    with open('docids.txt', newline = '') as files:                                                                                          
            lines = csv.reader(files, delimiter='\t')
            for line in lines:
                lst.append(line)

    dic2 = {}

    for x in lst:
        dic2[x[1]] = int(x[0])
    
    return dic2

def open_docIndex(did):

    lst = []
    with open('doc_index.txt', newline = '') as files:                                                                                          
            lines = csv.reader(files, delimiter='\t')
            for line in lines:
                lst.append(line)

    dic2 = {}
    dis_terms = 0
    tot_terms = 0

    for x in lst:
        if int(x[0]) == did:
            tot_terms += 1
            if int(x[2]) == 1:
                dis_terms += 1

    return did, dis_terms, tot_terms

def open_termID():

    lst = []
    with open('termids.txt', newline = '') as files:                                                                                          
            lines = csv.reader(files, delimiter='\t')
            for line in lines:
                lst.append(line)

    dic2 = {}

    for x in lst:
        dic2[x[1]] = x[0]
    
    return dic2

def open_terminfo():
    file = 'term_info.txt'

    dict = {}
    lst = []

    with open(file, newline = '') as files:                                                                                          
        lines = csv.reader(files, delimiter='\t')
        for line in lines:
            lst.append(line)

    for x in lst:
        dict[int(x[0])] = (int(x[1]), int(x[2]), int(x[3]))
    
    return dict

def type3(term, docname):
    
    term = stem(term)

    dict = open_docID()
    dict2 = open_termID()

    did = dict[docname]
    tid = dict2[term]

    offset = getOffset(int(tid))

    rem = len(str(tid)) + 1

    slst = open_invertIndex(offset)
    freq = getfreq(int(did), slst[rem: ])

    s = '\nInverted list for term: ' + str(term) + '\n' + 'In document: ' + str(docname) + '\n' + 'TERMID: ' + str(tid) + '\n' + 'DOCID: ' + str(did) + '\n' + 'Term frequency in document: ' + str(freq) + '\n'
    print(s)

def type2(term):
    dict = open_terminfo()
    dict2 = open_termID()

    term = stem(term)
    tid = dict2[term]

    (a, b, c) = dict[int(tid)]

    offset, freq, n_docs = (a, b, c)

    s = '\nListing for term: ' + str(term) + '\n' + 'TERMID: ' + str(tid) + '\n' + 'Number of documents containing term: ' + str(n_docs) + '\n' + 'Term frequency in corpus: ' + str(freq) + '\n' + 'Inverted list offset: ' + str(offset) + '\n'
    print(s)

def type1(docname):

    dict = open_docID()
    did, dis_terms, tot_terms = open_docIndex(dict[docname])
    
    s = '\nListing for document: ' + str(docname) + '\n' + 'DOCID: ' + str(did) + '\n' + 'Distinct terms: ' + str(dis_terms) + '\n' + 'Total terms: ' + str(tot_terms) + '\n'
    print(s)

n = len(sys.argv)

if (n == 5):
    if (sys.argv[1] == '--term' and sys.argv[3] == '--doc'):
        type3(sys.argv[2], sys.argv[4])
    else:
        print("\nWrong CMD Args given. Please try again with correct args!\n")
elif (sys.argv[1] == '--term'):
    type2(sys.argv[2])
elif (sys.argv[1] == '--doc'):
    type1(sys.argv[2])
else:
    print("\nWrong CMD Args given. Please try again with correct args!\n")
