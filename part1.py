
# In[ ]:


import os
import re
import sys
import csv
import math
import numpy as np
import collections


# In[ ]:


from bs4 import BeautifulSoup
from stemming.porter2 import stem


# # Part 1.............
# ## Begins Here........
# 
# ### Includes: 
# #### 1. Getting all files in the directory
# #### 2. Parsing the files with the HTML parser library
# #### 3. Tokenizing the text
# #### 4. Converting Tokens in lowercase
# #### 5. Removing Stop Words
# #### 6. Applying Stemming
# #### 7. Generating files: docids.txt, termids.txt, doc_index.txt

# In[ ]:


#------------Getting Files block--------------#


def getFiles(dir):
    
    """
    get files present in the given directory
    
    """

    files = []
    for file in os.listdir(dir):
        files.append(file)
    return files


# In[ ]:


#------------HTML parsing block--------------#

def removeRem(parsed):
    """
    Remove unnecessary spaces and characters left after doing html parsing

    """        
    parsed = parsed.replace('\n', ' ')
    parsed = parsed.replace('\\n', ' ')
    parsed = parsed.replace('\t', '')
    parsed = parsed.replace('\\t', '')
    parsed = parsed.replace('\xa0', '')
    parsed = parsed.replace('\\xa0', '')
    parsed = parsed.replace('\'', '')
    parsed = parsed.replace('\\\'', '')
    
    return parsed

def parseHtml(dir):
    """
    Beautiful Soup used for HTML parsing
    Code help taken from stackoverflow

    """
    try:
        text_html = open(dir, 'r', encoding='utf-8').read()
    except:
        try :
            text_html = open(dir, 'r', encoding='windows-1252').read()
        except:
            try:
                text_html = open(dir, 'r', encoding='utf8').read()
            except:
                text_html = open(dir, 'r', encoding='latin-1').read()
                
    bs4 = BeautifulSoup(text_html, "html.parser")

    for script in bs4(["script", "style"]):
        script.extract()

    parsed = bs4.get_text()
    parsed = parsed.encode('cp437', 'replace')
    parsed = parsed.decode('cp437')

    parsed  = removeRem(parsed)

    return parsed

def getParsedDocs(dir, files):
    dc = []
    for file in files:
        dc.append(parseHtml(dir + "\\"+ file))
    return dc


# In[ ]:


#------------Tokenization block--------------#

def tokenize(p_txt):
    """
    takes all of the text and concerts it into tokens
    
    """ 
    
    tokens=[]
    
    for txt in p_txt:
        token = re.findall(r'\w+', txt)
        tokens.append(token)
    
    return tokens

def lowerCase(tokens):
    """
    switch all tokens to lowercase
    
    """
    return [[w.lower() for w in a] for a in tokens]

def tokenization(p_txt):
    
    """
    calls functions to tokenize and then lowercase the tokens
    
    """
    
    tokens = tokenize(p_txt)
    
    return lowerCase(tokens)


# In[ ]:


#------------Stopwords Removal block--------------#

def removeNextLineChar(text):
    """
    Removes '\n' character after every word in given list
    
    """
    # An dict for stopwords tokens
    lst = {}

    for word in text:
        # We have to ignore the last character from every word
        # as it contains '\n'
        word = word[:-1]
        lst[word] = 1
    
    return lst

def RemoveStopWordsfromTK(stopwords, tokens):
    
    """
    Stop Words Removal from given list of tokens
    
    """
    pool = []
    
    for token in tokens:
        for word in token:
            if word in stopwords.keys():
                token.remove(word)
        pool.append(token)
        
    return pool

def StopWordsRem(file, tokens):

    # Reading the stoplist.txt file
    text = file.readlines()
    
    stopwords = removeNextLineChar(text)

    pool = RemoveStopWordsfromTK(stopwords, tokens)
         
    return pool


# In[ ]:


#------------Stemming block--------------#

def stemming(tokens):
    
    """
    Applies Stemming to tokens
    
    """
    my_dict = {}
    
    for x in tokens:
        k = stem(x)
        if k in my_dict.keys():
            my_dict[k] = my_dict[k] + 1
        else:
            my_dict[k] = 1
            
    return my_dict


# In[ ]:


#------------Doc1 : docsid.txt block--------------#

def assignID(files):
    
    """
    Creates a file mapping to document's filename (without path)
    
    """
    
    my_dic = []
    i = 1
    
    print("\t\tAssigning DOC IDs.........! \n")
    
    for file in files:
        my_dic.append({file : i})
        i += 1
    
    return my_dic

