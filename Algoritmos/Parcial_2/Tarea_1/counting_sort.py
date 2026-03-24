import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

#Couting sort
# data = [41, 68, 3, 90, 89, 53]
def counting_sort(data):
    n = len(data) # n = 6

    valor_max = max(data) # 90

    count = [0] * (valor_max + 1) # Crea un arreglo del tamaño del valor_maximo(90) + 1 con un valor inicial de 0
    # count[90] = [{0}0, {0}1, {0}..., {0}91]

    for num in data:
        count[num] += 1  # Cuenta la frecuencia de los elementos
        # num = 41, data[0] = 41
        # count[41] += 1

        # Tarde poquito en entender, pero en esencia lo que se hace es que count es un arreglo de tamano n,
        # esto con el fin de que el indice de este arreglo haga referencia directa al valor que aparece en el arrelgo.
        # count[41] hace referencia al valor 41, se suma 1 en el arrelgo de frecuencia cada vez que aparece.


    # IDK #######################################################
    for i in range(1, len(count)):
        count[i] += count[i - 1]  # Hace la suma de la frecuencia
        # i = 1, 1 al 90
        # count[1] += count[1 - 1] 
    #############################################################

    output = [0] * n
    # output = [{0}0, {0}1, {0}..., {0}6]
    # Un arreglo llamado output con listas de valor 0 del tamano n = 6

    # Este arreglo es del mismo tamano que el original ya que aqui se guardaran los valores
    # originales ya ordenados por su frecuencia, a diferencia de count que es de tamano valor_max
    # para poder contalizar las apariciones de cada dato.


    # IDK #################################
    for i in range(n - 1, -1, -1):
        a = data[i]
        b = count[a] - 1
        output[b] = a 
        count[a] -= 1
    ######################################

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
