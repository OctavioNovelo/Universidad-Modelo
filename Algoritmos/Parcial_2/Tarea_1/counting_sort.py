import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

#Couting sort
# REVISAR !!!
def counting_sort(data):
    n = len(data) # n = 50

    valor_max = max(data)
    count = [0] * (valor_max + 1) # Crea un arreglo de tamaño maximo + 1 para tomar el 0
    # count = [0] * (50 + 1) "Alc no se que hace"
    # Creo que hace un arreglo del tamano del original con valores iniciales de 0
    
    for num in data:
        count[num] += 1  # Cuenta la frecuencia de los elementos
        # num = 0, data[0]
        # count[0] += 1

    for i in range(1,len(count)):
        count[i] += count[i - 1]  # Hace la suma de la frecuencia

    output = [0] * n

    for i in range ( n - 1, -1, -1): #Desde n-1, hasta -1, con paso de -1
        a = data[i]
        b = count[a] - 1
        output[b] = a
        count[a] -= 1

        # Lo de la animacion
        temp = data.copy()
        for j in range(n):
            if output[j] != 0:
                temp[j] = output[j]
        yield temp
    return output


data = list(range(1, 51))
random.shuffle(data)

# Lo de la animacion
# Nota: Estas son funciones para la animacion
fig, ax = plt.subplots()
bars = ax.bar(range(len(data)), data)

ax.set_title("Counting Sort") # Titulo

# Update
def update(data):
    for bar, val in zip(bars, data):
        bar.set_height(val)

ani = animation.FuncAnimation(
    fig,
    update,
    frames = counting_sort(data),
    #frames=selection_sort(data),
    #frames=insertion_sort(data),
    #frames=quick_sort(data),
    repeat = False,
    interval = 100
)
 
plt.show()

