coins = [5, 1, 2, 10, 6]

def coin_row(coins):
    if len(coins) == 0:
        return 0, []
    if len(coins) == 1:
        return coins[0], [coins[0]]

    f = [0] * (len(coins) + 1)
    f[1] = coins[0]

    for i in range(2, len(coins) + 1):
        f[i] = max(f[i - 1], f[i - 2] + coins[i - 1])

    selected = []
    i = len(coins)
    while i >= 1:
        if f[i] == f[i - 1]:
            i -= 1
        else:
            selected.append(coins[i - 1])
            i -= 2

    selected.reverse()
    return f[len(coins)], selected

print(coin_row(coins))
