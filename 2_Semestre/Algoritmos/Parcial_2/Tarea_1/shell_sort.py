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
# Lock de audio: protege sd.stop()+sd.play() para que sean atomicos y no crasheen en Windows
# Cada sonido nuevo cancela el anterior inmediatamente — sin cola, sin desincronizacion
_audio_lock = threading.Lock()

def _play_async(wave, sample_rate):
    # Se llama en un hilo separado para no bloquear la animacion
    with _audio_lock:
        sd.stop()                              # cancela el sonido anterior al instante
        sd.play(wave, sample_rate)             # arranca el nuevo sin esperar a que termine

# Sonido suave: onda seno con volumen bajo y fade suave (comparaciones / colocacion)
def play_tone(value, n=50, duration=0.08, sample_rate=44100):
    freq  = 180 + (value / n) * 900        # 180 Hz (grave) → 1080 Hz (agudo)
    t     = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave  = 0.10 * np.sin(2 * np.pi * freq * t)   # volumen mas bajo que antes
    # Envelope suave: attack rapido, decay exponencial
    env   = np.exp(-t * 30)
    wave *= env
    threading.Thread(target=_play_async, args=(wave.astype(np.float32), sample_rate), daemon=True).start()

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
    threading.Thread(target=_play_async, args=(wave.astype(np.float32), sample_rate), daemon=True).start()
###########################################################################################################



def shell_sort(data):

    n = len(data)
    
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = data[i]
            j = i
            while j >= gap and data[j - gap] > temp:
                data[j] = data[j - gap]
                j -= gap
            data[j] = temp

            ########################################################
            # Rojo: elemento recien colocado (j) y el que se comparo (j + gap)
            colors = [COLOR_DEFAULT] * n
            colors[j] = COLOR_COMPARE
            if j + gap < n:
                colors[j + gap] = COLOR_COMPARE
            yield data, colors[:]
            ########################################################

        gap //= 2   
    
    ########################################################
    # Azul: Ya todos ordenados
    colors_done = [COLOR_DONE] * n
    for _ in range(10):
        yield data, colors_done[:]

    # Verde uwu: verde de izquierda a derecha para mostrar que ya se ordeno todo
    for k in range(n):
        colors_done[k] = COLOR_SORTED
        yield data, colors_done[:]
    ########################################################

    return data

data = list(range(1, 51))
random.shuffle(data)



# Fondo negro
BG = '#0d0d0d'
fig, ax = plt.subplots(facecolor=BG)
ax.set_facecolor(BG)

# Lo de la animacion
# Nota: Estas son funciones para la animacion
bars = ax.bar(range(len(data)), data, color=COLOR_DEFAULT, edgecolor='none')

ax.set_title("Shell Sort", color='white', fontsize=14, fontweight='bold', pad=12) # Titulo

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
    data, colors = frame                          # <-- desempacar colores
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
    frames = shell_sort(data),
    #frames=selection_sort(data),
    #frames=insertion_sort(data),
    #frames=quick_sort(data),
    repeat = False,
    interval = 100
)

plt.tight_layout()
plt.show()