def merge_sort(lista):
    if len(lista) <= 1:
        return lista

    # Dividir la lista en dos mitades
    medio = len(lista) // 2
    izquierda = merge_sort(lista[:medio])
    derecha = merge_sort(lista[medio:])

    # ordenar las mitades ordenadas
    return ordenar(izquierda, derecha)

def ordenar(izquierda, derecha):
    resultado = []
    i = 0 
    j = 0

    # Comparar elementos de ambas sublistas
    while i < len(izquierda) and j < len(derecha):
        if izquierda[i] < derecha[j]:
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1

    # Agregar los elementos restantes
    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])
    
    return resultado


numeros = [38, 27, 43, 3, 9, 82, 10]
print(f"Original: {numeros}")
ordenados = merge_sort(numeros)
print(f"Ordenados: {ordenados}")
