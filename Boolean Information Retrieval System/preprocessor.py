import time
import nltk
import os
import json
import tkinter as tk

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from tkinter import filedialog

"""This module pre-processes all the documents in a given directory and outputs 2 files - An inverted index table and a hashtable for the file names."""

root = tk.Tk()
root.withdraw()
# Selecting the folder with all the documents
directory = filedialog.askdirectory()

start_time = time.time()

invertedTable = {}
fileNames = {}
stopwords_ = stopwords.words('english')
documentNumber = 0

# Loop to create a Hash table for filename and assigning an index to each file

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f):
        documentNumber += 1
        fileNames[documentNumber] = str(filename)
        
        filename = directory + '/' + filename
        file = open(filename, "r")
        # Printing the document number of files opened
        print(str(documentNumber))
        
        content = file.read()
        extracted = []
        # Tokenizing the words extracted from the document
        words = nltk.word_tokenize(content)
        stemmer = PorterStemmer()
        #Removing all the stopwords
        for word in words:
            if word not in stopwords_:
                extracted += [stemmer.stem(word)]

        extracted = list(set(extracted))

        for word in extracted:
            if word not in invertedTable:
                invertedTable[word] = [documentNumber]
            else:
                invertedTable[word] += [documentNumber]

invertedTable['totalNumberOfDocuments'] = [documentNumber]

with open('Inverted Index Table.txt', 'w') as convert_file:
    convert_file.write(json.dumps(invertedTable))

with open('File Names.txt', 'w') as convert_file:
    convert_file.write(json.dumps(fileNames))

print("--- %s seconds ---" % (time.time() - start_time))


