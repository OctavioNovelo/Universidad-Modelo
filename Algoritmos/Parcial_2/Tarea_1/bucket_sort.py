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

    # n = elementos
    # k = cubetas
    # n / k = elementos por cubeta

    # Como usamos insertion sort y ademas creamos cubetas la complejidad total es:
    # n^2 / k + k = 0

    # Aqui es magia (matematicas)
    # n^2 / k = k
    # n^2 = k^2
    # k = n ** 0.5 (raiz cuadrada)
    # cubetas = raiz cuadrada de n
    # Lei que es eleccion personal escoger cuantas cubetas se crearan, para el caso en el que se usa insertion sort
    # la mejor forma para saber cuatas cubetas usar era con raiz cuadrada
    
    num_buckets = int(n ** 0.5)
    # num_buckets = 7.071
    
    # (50 - 1) / 7.071 + 1 --> 7.9297
    rango_buckets = (valor_max - valor_min) / num_buckets + 1
    # rango_buckets = 1-7


    buckets = [[] for _ in range(num_buckets)] 
    # Se crea una lista (buckets) de tamano num_buckets que guarde listas vacias
    
    # buckets = [{}0, {}1, ..., {}6]
    
    # buckets = []
    # for _ in range(num_buckets):
    #   buckets.append([])   


    for i in data:
        # i es el valor actual de data

        index = int((i - valor_min) // rango_buckets)
        # Calculamos en que cubeta va cada valor. 
        # index = int((i - 1) // 7) = 0
        
        buckets[index].append(i)
        # buckets[0].append(i)

        # Es importante usar el append por que si no re escribiremos las listas y 
        # no agregaremos los valores a las listas, iyk yk.
        # Date cuenta que cuando i = 8 index cambia a 1 ya que se pasa del rango por cubeta, 
        # lo que no permite que este en la cubeta 0 y si en la 1.


    sorted_arr = []

    # Ordenar las cubetas
    for cubeta in buckets:
        # cubeta = 0
        # buckets = 0 al 6
        for j in insertion_sort(cubeta):
            # j = 0
            # insertion_sort(cubeta[0])
            # Aqui se guardan los valores ya ordenados de la cubeta en la variable j, para posteriormente agregarla a 
            # sorted_arr
            sorted_arr.append(j)


            ########################################################
            # Esto es para la animacion, nada q ver con el algoritmo
            for i in range(len(sorted_arr)):
                data[i] = sorted_arr[i]

            yield data.copy()
            #######################################################
            
    return data


# Lo que se evaluara
data = [random.randint(1, 50) for _ in range(50)]
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