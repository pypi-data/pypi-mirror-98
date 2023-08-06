import complexity_science.ca as ca
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

g = nx.Graph()
g.add_node(1)
n = 2
g = nx.barabasi_albert_graph(n, 1)
adjacency_matrix = nx.to_numpy_matrix(g)

a = ca.gillespie(adjacency_matrix)
#a.initialize_population(100, p=[0.5,0.2,0.1,0.2])
a.initialize_population(10000, p=[0.98,0.02,0,0])
print(a.cells)
#print(a.cells.sum()) 
results = a.run_collect(10)
print(len(results[1]))
#
fig, ax = plt.subplots()
for i in range(len(results[0])-1):
    #print(results[0][i][0][0:,0][0])
    ax.plot(results[1][i], results[0][i][0][0:,0][0], 'c.')

plt.show()
