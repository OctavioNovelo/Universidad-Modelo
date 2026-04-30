
import os
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.animation import FuncAnimation

# Aqui no hay mucho o nada que decir, nos lo dio el profe y funciona, aparte esta facil de comprender.
def animate_maze(maze_generator, interval=0.01 ):
    # Obtener la ruta del directorio donde se encuentra este script
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Solo relacionamos las letras con las imagenes
    textures = {
        'W': mpimg.imread(os.path.join(base_dir, 'wall.png')),
        ' ': mpimg.imread(os.path.join(base_dir, 'path.png')),
        'S': mpimg.imread(os.path.join(base_dir, 'start.png')),
        'E': mpimg.imread(os.path.join(base_dir, 'end.png')),
        'A': mpimg.imread(os.path.join(base_dir, 'agent.png')),
        'V': mpimg.imread(os.path.join(base_dir, 'visited.png')),
        'P': mpimg.imread(os.path.join(base_dir, 'pinchos.png')),
        'L': mpimg.imread(os.path.join(base_dir, 'vida.png')),
        'M': mpimg.imread(os.path.join(base_dir, 'veneno.png')),
        '*': mpimg.imread(os.path.join(base_dir, 'visited.png'))
    }

    # Obtener primer estado
    maze, lives, steps = next(maze_generator)
    rows, cols = maze.shape

    fig, ax = plt.subplots(figsize=(10, 8))
    fig.patch.set_facecolor('#2b2b2b')  # Fondo negro grisáceo
    ax.set_facecolor('#2b2b2b')

    # Dibujar estado inicial
    ims = []
    for i in range(rows):
        row_imgs = []
        for j in range(cols):
            cell = maze[i, j]
            img = textures.get(cell, textures[' '])

            im = ax.imshow(img, extent=(j, j+1, rows-i-1, rows-i))
            row_imgs.append(im)
        ims.append(row_imgs)

    # Contadores en pantalla
    text_color = '#ecf0f1'
    # Colocamos el texto un poco arriba del laberinto
    info_text = ax.text(cols / 2, rows + 0.5, '', color=text_color, 
                        fontsize=12, fontweight='bold', ha='center', va='center')

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows + 1) # Espacio extra para el texto
    ax.set_aspect('equal')

    # Tiempo real desde el inicio de la animación
    start_time = time.time()

    # Función de actualización
    def update(frame):    
        maze, current_lives, current_steps = frame
        for i in range(rows):
            for j in range(cols):
                cell = maze[i, j]
                img = textures.get(cell, textures[' '])
                ims[i][j].set_data(img)
        
        # El tiempo se calcula basado en el tiempo real del sistema
        elapsed_time = time.time() - start_time
        info_text.set_text(f"Vidas: {current_lives} | Pasos: {current_steps} | Tiempo: {elapsed_time:.2f}s")
        
        return [info_text]

    ani = FuncAnimation(
        fig,
        update,
        frames=maze_generator,
        interval=interval,
        repeat=False,
        cache_frame_data=False
    )

    plt.tight_layout()
    plt.show()