def WriteToFile(files, my_dic, doc1):
    
    """
    Writing the prepared dictionary to the file
    
    """
    
    i = 0
    
    print("\t\tTokenizing File............! \n")
    
    for file in files:
        doc1.write(str(my_dic[i][file]) + '\t' + file + "\n")
        i += 1
    
def doc1(files):
    
    """
    Prepares 'docsid.txt' file
    
    """
    
    doc1 = open('docids.txt', 'w', encoding='utf-8', errors='ignore')
    
    dic = assignID(files)
    WriteToFile(files, dic, doc1)


# In[ ]:


#------------Doc2 : termids.txt block--------------#

def mergeListD(lst_d): #reference stackoverflow

    """
    Merges dictionaries in the list in a single one
    
    """
    
    d = {}
    
    for x in lst_d:
        for key in x:
            if key in d.keys():
                d[key] = d[key] + x[key]
            else:
                d[key] = x[key]
    
    return d
    
def assignttermID(pool, file):
    
    """
    Creates a file mapping to document's filename (without path)
    
    """
    
    n = 0
    
    n_dict = {}
    
    print("\tAssigning Term IDs.......!\n")
    
    for key in pool:
        n += 1
        n_dict[key] = n    
        WriteToTermFile(file, n, key)
    
    return n_dict
        
def WriteToTermFile(file, n, term):
    
    """
    Writing the ids to the file
    
    """
    
    file.write(str(n) + '\t' + term + "\n")
    
def doc2(s_arrd):
    
    """
    Prepares 'termids.txt' file
    
    """
    
    #Merge Dictionaries
    
    new_dict = {}
    
    new_dict = mergeListD(s_arrd)
            
    doc2 = open('termids.txt', 'w', encoding='utf-8', errors='ignore')
    
    n_dict = assignttermID(new_dict, doc2)
    
    return new_dict, n_dict


# In[ ]:


#------------Doc3 : doc_index.txt block--------------#
    
def doc3(single_dict, s_arrd, n_dict):
    
    """
    Prepares 'doc_index.txt' file
    
    """
    
    file = open('doc_index.txt','w', encoding='utf-8', errors='ignore')
            
    #return the pool of words after removing the duplicates for further processing
   
    doc_id = 1
    flag = False

    doc_index = {}
    
    for dicts in s_arrd:
        for key in dicts:
            doc_index[(doc_id, n_dict[key])] = dicts[key]
            
        doc_id += 1
    
    ordered_dict = collections.OrderedDict(sorted(doc_index.items()))
    
    for k, v in ordered_dict:
        string = str(k) + '\t' + str(v) + '\t' + str(ordered_dict[(k, v)]) + '\n'
        file.write(string)
    
    file.close()
    return ordered_dict


# In[ ]:


def inverted_index(n_dict, s_arrd):
    
    """
    generates inverted_index.txt
    
    """
    
    file = open('term_index.txt', 'w', encoding='utf-8', errors='ignore')
    
    doc_id = 0
    for x in n_dict:
        s = str(n_dict[x]) + '\t' 
        for dicts in s_arrd:
            doc_id += 1
            if x in dicts.keys():
                s = s + str(doc_id) + ':' + str(dicts[x]) + '\t'
        s = s + '\n'
        file.write(s)
        doc_id = 0
        
    file.close()


# In[ ]:


#------------Part1 : Tokenizer (Caller Function)--------------#

def tokenizer():
    
    """
    Part - 1 (Tokenizer):
    Calls all the functions required for Part 1
    
    """
    
    dir = r"C:\Users\haris\Documents\IR\A - 1\corpus"

    file = open ("C:/Users/haris/Downloads/stoplist.txt","r")
    
    #Creating doc1 : docsid.txt
    doc1(getFiles(dir))
    
    #Getting all the files in the provided Directory
    files = getFiles(dir)
    
    #Parsing with HTML library
    text = getParsedDocs(dir, files)
    
    #Tokinzation
    token_text = tokenization(text)
    
    tk_pool = token_text
    
    #Stopwords Removal
    stop_pool = StopWordsRem(file, token_text)
    
    #Stemming
    
    stem_pool = []
    for x in stop_pool:
        stem_pool.append(stemming(x))
        
    n_dict = {}
    s_arrd = stem_pool
    single_dict, n_dict = doc2(s_arrd)
    
    doc_index = doc3(single_dict, s_arrd, n_dict)

