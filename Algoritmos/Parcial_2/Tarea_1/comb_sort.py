import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches
import random
import numpy as np
import sounddevice as sd
import threading

# Colores para la animacion
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



# Comb sort
def comb_sort(data):
    n = len(data) # tamaño del arreglo
    gap = n # diferencia inicial
    swapped = True # indica si hubieron intercambios

    while (gap > 1 or not swapped): # termina cuando no hay intercambios y gap = 1 (bubble sort)
        i = 0 
        swapped = True

        # Shrink Factor
        for i in range(n - gap): # Si gap = n y aqui estamos haciendo n - gap eso no da 0 ? Eectivamente, en la primera ronda no hace nada xdxdxd
            if data[i] > data[i + gap]: # ¿el valor de la posición es mayor a la dada por el gap?
                data[i], data[i+gap] = data[i+gap], data[i] # si es así hace un intercambio
                swapped = False # para reiniciar dentro del while

            ########################################################
            # Rojo: Se marcan los elementos que se comparan
            colors = [COLOR_DEFAULT] * n
            colors[i]      = COLOR_COMPARE
            colors[i + gap] = COLOR_COMPARE
            yield data, colors[:]
            ########################################################

        gap = int(gap / 1.3) # actualiza dividiendo el gap actual entre el factor de encogimiento  Es para que se vaya haciendo mas chico no ?
        if gap < 1: # asegura que gap != 0
            gap = 1

        ########################################################
        # Default: Cuando no se estan comparando esos valores
        colors = [COLOR_DEFAULT] * n
        yield data, colors[:]
        ########################################################


    ########################################################
    # Gris: Ya todos ordenados
    colors = [COLOR_DONE] * n
    for _ in range(10):
        yield data, colors[:]

    # Verde uwu: verde de izquierda a derecha para mostrar que ya se ordeno todo
    for i in range(n):
        colors[i] = COLOR_SORTED
        yield data, colors[:]
    ########################################################

data = list(range(1, 51))
random.shuffle(data)


# Animacion
# Fondo negro
BG = '#0d0d0d'
fig, ax = plt.subplots(facecolor=BG)
ax.set_facecolor(BG)

bars = ax.bar(range(len(data)), data, color=COLOR_DEFAULT, edgecolor='none')

ax.set_title("Comb Sort", color='white', fontsize=14, fontweight='bold', pad=12)

# Info
ax.set_xlabel("Índice del elemento", color='white', labelpad=8)
ax.set_ylabel("Valor", color='white', labelpad=8)
ax.tick_params(colors='white')
ax.set_ylim(0, 58)
for spine in ['top', 'right']: ax.spines[spine].set_visible(False)
for spine in ['bottom', 'left']: ax.spines[spine].set_color('#444444')

# Simbologia
leyenda = [
    mpatches.Patch(color=COLOR_COMPARE, label='Comparando'),
    mpatches.Patch(color=COLOR_SORTED,  label='Ordenado'),
    mpatches.Patch(color=COLOR_DONE,    label='Completo'),
]
ax.legend(handles=leyenda, loc='upper left', facecolor='#1a1a1a', edgecolor='#444444', labelcolor='white', fontsize=9)

# Estado para detectar cambios en el piano y no spamear sonidos
audio_state = {'prev_green': 0}

def update(frame):
    data, colors = frame                          
    for bar, val, color in zip(bars, data, colors):
        bar.set_height(val)
        bar.set_facecolor(color)

    # Sonido: tocar el tono de la barra roja mas alta (comparacion)
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
    frames=comb_sort(data),
    repeat=False,
    interval=100
)

plt.tight_layout()
plt.show()