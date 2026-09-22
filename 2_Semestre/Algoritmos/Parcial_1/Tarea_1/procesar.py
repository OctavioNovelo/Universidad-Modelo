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