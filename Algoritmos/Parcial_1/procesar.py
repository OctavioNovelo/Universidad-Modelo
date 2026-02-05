lista2 = [0 , 0, 0, 0]
cont = 0
cont_neg = 0
prom_neg = 0

def procesar(lista ):
    for i in range(len(lista)):
        if lista[i] > 0:
            cont += 1
            prom += i
            lista2[0] = prom / cont
        elif lista[i] < 0:
            cont_neg += 1
            prom_neg += i
            lista2[1] = prom_neg / cont_neg
        elif lista[i] == 0:
            lista2[2] += 1
        if lista[i] == 1 or lista[i] == 2:
            lista2[3] = [i]
        elif lista[i] % 2 == 1:
            lista2[i] = [i]
    return lista2

print(procesar([-5, 3, 0, 7, 14, -6, 3, 0, -2, 3, 8]))