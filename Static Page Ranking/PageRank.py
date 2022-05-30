import numpy as np

no_of_nodes=int(input("Enter the number of nodes: "))
no_of_edges=int(input("Enter the number of edges: "))
adj_matrix=np.zeros(shape=(no_of_nodes,no_of_nodes),dtype='f')
probability_matrix=np.zeros(shape=(no_of_nodes,no_of_nodes),dtype='f')
teleportation_matrix=np.full(shape=(no_of_nodes,no_of_nodes),fill_value=(1/no_of_nodes),dtype='f')

for i in range(no_of_edges):
    print(f"Enter the node of {i+1} edge: ")
    node_1=int(input())
    node_2=int(input())
    adj_matrix[node_1-1][node_2-1]=1


for i in range(no_of_nodes):
    total_connection=adj_matrix[i].sum()
    if total_connection!=0: probability_matrix[i]=adj_matrix[i]/total_connection

is_teleportation_allowed=int(input("Do you want teleportation(0/1)? "))

if is_teleportation_allowed:
    probability_matrix=0.9*probability_matrix+0.1*teleportation_matrix

intial_rank=np.full(shape=no_of_nodes,fill_value=0,dtype='f')
intial_rank[0]=1

no_of_iterations=100000

for i in range(no_of_iterations):
    ## intial_rank*adj_matrix
    # print(f"Before {i}:"," ",intial_rank)
    temp_rank_list=np.dot(intial_rank,probability_matrix)
    intial_rank=temp_rank_list.copy()
    # print(f"After {i}: ",temp_rank_list," ",intial_rank)


print(intial_rank)



###### Principal Left Eigen Vector #######

values,Vector=np.linalg.eig(probability_matrix.T)
left_eigen_vector=abs(Vector[:,0].T)
print("Printing left eigen vector: ",left_eigen_vector)