def count_unique_values(lista):
    count = 1
    if len(lista) == 0: return 0
    for i in range(1, len(lista)):
        if lista[i] != lista[i - 1]:
            count += 1
    return count

print(count_unique_values([1, 1, 1, 1, 1, 2]))
print(count_unique_values([1, 2, 3, 4, 4, 4, 7, 7, 12, 12, 13]))
print(count_unique_values([]))
print(count_unique_values([-2, -1, -1, 0, 1]))