import networkx as nx
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
string.punctuation


stop=stopwords.words('english')
lemmatizer=WordNetLemmatizer()

def PreProcess_Text(str):
    list=""
    ## Lower Casing and Removing Punctuation ##
    str=str.lower()
    s=string.punctuation
    for x in str:
        if s.find(x)>=0:
            list=list+" "
        else:
            list=list+x
    
    list=lemmatizer.lemmatize(list)
    
    ## tokenization ##
    tokenized_text=nltk.word_tokenize(list)
    
    ## Stopwords Removal ##
    tokenized_text=[i for i in tokenized_text if i not in stop]
    
    return tokenized_text

web_graph=nx.read_gpickle("web_graph.gpickle")



inverted_dictionary={}
for i in range(len(web_graph.nodes)):
    web_graph.nodes[i]['page_content']=PreProcess_Text(web_graph.nodes[i]['page_content'])
    for j in web_graph.nodes[i]['page_content']:
        lis=web_graph.nodes[i]['page_content']
        if j not in inverted_dictionary:
            inverted_dictionary[j]=[]
        inverted_dictionary[j].append(i)
    

# print(inverted_dictionary)


while True:
    str=input('Enter the query: ')
    str=str.lower()
    actual_node=inverted_dictionary[str]
    list_len=len(actual_node)
    final_nodes=actual_node.copy()
    print("Root set:",end=" ")
    print(actual_node)

    for x in actual_node:

        if web_graph.has_node(x)==False: 
            continue
        
        temp_list_pred=web_graph.predecessors(x)
        temp_list_succ=web_graph.successors(x)



        for y in temp_list_pred:
            final_nodes.append(y)

        for y in temp_list_succ:
            final_nodes.append(y)
                

    sub_graph=list(set(final_nodes))


    print("Base set: ",end=" ")
    print(sub_graph)

    hub_score={}
    auth_score={}
    for i in sub_graph:
        hub_score[i]=1.0
        auth_score[i]=1.0

    for epochs in range(500):
        temp_auth_score={}
        temp_hub_score={}
        normalize_hub=0.0
        normalize_auth=0.0
        for node in sub_graph:
            if node not in temp_auth_score :
                temp_auth_score[node]=0.0

            if node not in temp_hub_score:
                temp_hub_score[node]=0.0

            succ=list(web_graph.successors(node))
            for val in succ:
                if val not in sub_graph: continue
                normalize_hub+=auth_score[val]
                temp_hub_score[node]+=auth_score[val]

            pred=list(web_graph.predecessors(node))
            for val in pred :
                if val not in sub_graph: continue
                normalize_auth+=hub_score[val]
                temp_auth_score[node]+=hub_score[val]

        
        for node in sub_graph:
            auth_score[node]=temp_auth_score[node]/normalize_auth
            hub_score[node]=temp_hub_score[node]/normalize_hub


    sorted_hub=dict(sorted(hub_score.items(),key=lambda item: item[1],reverse=True))
    sorted_auth=dict(sorted(auth_score.items(),key=lambda item: item[1],reverse=True))
    print(sorted_hub)
    print(auth_score)
    op=input('Do you still want to continue? (y/n):')
    if op=='n': 
        break
