graph_1 = {
    1 : {2},
    2 : {1, 7, 5},
    3 : {5},
    4 : {6},
    5 : {2, 3, 8},
    6 : {8, 4},
    7 : {2},
    8 : {5, 6}
}

graph_2 = {
    1 : {4},
    2 : {4},
    3 : {4},
    4 : {1, 2, 3, 5},
    5 : {4, 6},
    6 : {5}
}

def is_leaf(graph, node):
    if len(graph[node]) == 1:
        return True
    else:
        return False

def remove_leaf_node(graph, node):
    for n in graph:
        if node in graph[n]:
            graph[n].remove(node)

def prufer(graph):
    fin_seq = []

    while len(graph) > 2:
        for n in list(graph):
            if is_leaf(graph, n):
                fin_seq.append(next(iter(graph[n])))
                graph.pop(n)
                remove_leaf_node(graph, n)
                break

    return fin_seq

print(prufer(graph_1))