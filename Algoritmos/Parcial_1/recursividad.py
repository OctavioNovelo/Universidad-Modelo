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
    