import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches
import random
import numpy as np
import sounddevice as sd
import threading

# Colores para la animacion
COLOR_DEFAULT = '#4a90d9'  # azul  — sin procesar
COLOR_COMPARE = '#e74c3c'  # rojo  — siendo comparados
COLOR_SORTED  = '#2ecc71'  # verde — ya ordenado
COLOR_DONE    = '#95a5a6'  # gris  — antes del piano

# Sonido: genera y reproduce un tono segun el valor de la barra (no bloquea el hilo principal)
def play_tone(value, n=50, duration=0.07, sample_rate=44100):
    freq = 180 + (value / n) * 900      # 180 Hz (grave) → 1280 Hz (agudo)
    t    = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = 0.10 * np.sin(2 * np.pi * freq * t)
    env   = np.exp(-t * 30)
    wave *= env   # fade-out para evitar clicks
    threading.Thread(target=sd.play, args=(wave.astype(np.float32), sample_rate), daemon=True).start()

# Sonido piano: fundamental + armonicos con decay tipo piano (efecto final)
def play_piano(value, n=50, duration=0.55, sample_rate=44100):
    freq = 220 + (value / n) * 880         # rango A3 → A5 aprox
    t    = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    # Armonicos con amplitudes decrecientes (simula timbre de piano)
    wave  = 0.00 * np.ones(len(t))
    wave += 0.13 * np.sin(2 * np.pi * freq * 1 * t)   # fundamental
    wave += 0.07 * np.sin(2 * np.pi * freq * 2 * t)   # 2do armonico
    wave += 0.04 * np.sin(2 * np.pi * freq * 3 * t)   # 3er armonico
    wave += 0.02 * np.sin(2 * np.pi * freq * 4 * t)   # 4to armonico
    wave += 0.01 * np.sin(2 * np.pi * freq * 5 * t)   # 5to armonico
    # Envelope tipo piano: attack instantaneo, decay exponencial largo
    env   = np.exp(-t * 5)
    wave *= env
    threading.Thread(target=sd.play, args=(wave.astype(np.float32), sample_rate), daemon=True).start()


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

        ################## Esto es de la animacion #####################################
        # Rojo: Se marcan los elementos de la cubeta actual (los que se compararan)
        bucket_start = len(sorted_arr)
        colors = [COLOR_SORTED if k < bucket_start else COLOR_DEFAULT for k in range(n)]
        for k in range(len(cubeta)):
            colors[bucket_start + k] = COLOR_COMPARE
        for _ in range(6):             # varios frames para que se vea el rojo
            yield data.copy(), colors[:]
        ###############################################################################



        for j in insertion_sort(cubeta):
            # j = 0
            # insertion_sort(cubeta[0])
            # Aqui se guardan los valores ya ordenados de la cubeta en la variable j, para posteriormente agregarla a 
            # sorted_arr
            sorted_arr.append(j)



####################################################################
            # Esto es para la animacion, nada q ver con el algoritmo
            for i in range(len(sorted_arr)):
                data[i] = sorted_arr[i]

            # Verde para los ya ordenados, rojo para el recien colocado
            colors = [COLOR_DEFAULT] * n
            for k in range(len(sorted_arr) - 1):
                colors[k] = COLOR_SORTED
            colors[len(sorted_arr) - 1] = COLOR_COMPARE

            yield data.copy(), colors[:]

    # Gris: Ya todos ordenados
    colors = [COLOR_DONE] * n
    for _ in range(10):
        yield data.copy(), colors[:]

    # Verde uwu: verde de izquierda a derecha para mostrar que ya se ordeno todo
    for i in range(n):
        colors[i] = COLOR_SORTED
        yield data.copy(), colors[:]
#################################################################
            
    return data


# Lo que se evaluara
data = [random.randint(1, 50) for _ in range(50)]
random.shuffle(data)


# Lo de la animacion
# Fondo negro
BG = '#0d0d0d'
fig, ax = plt.subplots(facecolor=BG)
ax.set_facecolor(BG)
 
bars = ax.bar(range(len(data)), data, color=COLOR_DEFAULT, edgecolor='none')
 
ax.set_title("Bucket Sort", color='white', fontsize=14, fontweight='bold', pad=12) # Titulo
 
# Ejes
ax.set_xlabel("Índice del elemento", color='white', labelpad=8)
ax.set_ylabel("Valor", color='white', labelpad=8)
ax.tick_params(colors='white')
ax.set_ylim(0, 58)
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
for spine in ['bottom', 'left']:
    ax.spines[spine].set_color('#444444')
 
# Simbologia (leyenda)
leyenda = [
    mpatches.Patch(color=COLOR_DEFAULT, label='Sin procesar'),
    mpatches.Patch(color=COLOR_COMPARE, label='Comparando'),
    mpatches.Patch(color=COLOR_SORTED,  label='Ordenado'),
    mpatches.Patch(color=COLOR_DONE,    label='Completo'),
]
ax.legend(handles=leyenda, loc='upper left', facecolor='#1a1a1a',
          edgecolor='#444444', labelcolor='white', fontsize=9)
 
# Estado para detectar cambios en el piano y no spamear sonidos
audio_state = {'prev_green': 0}
# Update
def update(frame):
    data, colors = frame                          
    for bar, val, color in zip(bars, data, colors):
        bar.set_height(val)
        bar.set_facecolor(color)
    
    # Sonido: tocar el tono de la barra roja mas alta (comparacion / colocacion)
    red_vals = [val for val, c in zip(data, colors) if c == COLOR_COMPARE]
    if red_vals:
        play_tone(max(red_vals))
    else:
        # Piano: reproducir el tono de la barra recien puesta en verde
        green_count = colors.count(COLOR_SORTED)
        if green_count > audio_state['prev_green']:
            play_piano(data[green_count - 1])
        audio_state['prev_green'] = green_count

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

plt.tight_layout()
plt.show()