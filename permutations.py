def decrease_by_one(n):
    if n == 1:
        return [[1]]

    prev = decrease_by_one(n - 1)
    result = []
    direction = True 

    for perm in prev:
        if direction: 
            for i in range(len(perm), -1, -1):
                confirm = perm[:i] + [n] + perm[i:]
                result.append(confirm)
        else:  
            for i in range(len(perm) + 1):
                confirm = perm[:i] + [n] + perm[i:]
                result.append(confirm)

        direction = not direction 

    return result

print(decrease_by_one(4))