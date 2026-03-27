def min_subarray_sum_dual_pointer(nums): 
    min_sum     = float('inf') 
    current_sum = 0 

    for num in nums: 
        current_sum += num 
        min_sum = min(min_sum, current_sum) 
        if current_sum > 0:      # reset window when sum goes positive 
            current_sum = 0 

    return min_sum 

print(min_subarray_sum_dual_pointer([-2, 1, -3, 4, -1, 2, 1, -5, 4])) 