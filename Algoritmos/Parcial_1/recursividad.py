data = [1, 3, 7, 8, 11, 12, 18, 21, ]
def binary_search(data, element): 
    return -1

def binary_search_R(data, element, i, j):
    #i = 0 
    #j = len(data) - 1

    if i > j:
        return -1
    
    medio = (i + j) // 2

    if data[medio] == element:
        return medio
    elif data[medio] > element:
        return binary_search_R(data, element, i, medio - 1)
    else:
        return binary_search_R(data, element, medio + 1, j)


#####################################################################################
def partition(data, low, high):
    pivote = data[high]
    i = low - 1

    for j in range(low, high):
        if data[j] <= pivote:
            i + 1
            data[i], data[j] = data[j], data[i]
    
    data[i + 1], data[high] = data[high], data[i + 1]
    return i + 1

def quicksort_impl(data, low, high):
    if low < high:
        pivote = partition(data, low, high)

        quicksort_impl(data, low, pivote - 1)
        quicksort_impl(data, pivote +  high)

def quicksort(data):
    quicksort_impl(data, 0, len(data) - 1)
