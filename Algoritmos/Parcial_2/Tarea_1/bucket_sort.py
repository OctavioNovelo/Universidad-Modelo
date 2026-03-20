import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

# Insertion Sort
def insertion_sort(data, reverse = True):  
   n = len(data)
   for i in range(1, n):
      e = data[i]
      save = data[i]
      j = i - 1
      # i = 1 ; n = 10
      # e = id(data[1])
      # save = data[1]
      # j = 1 - 1 
      if reverse:
       # 0 >= 0 and id(data[0]) > id(data[1])
       while j >= 0 and data[j] > e:
            # data[1] = data[0]
            data[j + 1] = data[j]
            j -= 1
      else:
         while j >= 0 and data[j] < e:
            data[j + 1] = data[j]
            j -= 1

      data[j + 1] = save
   return data



# Bucket Sort
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
        for val in insertion_sort(cubeta):
            sorted_arr.append(val)

            for i in range(len(sorted_arr)):
                array[i] = sorted_arr[i]

            yield array.copy()

    return array


# Lo que se evaluara
array = list(range(1, 51))
random.shuffle(array)


# Lo de la animacion
# Nota: Estas son funciones para la animacion
fig, ax = plt.subplots()
bars = ax.bar(range(len(array)), array)

ax.set_title("Bucket Sort") # Titulo

# Update
def update(data):
    for bar, val in zip(bars, data):
        bar.set_height(val)

ani = animation.FuncAnimation(
    fig,
    update,
    frames = bucket_sort(array),
    #frames=selection_sort(data),
    #frames=insertion_sort(data),
    #frames=quick_sort(data),
    repeat = False,
    interval = 100
)
 
plt.show()