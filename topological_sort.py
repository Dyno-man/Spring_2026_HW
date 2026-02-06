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

def get_indegree(graph, node):
   return  len(graph.get(node, []))

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


def source_removal(graph):
    q = queue.Queue()
    
    inDeg = []

    for node in graph:
        inDeg.append(get_indegree(graph, node))
    
    print(inDeg)


source_removal(graph_a)