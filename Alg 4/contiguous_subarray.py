"""Dual Pointer Method"""

num = [-2,1,-3,4,-1,2,1,-5,4]

print(sum(num[0:3]))

def dual_point(num):
    i = 0
    j = 1
    c = 0

    lowest = []
    cur_lowest = [num[0]]

    while c < len(num):
        if sum(num[i:j]) < sum(cur_lowest):
            lowest.append(cur_lowest)
            i += 1

        elif sum(num[i:j]) > sum(cur_lowest):
            cur_lowest = []
            cur_lowest.append(num[j])
        j += 1
        c += 1
    
    temp = lowest[0]
    for n in range(1, len(lowest)):
        if sum(lowest[n]) < temp:
            temp = lowest[n]
    
    return temp

print(dual_point(num))
