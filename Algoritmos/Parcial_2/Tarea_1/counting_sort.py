import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches
import random
import numpy as np
import sounddevice as sd
import threading

# Colores para la animacion
COLOR_DEFAULT = '#95a5a6'  # gris  — sin procesar
COLOR_COMPARE = '#e74c3c'  # rojo  — comparaciones
COLOR_SORTED  = '#2ecc71'  # verde — uwu
COLOR_DONE    = '#4a90d9'  # azul  — ordenado


#### Lo del sonido la neta se lo pedi a chat jeje #########################################################
# Cola de audio: un solo hilo worker reproduce sonidos para evitar crashes en Windows
# (sd.play no es thread-safe; llamarlo desde multiples hilos corrompe los buffers de PortAudio)
import queue as _queue
_audio_queue = _queue.Queue(maxsize=10)
 
def _audio_worker():
    while True:
        item = _audio_queue.get()
        if item is None:
            break
        wave, sample_rate = item
        try:
            sd.play(wave, sample_rate)
            sd.wait()          # espera a que termine antes de aceptar el siguiente
        except Exception:
            pass               # ignorar errores de audio para no crashear la animacion
 
# Sonido suave: onda seno con volumen bajo y fade suave (comparaciones / colocacion)
def play_tone(value, n=50, duration=0.08, sample_rate=44100):
    freq  = 180 + (value / n) * 900        # 180 Hz (grave) → 1080 Hz (agudo)
    t     = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave  = 0.10 * np.sin(2 * np.pi * freq * t)   # volumen mas bajo que antes
    # Envelope suave: attack rapido, decay exponencial
    env   = np.exp(-t * 30)
    wave *= env
    try:
        _audio_queue.put_nowait((wave.astype(np.float32), sample_rate))
    except _queue.Full:
        pass                   # descartar si la cola esta llena, no bloquear la animacion
 
# Sonido piano: fundamental + armonicos con decay tipo piano (efecto final)
def play_piano(value, n=50, duration=0.55, sample_rate=44100):
    freq = 180 + (value / n) * 900         # misma tonalidad que play_tone
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
    try:
        _audio_queue.put_nowait((wave.astype(np.float32), sample_rate))
    except _queue.Full:
        pass                   # descartar si la cola esta llena, no bloquear la animacion
###########################################################################################################


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


    # Convierte arreglo de conteo en arreglo de posiciones
    for i in range(1, len(count)):
        count[i] += count[i - 1]  # Va haciendo la acumulación de cada índice con el anterior
        # i = 1, 1 al 90
        # al valor de count[índice 1] += se le suma el valor de count[índice 0] 


    output = [0] * n
    # output = [{0}0, {0}1, {0}..., {0}6]
    # Un arreglo llamado output con listas de valor 0 del tamano n = 6

    # Este arreglo es del mismo tamano que el original ya que aqui se guardaran los valores
    # originales ya ordenados por su frecuencia, a diferencia de count que es de tamano valor_max
    # para poder contalizar las apariciones de cada dato.


    # Ordenamiento
    for i in range(n - 1, -1, -1): # recorre el arreglo de der a izq
        a = data[i]  # número actual 
        b = count[a] - 1  # a su contador correspondiente le resta 1 para saber posición
        output[b] = a  # b ya indica su debido índice y pone al num en output
        count[a] -= 1  # bajar el contador del número




###################################################################################
        # Lo de la animacion
        temp = data.copy()
        for j in range(n):
            if output[j] != 0:
                temp[j] = output[j]

        # Rojo: Elemento que se acaba de colocar (posicion b)
        # Default: Posiciones de output ya llenadas anteriormente
        colors = [COLOR_DEFAULT] * n
        for j in range(n):
            if output[j] != 0:
                colors[j] = COLOR_SORTED
        colors[b] = COLOR_COMPARE   # el recien colocado va en rojo encima del gris

        yield temp, colors[:]

    # Gris: Ya todos ordenados
    colors_done = [COLOR_DONE] * n
    for _ in range(10):
        yield temp, colors_done[:]

    # Verde uwu: verde de izquierda a derecha para mostrar que ya se ordeno todo
    for k in range(n):
        colors_done[k] = COLOR_SORTED
        yield temp, colors_done[:]
###################################################################################

    return output


data = [random.randint(1, 50) for _ in range(50)]
random.shuffle(data)

# Fondo negro
BG = '#0d0d0d'
fig, ax = plt.subplots(facecolor=BG)
ax.set_facecolor(BG)

# Lo de la animacion
bars = ax.bar(range(len(data)), data, color=COLOR_DEFAULT, edgecolor='none')

ax.set_title("Counting Sort", color='white', fontsize=14, fontweight='bold', pad=12) # Titulo

# Info
ax.set_xlabel("Índice del elemento", color='white', labelpad=8)
ax.set_ylabel("Valor", color='white', labelpad=8)
ax.tick_params(colors='white')
ax.set_ylim(0, 58)
for spine in ['top', 'right']:ax.spines[spine].set_visible(False)
for spine in ['bottom', 'left']:ax.spines[spine].set_color('#444444')

# Simbologia
leyenda = [
    mpatches.Patch(color=COLOR_COMPARE, label='Colocando'),
    mpatches.Patch(color=COLOR_SORTED,  label='Ordenado'),
    mpatches.Patch(color=COLOR_DONE,    label='Completo'),
]
ax.legend(handles=leyenda, loc='upper left', facecolor='#1a1a1a', edgecolor='#444444', labelcolor='white', fontsize=9)

# Estado para detectar cambios en el piano y no spamear sonidos
audio_state = {'prev_green': 0}

# Update
def update(frame):
    data, colors = frame                         
    for bar, val, color in zip(bars, data, colors):
        bar.set_height(val)
        bar.set_facecolor(color)

    # Sonido: tocar el tono de la barra roja (elemento siendo colocado)
    red_vals = [val for val, c in zip(data, colors) if c == COLOR_COMPARE]
    if red_vals:
        play_tone(max(red_vals))
    else:
        # Piano: reproducir tono piano de la barra recien puesta en verde
        green_count = colors.count(COLOR_SORTED)
        if green_count > audio_state['prev_green']:
            play_piano(data[green_count - 1])
        audio_state['prev_green'] = green_count

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

plt.tight_layout()
plt.show()