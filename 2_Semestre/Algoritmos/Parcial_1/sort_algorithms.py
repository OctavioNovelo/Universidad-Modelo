data = [1, 0, -4, 5, 11, 2, -9, 3, 17, 6]

def bubble_sort(data):
    n = len(data)

    for i in range(n-1): # pasadas
        for j in range(n - 1 - i):
            if (data[j] > data[j + 1]): data[j], data[j + 1] = data[j + 1], data[j] # tuplas

bubble_sort(data)
print(data)
