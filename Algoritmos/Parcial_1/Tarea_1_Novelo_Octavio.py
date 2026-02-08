def anagrama(palabra1, palabra2):

    resultado1 = 0
    resultado2 = 0

    resultado1 += sum(ord(char) for char in palabra1)
    resultado2 += sum(ord(char) for char in palabra2)

    if resultado1 == resultado2:
        return True
    else:
        return False

print(anagrama(palabra1 = ", ", palabra2 = ", "))
print(anagrama(palabra1 = "rat", palabra2 = "car"))
print(anagrama(palabra1 = "anagram", palabra2 = "nagaram"))
print(anagrama(palabra1 = "awesome", palabra2 = "awesom"))
print(anagrama(palabra1 = "qwerty", palabra2 = "qeywrt"))
print(anagrama(palabra1 = "texttwisstime", palabra2 = "timetwisttext"))

print("##############################################################################################################################################################")
print("##############################################################################################################################################################")
print("##############################################################################################################################################################")

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

print("##############################################################################################################################################################")
print("##############################################################################################################################################################")
print("##############################################################################################################################################################")

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

print("##############################################################################################################################################################")
print("##############################################################################################################################################################")
print("##############################################################################################################################################################")

lista2 = [0, 0, 0, []]

def procesar(lista):
    count = 0
    sum = 0
    count_neg = 0
    sum_neg = 0
    primos = []
    zero = 0
    
    for i in range(len(lista)):
        if lista[i] > 0:
            count += 1
            sum += lista[i]
            lista2[0] = sum / count
        if lista[i] < 0:
            count_neg += 1
            sum_neg += lista[i]
            lista2[1] = sum_neg / count_neg
        if lista[i] == 0:
            zero += 1
            
        lista2[2] = zero
        
        n = lista[i]
        count_primos = 1
        if n > 2:
            for j in range(2, n - 1):
                if n % j == 0:
                    count_primos += 1
            if count_primos <= 2:
                primos.append(lista[i])
                
        lista2[3] = primos
        
    return lista2

print(procesar([-5, 3, 0, 7, 14, -6, 3, 0, -2, 3, 8]))
print(procesar([2, 0, 0, 1, -4, -3, 0, 5, 11, -7, 9]))

###################################################################################################################################################################
###################################################################################################################################################################
###################################################################################################################################################################
