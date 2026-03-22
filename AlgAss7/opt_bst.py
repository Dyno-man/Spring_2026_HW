keys = ["A", "B", "C", "D", "E"]
probs = [0.1, 0.15, 0.2, 0.25, 0.3]

def optimal_bst(keys, probs):
    n = len(keys)

    cost = []
    root = []

    i = 0
    while i < n:
        cost.append([0] * n)
        root.append([0] * n)
        i += 1

    i = 0
    while i < n:
        cost[i][i] = probs[i]
        root[i][i] = i
        i += 1

    length = 2
    while length <= n:
        i = 0
        while i <= n - length:
            j = i + length - 1

            s = 0
            k = i
            while k <= j:
                s += probs[k]
                k += 1

            best = 999999
            best_root = -1

            r = i
            while r <= j:
                left = 0
                right = 0

                if r > i:
                    left = cost[i][r - 1]

                if r < j:
                    right = cost[r + 1][j]

                total = left + right + s

                if total < best:
                    best = total
                    best_root = r

                r += 1

            cost[i][j] = best
            root[i][j] = best_root
            i += 1

        length += 1

    return cost, root

def print_tree(root, keys, i, j, parent, side):
    if i > j:
        return

    r = root[i][j]

    if parent == "":
        print(keys[r], "is the root")
    else:
        print(keys[r], "is the", side, "child of", parent)

    print_tree(root, keys, i, r - 1, keys[r], "left")
    print_tree(root, keys, r + 1, j, keys[r], "right")

cost, root = optimal_bst(keys, probs)

print("Main Table:")
for row in cost:
    print(row)

print("\nRoot Table:")
for row in root:
    print(row)

print("\nOptimal BST:")
print_tree(root, keys, 0, len(keys) - 1, "", "")