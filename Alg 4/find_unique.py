import random

# num = [i for i in range(50)] * 2
# num.sort()

# ran = random.randint(0, 49)
# ran = 49

# num.remove(ran)

num = [1, 1, 2, 2, 3, 3, 4, 50, 50, 65, 65]

def find_unique(num):
    p1 = 0
    p2 = 1

    c = 0

    while c < len(num):
        if not p2 >= len(num):
            if num[p1] != num[p2]:
                if num.count(num[p1]) > 1:
                    return num[p2]
                else:
                    return num[p1]
        else:
            return num[len(num) - 1]
    
        c += 1
        p1 += 2
        p2 += 2 
    
    return -1

print(num)
print()
print("The single number is: ",find_unique(num))
print()
# print(ran)