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
def bucket_sort(data):
    if not data: return data # UK 
    
    n = len(data) # n = 50
    
    # valor_max = 50, valor_min = 1.
    valor_max, valor_min = max(data), min(data) #Valor maximo y valor minimo
    num_buckets = n # Las cubetas seran las mismas que el tamano de elementos del data REVISAR!!!
    # num_buckets = 50
    
    # (50 - 1) / 50 + 1 --> 0.9607
    rango_buckets = (valor_max - valor_min) / num_buckets + 1
    
    # Nota: aparentemente se puede usar "_" en vez una variable ("i") para indicar
    # que no se usara el valor del iterador.
    buckets = [[] for _ in range(num_buckets)] 
    # Se crea una lista (buckets) de tamano n que guarde listas vacias
    
    # buckets = [{}1, {}2, ..., {}50]
    
    # buckets = []
    # for _ in range(num_buckets):
    #   buckets.append([])   


    for i in data:
        index = int((i - valor_min) // rango_buckets)
        # Calculamos en que rango donde va cada numero. 
        # index = int((0 - 1) // 0.9607) = 1
        
        buckets[index].append(i)
        # buckets[1].append(1)
        # Es importante usar el append por que si no re escribiremos las listas y 
        # no agregaremos a las listas, iyk yk 

    sorted_arr = []

    # Ordenar las cubetas
    for cubeta in buckets:
        # cubeta = 0
        # buckets = 1 al 50
        for j in insertion_sort(cubeta):
            # j = 0
            # insertion_sort(0)
            # Aqui se guardan los valores ya ordenados de la cubeta en la variable j, para posteriormente agregarla a 
            # sorted_arr.
            sorted_arr.append(j)

            # Esto es para la animacion, nada q ver con el algoritmo
            for i in range(len(sorted_arr)):
                data[i] = sorted_arr[i]

            yield data.copy()
            #######################################################
            
    return data


# Lo que se evaluara
data = list(range(-100, 51))
random.shuffle(data)


# Lo de la animacion
# Nota: Estas son funciones para la animacion
fig, ax = plt.subplots()
bars = ax.bar(range(len(data)), data)

ax.set_title("Bucket Sort") # Titulo

# Update
def update(data):
    for bar, val in zip(bars, data):
        bar.set_height(val)

ani = animation.FuncAnimation(
    fig,
    update,
    frames = bucket_sort(data),
    #frames=selection_sort(data),
    #frames=insertion_sort(data),
    #frames=quick_sort(data),
    repeat = False,
    interval = 100
)
 
plt.show()