import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

#Couting sort
# REVISAR !!!
# data = [41, 68, 3, 90, 89, 53]
def counting_sort(data):
    n = len(data) # n = 6

    valor_max = max(data) # 90

    count = [0] * (valor_max + 1) # Crea un arreglo del tamaño del valor_maximo(90) + 1 con un valor inicial de 0
    # count[90] = [{0}0, {0}1, {0}..., {0}91]

    for num in data:
        count[num] += 1  # Cuenta la frecuencia de los elementos
        # num = 0, data[0] = 41
        # count[0] += 1

        # Tarde poquito en entender, pero en esencia lo que se hace es que count es un arreglo de tamano n,
        # esto con el fin de que el indice de este arreglo haga referencia directa al valor que aparece en el arrelgo.
        # count[3] hace referencia al valor 3, no entiendo como funciona en este caso ya que se usan valores del 1 al 51 por lo que
        # cada valor se repita una sola vez, tampoco veo un comparacion para saber cual es el valor que se evalua

    for i in range(1, len(count)):
        count[i] += count[i - 1]  # Hace la suma de la frecuencia
        # i = 1, 1 al 50
        # count[1] += count[1 - 1] 

    output = [0] * n
    # output = [{0}0, {0}1, {0}..., {0}n]
    # Un arreglo llamado output con listas de valor 0 del tamano n = 50


    for i in range(n - 1, -1, -1): #Desde n-1, hasta -1, con paso de -1
        a = data[i] # Elemento actual
        b = count[a] - 1 # count[elemento actual - 1]
        output[b] = a # Output[b] = elemento actual
        count[a] -= 1 # Output[a] -= 1

        # Lo de la animacion
        temp = data.copy()
        for j in range(n):
            if output[j] != 0:
                temp[j] = output[j]
        yield temp
    return output


data = [random.randint(1, 50) for _ in range(50)]
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

