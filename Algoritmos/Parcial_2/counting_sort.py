#Couting sort
def counting_sort(data):
    n=len(data)
    valor_max=max(data) #Me da el valor mas grande
    count= [0] * (valor_max + 1) #creo un arreglo de mi tamaño maximo+1 para tomar el 0
    for num in data:
        count[num] += 1  #cuenta la frecuencia de los elementos

    for i in range(1,len(count)):
        count[i] += count[i-1]  #Hace la suma de la frecuencia

    output= [0] * n

    for i in range (n-1,-1,-1): #Desde n-1, hasta -1, con paso de -1
        a = data[i]
        b = count[a] - 1
        output[b] = a
        count[a] -= 1

    return output

print(counting_sort([3,4,2,3,4,1,4]))

