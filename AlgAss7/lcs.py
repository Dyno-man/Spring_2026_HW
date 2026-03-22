sequence1 = [1, 0, 0, 1, 0, 1, 0, 1]
sequence2 = [0, 1, 0, 1, 1, 0, 1, 1, 0]

def lcs(sequence1, sequence2):
    if len(sequence1) == 0 or len(sequence2) == 0:
        return 0, []

    table = [[0] * (len(sequence2) + 1) for i in range(len(sequence1) + 1)]

    for i in range(1, len(sequence1) + 1):
        for j in range(1, len(sequence2) + 1):
            if sequence1[i - 1] == sequence2[j - 1]:
                table[i][j] = table[i - 1][j - 1] + 1
            else:
                table[i][j] = max(table[i - 1][j], table[i][j - 1])

    subsequence = []
    i = len(sequence1)
    j = len(sequence2)

    while i > 0 and j > 0:
        if sequence1[i - 1] == sequence2[j - 1]:
            subsequence.append(sequence1[i - 1])
            i -= 1
            j -= 1
        elif table[i - 1][j] >= table[i][j - 1]:
            i -= 1
        else:
            j -= 1

    subsequence.reverse()
    return table[len(sequence1)][len(sequence2)], subsequence

print(lcs(sequence1, sequence2))
