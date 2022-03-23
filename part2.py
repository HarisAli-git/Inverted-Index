#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import re
import sys
import csv
import math
import numpy as np
import collections


# In[ ]:


# Part 2 ..........................

## ............. Begins Here........

### Includes:

#### 1. Inverted Index
#### 2. Faster Access to Inverted Index
#### Generating files: term_index.txt, term_info.txt


# In[ ]:


def files_reader(doc1, doc2, doc3):

    lst = []
    with open(doc3, newline = '') as files:                                                                                          
            lines = csv.reader(files, delimiter='\t')
            for line in lines:
                lst.append(line)

    dic = {}

    for x in lst:
        dic[x[0], x[1]] = x[2]

    lst = []
    with open(doc2, newline = '') as files:                                                                                          
            lines = csv.reader(files, delimiter='\t')
            for line in lines:
                lst.append(line)

    dic2 = {}

    for x in lst:
        dic2[x[0]] = x[1]
        
    lst = []
    with open(doc1, newline = '') as files:                                                                                          
            lines = csv.reader(files, delimiter='\t')
            for line in lines:
                lst.append(line)

    dic1 = {}

    for x in lst:
        dic1[x[0]] = x[1]

    return dic, dic1, dic2


# In[ ]:


def inverted_index(dic, dic1, dic2):
    
    file = open('term_index.txt', 'w', encoding='utf-8', errors='ignore')
    
    i_index = {}
    for tid in dic2:
        s = str(tid) + '\t'
        docs_count = 0
        freq = 0
        for did in dic1:
            tar = (str(did), str(tid))
            if tar in dic.keys():
                docs_count += 1
                freq += int(dic[str(did), str(tid)])
                s = s + str(did) + ':' + dic[str(did), str(tid)] + '\t'
        s = s + '\n'
        file.write(s)
        i_index[int(tid)] = (docs_count, freq)
    
    file.close()
    return i_index


# In[ ]:


def fast_access(doc):
  
    """
    returns a dict with fast access (bytes offset to each term in 'term_index.txt')
    
    """
    
    i = 0
    dic = {}
    t_len = 0
    with open(doc, 'r', encoding='utf-8', errors='ignore') as files:                                                                                          
        for file in files:
            i += 1
            t_len += len(file) + 1
            dic[i] = t_len

    return dic


# In[ ]:


def term_info(i_index, byte_offset):
    
    """
    Prepares 'term_info.txt' file
    
    """
    
    file = open('term_info.txt', 'w', encoding='utf-8', errors='ignore')
    
    for x in byte_offset:
        (a, b) = i_index[x]
        d_count, freq = (a, b)
        if x > 1:
            file.write(str(x) + '\t' + str(byte_offset[x - 1]) + '\t' + str(freq) + '\t' + str(d_count) + '\n')
        else:
            file.write(str(x) + '\t' + str(0) + '\t' + str(freq) + '\t' + str(d_count) + '\n')

    file.close()


# In[ ]:


def doc_processing():
    
    """
    Part - 2 (doc_processing):
    Calls all the functions required for Part 2
    
    """
    
    print("\tCreating Inverted Index...............!\n")
    
    #dicts after reading files
    dic, dic1, dic2 = files_reader('docids.txt','termids.txt','doc_index.txt')
    
    #inverted_index
    i_index = inverted_index(dic, dic1, dic2)
    
    #calculating the byte_offset of 'term_index.txt'
    byte_offset = fast_access('term_index.txt')

    #writing 'term_info.txt'
    term_info(i_index, byte_offset)

