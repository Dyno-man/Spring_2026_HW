possible_items = ('a','b','c','d')
unsorted_list = ['b', 'c', 'd', 'c', 'b', 'a', 'a', 'b']

def count_items(uns_l):
    table = [0] * 4 # 0 => a, 1 => b, 2 => c, 3 => d

    for item in uns_l:
        if item == possible_items[0]:
            table[0] += 1
        elif item == possible_items[1]:
            table[1] += 1
        elif item == possible_items[2]:
            table[2] += 1
        else:
            table[3] += 1
        
    temp = []

    for _ in range(len(uns_l)):
        if table[0] > 0:
            temp.append('a')
            table[0] -= 1
        elif table[1] > 0:
            temp.append('b')
            table[1] -= 1
        elif table[2] > 0:
            temp.append('c')
            table[2] -= 1
        else:
            temp.append('d')
            table[3] -= 1
    
    return temp

print(count_items(unsorted_list))