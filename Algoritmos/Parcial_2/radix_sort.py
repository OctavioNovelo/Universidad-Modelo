#Radix sort
def radix_sort(data):
    def countingdigit_sort(data,exp):
        n=len(data)
        count= [0] * 10 #porque solo hay digitos del 1-9
        for num in data:
            d = (num//exp)%10
            count[d] += 1  #cuenta la frecuencia de los elementos

        for i in range(1,10):
            count[i] += count[i-1]  #Hace la suma de la frecuencia

        output= [0] * n

        for i in range (n-1,-1,-1): #Desde n-1, hasta -1, con paso de -1
            a = data[i]
            d = (a//exp)%10
            b=count[d]-1
            output[b] = a
            count[d] -= 1

        return output
    
    valor_max=max(data)
    exp=1

    while valor_max // exp >0:
        data=countingdigit_sort(data,exp)
        exp *= 10
    
    return data

print(radix_sort([12,150,3,31]))