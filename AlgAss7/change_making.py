sum = 9

denoms = [5, 3, 1]

def make_change(sum, denoms):
    count = [0] * len(denoms)
    t = 0
    while sum > 0:
        if sum - denoms[t] >= 0:
            sum = sum - denoms[t]
            count[t] += 1
        else:
            t += 1
    
    return count

def make_all_change(sum, denoms):
    solutions = [[] for i in range(sum + 1)]
    solutions[0] = [[0] * len(denoms)]

    for i in range(len(denoms)):
        coin = denoms[i]
        for amount in range(coin, sum + 1):
            for solution in solutions[amount - coin]:
                new_solution = solution[:]
                new_solution[i] += 1
                if new_solution not in solutions[amount]:
                    solutions[amount].append(new_solution)

    return solutions[sum]

print(make_all_change(sum, denoms))
