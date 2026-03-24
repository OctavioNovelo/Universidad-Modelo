import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

# Comb sort
def comb_sort(array):
    n = len(array) # tamaño del arreglo
    gap = n # diferencia inicial
    swapped = True # indica si hubieron intercambios

    while (gap > 1 or not swapped): # termina cuando no hay intercambios y gap = 1 (bubble sort)
        i = 0 
        swapped = True

        for i in range(n-gap): # recorridos para ordenar
            if array[i] > array[i+gap]: # ¿el valor de la posición es mayor a la dada por el gap?
                array[i], array[i+gap] = array[i+gap], array[i] # si es así hace un intercambio
                swapped = False # para reiniciar dentro del while
            yield array

        gap = int(gap / 1.3) # actualiza dividiendo el gap actual entre el factor de encogimiento
        if gap < 1: # asegura que gap != 0
            gap = 1

        yield array
    print(f'Arreglo ordenado => {array}')

# Animación
array = list(range(1, 51))
random.shuffle(array)
 
fig, ax = plt.subplots()
bars = ax.bar(range(len(array)), array)
 
ax.set_title("Comb Sort")
 
def update(data):
    for bar, val in zip(bars, data):
        bar.set_height(val)
 
ani = animation.FuncAnimation(
    fig,
    update,
    frames=comb_sort(array),
    repeat=False,
    interval=100
)
 
plt.show()
    