prices = [3, 5, 8, 9, 10, 17]

def max_price(prices):
    n = len(prices)
    dp = [0] * (n + 1)

    for i in range(1, n + 1):
        best = 0
        j = 0
        while j < i:
            if prices[j] + dp[i - j - 1] > best:
                best = prices[j] + dp[i - j - 1]
            j += 1
        dp[i] = best

    return dp

result = max_price(prices)

print("DP array:", result)
print("Maximum price:", result[len(prices)])