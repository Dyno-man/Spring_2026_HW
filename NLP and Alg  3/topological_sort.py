graph_a = {
    'd': {'a', 'b', 'c', 'f', 'g'},
    'a': {'c', 'b'},
    'b': {'e', 'g'},
    'c': {'f'},
    'e': {},
    'f': {},
    'g': {'e', 'f'}
    }

graph_b = {
    'a': {'b'},
    'b': {'c'},
    'c': {'d'},
    'd': {'g'},
    'e': {'a'},
    'f': {'e', 'b', 'c', 'g'},
    'g': {'e'}
}

import queue

def get_indegree(graph):
   nodes = list(graph.keys())
   count = [0] * len(nodes)

   for items in graph:
       edges = list(graph[items])
       
       for keys in nodes:
           if keys in edges:
               num = edges.count(keys)
               ind = nodes.index(keys)

               count[ind] += num

   return count
           


def source_removal(graph):
    q = queue.Queue()
    run = True

    removal = []
    inDeg = []


    while run:
        inDeg = get_indegree(graph)

        for node in range(len(inDeg)):
            if inDeg[node] == 0:
                q.put(list(graph)[node])

        if q.empty():
            run = False
            continue

        
        while not q.empty():
            node = q.get()
            graph.pop(node)
             
            removal.append(node)

        for rem in list(graph):
            edges = list(graph.get(rem, []))

            for item in removal:
                if item in edges:
                    edges.remove(item)

            graph[rem] = (edges)
    
    return removal


# source_graph_a = source_removal(graph_a)
# source_graph_b = source_removal(graph_b)

# graph_a = {
#     'd': {'a', 'b', 'c', 'f', 'g'},
#     'a': {'c', 'b'},
#     'b': {'e', 'g'},
#     'c': {'f'},
#     'e': {},
#     'f': {},
#     'g': {'e', 'f'}
#     }

# graph_b = {
#     'a': {'b'},
#     'b': {'c'},
#     'c': {'d'},
#     'd': {'g'},
#     'e': {'a'},
#     'f': {'e', 'b', 'c', 'g'},
#     'g': {'e'}
# }

# if len(source_graph_a) != len(list(graph_a)):
#     print("Graph A has a cycle")
# else:
#     print(source_graph_a)

# if len(source_graph_b) != len(list(graph_b)):
#     print("Graph B has a cycle")
# else:
#     print(source_graph_b)


def top_sort(graph):
    stack = []
    visited = []
    visiting = []
    
    def dfs(graph, node):
        if node in visiting:
            raise ValueError("Cycle detected")

        if node not in visited:
            visited.append(node)
            visiting.append(node)

            child_node = graph.get(node, [])

            for next in child_node:
                if next in visiting:
                    raise ValueError("Cycle detected")
                if next not in visited:
                    dfs(graph, next)

            visiting.remove(node)

        if node not in stack:
            stack.append(node)
    
    for node in graph:
        dfs(graph, node)

    return stack[::-1]