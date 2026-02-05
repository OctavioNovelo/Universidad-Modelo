def max_subarray_sum(list, n):
    max = 0
    sum = 0
    for i in range(len(list) - (n + 1)):
        sum = 0
        for j in range(n):
            sum += list[i + j]
            if sum > max: max = sum
    return max

print(max_subarray_sum([1, 2, 5, 2, 8, 1, 5], 2))
print(max_subarray_sum([1, 2, 5, 2, 8, 1, 5], 4))
print(max_subarray_sum([4, 2, 1, 6], 1))