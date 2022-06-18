import query
import nltk
import numpy as np

from query import QueryHandler

q = QueryHandler()

accept = 'y'
wild = False

while accept == 'y':
    wild = False
    answer = []
    query = input('\nEnter the Boolean / Wildcard query:\n')
    for char in query:                                          # If the query includes * it will be wildcard query otherwise boolean query
        if char == '*':
            wild = True
            answer = q.wildcardQuery(query)                     # Finding words for the the wildcard query
            print(answer)
            break

    if wild == False:
        answer = q.boolQuery(query)                             # Finding documents satisfying boolean querycd
        print(answer)
    accept = input('\nDo you want to enter another query? (y/n):\n')
