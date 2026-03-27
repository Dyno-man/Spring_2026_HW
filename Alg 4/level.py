def min_crossing_sum(arr, left, mid, right): 

    left_sum = float('inf')
    total = 0 

    for i in range(mid, left - 1, -1): 
        total += arr[i] 
        left_sum = min(left_sum, total)

    right_sum = float('inf') 
    total = 0 

    for i in range(mid + 1, right + 1): 
        total += arr[i] 
        right_sum = min(right_sum, total) 

    return left_sum + right_sum 

 

def min_subarray_sum_dc(arr, left, right): 

    if left == right: 
        return arr[left] 

    mid = (left + right) // 2 
    left_min  = min_subarray_sum_dc(arr, left, mid) 
    right_min = min_subarray_sum_dc(arr, mid + 1, right) 
    cross_min = min_crossing_sum(arr, left, mid, right) 

    return min(left_min, right_min, cross_min) 

nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4] 

print(min_subarray_sum_dc(nums, 0, len(nums) - 1)) 