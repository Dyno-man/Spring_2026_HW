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

def top_sort(graph):
    stack = []
    visited = []
    
    def dfs(graph, node):
        if node not in visited:
            visited.append(node)

        child_node = graph.get(node)

        for next in child_node:
            if next not in visited:
                dfs(graph, next)

        if node not in stack:
            stack.append(node)
    
    for node in graph:
        dfs(graph, node)

    
    return stack[::-1]


print(top_sort(graph_a))
print(top_sort(graph_b))
