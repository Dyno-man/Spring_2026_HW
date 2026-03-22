def bottom_up_heap(arr):
    n = len(arr)

    run = True
    start = (n // 2) - 1   

    while run:

        if start < 0:
            run = False
            continue

        root = start

        while True:
            largest = root
            left = 2 * root + 1
            right = 2 * root + 2

            if left < n and arr[left] > arr[largest]:
                largest = left

            if right < n and arr[right] > arr[largest]:
                largest = right

            if largest != root:
                arr[root], arr[largest] = arr[largest], arr[root]
                root = largest
            else:
                break

        start -= 1

    return arr


data = [1, 8, 6, 5, 3, 7, 4]
print(bottom_up_heap(data))