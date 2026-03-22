weights = [3, 2, 1, 4, 5]
values = [25, 20, 15, 40, 50]
W = 6

def knapsack(weights, values, W):
    n = len(weights)

    dp = []
    i = 0
    while i <= n:
        dp.append([0] * (W + 1))
        i += 1

    i = 1
    while i <= n:
        j = 1
        while j <= W:
            if weights[i - 1] <= j:
                take = values[i - 1] + dp[i - 1][j - weights[i - 1]]
                leave = dp[i - 1][j]

                if take > leave:
                    dp[i][j] = take
                else:
                    dp[i][j] = leave
            else:
                dp[i][j] = dp[i - 1][j]
            j += 1
        i += 1

    return dp

result = knapsack(weights, values, W)

print("DP Matrix:")
for row in result:
    print(row)

print("Maximum value:", result[len(weights)][W])