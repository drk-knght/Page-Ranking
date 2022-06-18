import nltk
import trie
import json
import numpy as np

from nltk.stem import PorterStemmer
from trie import TrieNode
from trie import Trie

class QueryHandler:
    """Class designed to handle the queries given by the user."""
    def __init__(self):
        """Constructor for the class. Initializes the threshold, stemmer and the inverted index table."""
        self.threshold = 5
        self.trie = Trie()
        self.stemmer = PorterStemmer()
        self.invertedTable = json.loads(open('Inverted Index Table.txt', 'r').read())   # Opens file made in preprcessor called Inverted Index Table
        self.invertedTable[''] = []
        self.fileNames = json.loads(open('File Names.txt', 'r').read())
        self.documentNumber = self.invertedTable["totalNumberOfDocuments"][0]
        self.documentList = []                                                          # Initializing documentList to null list

        for i in range(self.documentNumber):                                            # Forming list of documents
            self.documentList += [i + 1]
        self.documentList = set(self.documentList)

        for word in self.invertedTable:
            word += '$'                                                                 # Adding char $ at the end of the word
            for i in range(len(word)):
                self.trie.insert(self.rotate(word, i))                                  # Rotaing word i times

    def rotate(self, word : str, n : int) -> str:
        """Function used to rotate a string."""
        return word[n:] + word[0:n]

    def levenshteinDistance(self, source : str, target : str) -> int:
        """Function to calculate the Levenshtein (Edit) Distance between 2 words."""
        distance = np.zeros((len(source) + 1, len(target) + 1))                         # Forming 2D list called distance

        for i in range(len(source) + 1):                                                # Initializing Row 0 with the value of the column
            distance[i][0] = i

        for i in range(len(target) + 1):                                                # Initializing Column 0 with the value of the row
            distance[0][i] = i

        for i in range(1, len(source) + 1):
            for j in range(1, len(target) + 1):
                if (source[i-1] == target[j-1]):
                    distance[i][j] = distance[i - 1][j - 1]                             # If the previous words are equal, following words will also be equal 
                else:
                    distance[i][j] = min(distance[i - 1][j - 1], distance[i - 1][j], distance[i][j - 1]) + 1    # Using levenshtein Distance formula 
                    
        return int(distance[len(source)][len(target)])

    def boolQuery(self, query : str) -> list:
        """Function designed to handle boolean queries made by the user."""
        query = '(' + query + ')'                                           # Adding brackets to the query
        operatorStack = []                                                  # Intializing operactorStack with null list
        operandStack = []                                                   # Intializing operandStack with null list
        operators = ['AND', 'OR', 'NOT']                                    
        token = ''
        
        for j in range(len(query)):
            if query[j] == '(':                                             # For every ( in the query add it to operatorStack
                operatorStack += ['(']
                
            elif query[j] == ')':                                           # For every ) in the query 
                if token != '':                                             # If token is not equal to space
                    if token in operators:                                  # And token is equal to one of the operators mentioned add it to operatorStack
                        operatorStack.append(token)
                    else:
                        operandStack.append(token)                          # Otherwise add it to the operandStack
                token = ''
                    
                while operatorStack[len(operatorStack) - 1] != '(':
        
                    operator = operatorStack[len(operatorStack) - 1]        # Intialize operator with the last element from operatorStack
                    operatorStack.pop()

                    operand1 = operandStack[len(operandStack) - 1]          # Intialize operand1 with the last element from operandStack
                    operandStack.pop()

                    operand2 = ''                                               

                    if operator != 'NOT':                                   # For operators AND and OR we will take one more operand
                        operand2 = operandStack[len(operandStack) - 1]      # Intialize operand2 with the last element from operandStack
                        operandStack.pop()
                        
                    operandStack.append('ResultOfStackOperation' + str(j))

                    # Stemming Operand1 and Operand2
                    operand1 = self.stemmer.stem(operand1)
                    operand2 = self.stemmer.stem(operand2)
                    
                    if operand1 not in self.invertedTable:                          # Correcting operand1 if we can't find it in the invertedTable
                        minDist = 1000
                        maxFreq = 0
                        correctedWord = ''
                        for word in self.invertedTable:
                            distance = self.levenshteinDistance(operand1, word)     # Finding edit distance between operand1 and the words in invertedTable 
                            freq = len(self.invertedTable[word])

                            if (distance < minDist or (distance == minDist and freq > maxFreq)) and distance < self.threshold:      # Correct operand1 iff its edit distance is less than threshold
                                minDist = distance
                                maxFreq = freq
                                correctedWord = word
                        print('Corrected ' + operand1 + ' to ' + correctedWord)
                        operand1 = correctedWord
                                
                    docList1 = set(self.invertedTable[operand1]) if operand1 != '' else set([])
                        
                    if operand2 != '':
                        if operand2 not in self.invertedTable:                      # Correcting operand2 if we can't find it in the invertedTable
                            minDist = 1000
                            maxFreq = 0
                            correctedWord = ''
                            for word in self.invertedTable:
                                distance = self.levenshteinDistance(operand2, word)         # Finding edit distance between operand2 and the words in invertedTable 
                                freq = len(self.invertedTable[word])

                                if (distance < minDist or (distance == minDist and freq > maxFreq)) and distance < self.threshold:      # Correct operand2 iff its edit distance is less than threshold
                                    minDist = distance
                                    maxFreq = freq
                                    correctedWord = word
                            print('Corrected ' + operand2 + ' to ' + correctedWord)
                            operand2 = correctedWord

                    docList2 = set(self.invertedTable[operand2]) if operand2 != '' else set([])

                    if operator == 'AND':                                                                                                           # Finding intersection incase of AND 
                        self.invertedTable[self.stemmer.stem('ResultOfStackOperation' + str(j))] = list(docList1.intersection(docList2))
                    elif operator == 'OR':                                                                                                          # Finding union incase of OR
                        self.invertedTable[self.stemmer.stem('ResultOfStackOperation' + str(j))] = list(docList1.union(docList2))
                    else:                                                                                                                           # Finding difference incase of NOT
                        self.invertedTable[self.stemmer.stem('ResultOfStackOperation' + str(j))] = list(self.documentList.difference(docList1))     
                        
                operatorStack.pop()

            elif query[j] == ' ':
                if len(token) == 0:
                    continue

                if token in operators:
                    operatorStack.append(token)
                else:
                    operandStack.append(token)
                token = ''

            else:
                token += query[j]

        print()
        
        key = self.stemmer.stem(operandStack[0])
        if key not in self.invertedTable:                               # Correcting key if we can't find it in the invertedTable
            minDist = 1000
            maxFreq = 0
            correctedWord = ''
            for word in self.invertedTable:
                distance = self.levenshteinDistance(key, word)          # Finding edit distance between key and the words in invertedTable
                freq = len(self.invertedTable[word])

                if (distance < minDist or (distance == minDist and freq > maxFreq)) and distance < self.threshold:      # Correct key iff its edit distance is less than threshold
                    minDist = distance
                    maxFreq = freq
                    correctedWord = word
            print('Corrected ' + key + ' to ' + correctedWord)
            key = correctedWord

        docNames = []
        docNames = self.invertedTable[key].copy()
        for i in range(len(docNames)):
            docNames[i] = self.fileNames[str(docNames[i])]
        return docNames

    def wildcardQuery(self, query : str) -> list:
        """Function designed to handle wildcard queries made by the user."""
        return self.trie.wildcardHandler(query)                 # Calling WildCard Handler for the given query





