def bucket_sort(array):
    if not array: return array # UK 
    
    n = len(array)
    
    valor_max, valor_min = max(array), min(array) #Valor maximo y valor minimo
    num_buckets = n # Las cubetas seran las mismas que el tamano de elementos del array
    
    # Nota: aparentemente se puede usar "_" en vez una variable ("i") para indicar
    # que no se usara el valor del iterador.
    rango_buckets = (valor_max - valor_min) / num_buckets + 1
    buckets = [[] for _ in range(num_buckets)] # Se crea una lista (buckets) de tamano n 
    # que guarde listas vacias

    # buckets = []
    # for _ in range(num_buckets):
    #   buckets.append([])   


    for num in array:
        index = int((num - valor_min) // rango_buckets)
        # Calculamos en que rango donde va cada numero. 
        buckets[index].append(num)
        # Es importante usar el append por que si no re escribiremos las listas y 
        # no agregaremos a las listas, iyk 


    sorted_arr = []

    # Pondre un selection sort o algo porfavor litzy no me funes por no hacerlo ahora
    for cubeta in buckets:
        sorted_arr.extend(sorted(cubeta))

    return sorted_arr  

array = [11, 9, 21, 8, 17, 19, 13, 1, 24, 12]
print(bucket_sort(array))