"""
So basically what I'm trying to do is take a graph and see if there are k nodes all connected to each other.

So if k=2 and I have a graph such as (a)<->(b)<->(c). so this would be true and we want to return the first subset
of nodes where we find this 'clique'.

To do this we want to take a graph of size n and recursivley iterate through it. Keeping track of the current nodes and 
their children, so when we entered the graph in the previous example we first go into node a. Once we enter we exapnd to see
that the node a is connected to b we see they are connected to each other. But let's expand out to k=3, so we store that a 
and b nodes are connected to each other
"""

import queue
import networkx as nx

G = nx.Graph()
Q = queue.Queue()


G.add_nodes_from([1,2,3,4,5])
G.add_edges_from([(1,2), (2,3), (3,1), (3,4), (4,5), (5, 3)])

"""stuff = []
for n in G.nodes:
    neighbors = set(G.neighbors(n))
    stuff.append((n, neighbors))"""

k = 10
n = 0
cliques = []

track_edges = []
visited = []
first_node = list(G.nodes())
Q.put(first_node[0])

while n < k:
    temp_node = Q.get()
    visited.append(temp_node)
    

    for val in list(set(G.neighbors(temp_node))):
        if val not in visited:
            Q.put(val)
            visited.append(val)
    
    track_edges.append((temp_node, list(set(G.neighbors(temp_node)))))
    
    
    print(track_edges)
    print(Q.queue)
    cur_clique = []
    n += 1
