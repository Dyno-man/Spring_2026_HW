def gaussian_elimination(A, b):
    n = len(A)

    mat = [list(map(float, row)) for row in A]
    vec = list(map(float, b))

    run = True
    col = 0

    while run:
        if col >= n:
            run = False
            continue

        pivot_row = col
        best = abs(mat[col][col])
        for r in range(col + 1, n):
            if abs(mat[r][col]) > best:
                best = abs(mat[r][col])
                pivot_row = r

        if best < 1e-12:
            raise ValueError("Matrix is singular or nearly singular")

        if pivot_row != col:
            mat[col], mat[pivot_row] = mat[pivot_row], mat[col]
            vec[col], vec[pivot_row] = vec[pivot_row], vec[col]

        row = col + 1
        while row < n:
            factor = mat[row][col] / mat[col][col]

            k = col
            while k < n:
                mat[row][k] = mat[row][k] - factor * mat[col][k]
                k += 1

            vec[row] = vec[row] - factor * vec[col]
            row += 1

        col += 1

    x = [0.0] * n
    i = n - 1
    while i >= 0:
        s = 0.0
        j = i + 1
        while j < n:
            s += mat[i][j] * x[j]
            j += 1

        x[i] = (vec[i] - s) / mat[i][i]
        i -= 1

    return x


A = [
    [1, 1, 1],
    [2, 1, 1],
    [1, -1, 3]
]
b = [2, 3, 8]

print(gaussian_elimination(A, b)) 