import nltk
from nltk.stem import PorterStemmer
# Rotating word letter by letter n times
def rotate(word : str, n : int) -> str:
    """Function used to rotate a string"""
    return word[n:] + word[0:n]

# Defining trie node 
class TrieNode:
    """Describes the structure of a node of the trie."""
    def __init__(self):
        """Constructor for the node."""
        self.children = {}              # Intializing children as empty dicitionary
        self.endOfWord = False          # Intializing end of the word as false until specified otherwise

class Trie:
    """Describes the structure of a trie."""
    def __init__(self):
        """Constructor for the trie."""
        self.root = TrieNode()          # Intializing root of trie 

    def insert(self, word : str) -> None:
        """Function to insert a node into the trie."""
        currentNode = self.root         # Pointing currentNode of the Trie

        for char in word:
            if char not in currentNode.children:            # if the char is not in the trie already,create a new node for that char
                currentNode.children[char] = TrieNode()
            currentNode = currentNode.children[char]        # if the char is available in the trie,go to that node
        currentNode.endOfWord = True                        # for the last char of the word make the endOfWord True

    def getWords(self, prefix : list, currentNode : TrieNode, answer : list) -> None:
        """Function to return a set of words from the trie."""
        if currentNode.endOfWord:                               # it checks if the given query is a word 
            answer += [''.join(prefix)]                         # if yes it adds the word to the answer list

        for char, nextNode in currentNode.children.items():     # checks if it has any children
            prefix.append(char)
            self.getWords(prefix, nextNode, answer)             # runs again to check if the children form a word
            prefix.pop()

    def startsWith(self, word : str) -> list:
        """Function to check if a given prefix is in the trie. Also calls getWords()."""
        currentNode = self.root     

        for char in word:
            if char in currentNode.children:
                currentNode = currentNode.children[char]    # if the node has children, we update the currentNode with the location of the children
            else:
                return []                                   # if not we return empty list

        answer = []                                         # intialize answer with empty list
        self.getWords(list(word), currentNode, answer)
        return answer

    def wildcardHandler(self, query : str) -> list:
        """Function to handle wildcard query searches."""
        stemmer = PorterStemmer()
        query = stemmer.stem(query)                     # Stemming the query
        query += '$'                                    # Adding char $ at the end of the query
        for i in range(len(query)):
            if query[i] == '*':                         # Finding the position of * in the query 
                break
        query = rotate(query, i + 1)                    # Rotate the word to get * char at the end
        query = query[0:len(query) - 1]                 # Removing *
        
        answer = self.startsWith(query)                 # Finding words starting with the query
        finalAnswer = []                                # Initializing finalAnswer with empty list

        for word in answer:
            for i in range(len(word)):                  # Find the position of $ in the query
                if word[i] == '$':
                    break
            word = rotate(word, i + 1)                  # Rotating it to get $ at the end
            word = word[0:len(word) - 1]                # Removing $
            finalAnswer += [word]                       # Adding the word to finalAnswer
        return finalAnswer
