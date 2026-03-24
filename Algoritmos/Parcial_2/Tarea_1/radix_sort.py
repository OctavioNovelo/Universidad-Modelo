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



#Radix sort
# data = [12, 150, 3, 31]
def radix_sort(data):

##############################################################################################
    def countingdigit_sort(data, exp):
        # Es un counting sort primero

        n = len(data) # n = 4
        count = [0] * 10
        # count[10] = [{0}0, {0}1, ..., {0}9]
        # Los digitos que compararan primero son unidades (0-9)

        for num in data:
            i = (num // exp) % 10
            # Esta linea nos da el digito exacto de la posicion exp
            # i = (12 // 1) % 10 = 2 (el digito de unidades del 12 es 2)
            # Si exp fuera 10, i = 1 (el digito de decenas del 12 es 1)
            # Si exp fuera 100, i = 0 (el digito de centenas del 12 es 0 (012))
            count[i] += 1
            # count[2] += 1
            # Justo como en el counting sort

        for i in range(1, 10):
            count[i] += count[i - 1]
            # i = 3
            # count [3] += count[3 - 1] 

        output = [0] * n

        for i in range(n - 1, -1, -1):
            a = data[i]
            d = (a // exp) % 10
            b = count[d] - 1

            output[b] = a
            count[d] -= 1

            temp = data.copy()
            for j in range(n):
                if output[j] != 0:
                    temp[j] = output[j]

            ############################################################################
            # Rojo: elemento recien colocado en output[b]
            # Default: Cuando no se estan comparando esos valores
            colors = [COLOR_DEFAULT] * n
            for j in range(n):
                if output[j] != 0:
                    colors[j] = COLOR_SORTED
            colors[b] = COLOR_COMPARE   # el recien colocado va en rojo encima del gris
            ############################################################################


            yield temp, colors[:]

        return output
###############################################################################################


    valor_max = max(data)
    exp = 1

    while valor_max // exp > 0:
        # 150 // 1 > 0 = True

        ####################################################################################
        gen = countingdigit_sort(data, exp)

        for frame in gen:
            yield frame  

        data = list(gen)[-1] if False else sorted(data, key = lambda x: (x // exp) % 10)
        ####################################################################################


        # El exp va aumentano por 10 (1, 10, 100, 1000, etc)
        exp *= 10

    ############################################################################
    # Azul: Ya todos ordenados
    n = len(data)
    colors_done = [COLOR_DONE] * n
    for _ in range(10):
        yield data, colors_done[:]

    # Verde uwu: verde de izquierda a derecha para mostrar que ya se ordeno todo
    for k in range(n):
        colors_done[k] = COLOR_SORTED
        yield data, colors_done[:]

    yield data, [COLOR_SORTED] * len(data)
    ############################################################################



data = [random.randint(1, 50) for _ in range(50)]
random.shuffle(data)



# Fondo negro
BG = '#0d0d0d'
fig, ax = plt.subplots(facecolor=BG)
ax.set_facecolor(BG)

# Lo de la animacion
bars = ax.bar(range(len(data)), data, color=COLOR_DEFAULT, edgecolor='none')

ax.set_title("Radix Sort", color='white', fontsize=14, fontweight='bold', pad=12) # Titulo

# Ejes
ax.set_xlabel("Índice del elemento", color='white', labelpad=8)
ax.set_ylabel("Valor", color='white', labelpad=8)
ax.tick_params(colors='white')
ax.set_ylim(0, 58)
for spine in ['top', 'right']: ax.spines[spine].set_visible(False)
for spine in ['bottom', 'left']: ax.spines[spine].set_color('#444444')

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
    frames = radix_sort(data),
    #frames=selection_sort(data),
    #frames=insertion_sort(data),
    #frames=quick_sort(data),
    repeat = False,
    interval = 100
)

plt.tight_layout()
plt.show()