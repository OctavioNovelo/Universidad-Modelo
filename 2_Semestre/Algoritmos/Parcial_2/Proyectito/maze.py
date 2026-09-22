import numpy as np
import random
from animated_maze import animate_maze
 
#Segun google tener constantes es buena practica, pero se puden cambiar si es necesario
N               = 15     # Cambiar el tamano del laberinto
INITIAL_LIVES   = 5      # vidas iniciales
POISON_INTERVAL = 3      # cada cuantos movimientos hace daño el veneno
LIFE_CELL_HEAL  = 2      # vida que recupera una celda 'L'
DAMAGE_CELLS    = {'P', 'M'}   # celdas que quitan vida al entrar
LIFE_CELLS      = {'L'}        # celdas que dan vida
 

#------------------------------------------------------------------------------------
# Esta funcion enuentra y se asegura de que haya solo 1 start y solo 1 exit.
def find_start(maze):
    #Valida el inicio y final
    rows, cols = maze.shape
    start_pos  = None
    start_count = end_count = 0

    # No hay mucho pierde, recorre todo el arrelgo en busca del start (S) y del exit (E)
    for i in range(rows):
        for j in range(cols):
            cell = maze[i, j]
            if cell == 'S':
                start_count += 1
                start_pos = (i, j)
            elif cell == 'E':
                end_count += 1
 
    if start_count == 0:
        print("Error: No existe celda de inicio (S)")
        return -1, -1
    if start_count > 1:
        print("Error: Hay múltiples celdas de inicio (S)")
        return -1, -1
    if end_count == 0:
        print("Error: No existe celda de salida (E)")
        return -1, -1
    if end_count > 1:
        print("Error: Hay múltiples celdas de salida (E)")
        return -1, -1
 
    return start_pos
#-------------------------------------------------------------------------------------- 
 

#--------------------------------------------------------------------------------------
# Esta funcion es la encargada de resolver el maze
# Ya explique lo que recibe mas abajo, solo que de principio usamos last_row y last_col =- 1. 
def maze_solver_impl(maze, original, row, col, lives, poisoned, poison_steps, steps, visited, solutions, last_row=-1, last_col=-1, path=None):
    #El backtracking
    if path is None:
        path = []  #Aqui es para limpiar el path
    path = path + [(row, col)]  # copia nueva en cada rama, no modifica la anterior, crea una lista con la posición actual agregada
 
    #Primero comprobar si viene envenenado
    if poisoned:
        poison_steps += 1
        if poison_steps % POISON_INTERVAL == 0:
            lives -= 1
 
    #Si ya no tiene vida la ruta no sirve
    if lives <= 0:
        return
 
    steps += 1  #Avanzar si tiene vida aun
 
    # Encontramos la meta
    # Si en el maze[row del start, col del start] es == exit, agregamos a la lista de soluciones
    if original[row, col] == 'E':
        print(f"Solucion encontrada: pasos = {steps}, vidas = {lives}")
        solutions.append({'steps': steps, 'lives': lives, 'path':path})
        return
 
    #Aqui es para saber en que celda se encuentra y que hacer
    original_cell = original[row, col]
 
    if original_cell == 'P':          # Los pinchos por eso P
        lives -= 1
    elif original_cell == 'M':        # Veneno es M (que toc XDXDXD)
        poisoned = True
        poison_steps = 0
    elif original_cell == 'L':        #Vida es lives
        lives = min(lives + LIFE_CELL_HEAL, INITIAL_LIVES)
        poisoned = False              # La vida cura el veneno
        poison_steps = 0
 
    if lives <= 0:    #Igual si en este momento donde esta se queda sin vida para que no siga
        return
 
    # Guarda los valores que tenia antes esta celda y los guarda 
    prev_state = visited.get((row, col))
    visited[(row, col)] = (lives, steps)   #Se registra los valores actuales sobreescribiendo los anteriores
 
    # Limpiar la celda anterior: si era S o E se restaura, si no se marca como visitada
    if last_row != -1 and original[last_row, last_col] not in ('S', 'E'):
        maze[last_row, last_col] = 'V'
    if original[last_row, last_col] in ('S'):
        maze[last_row, last_col] = 'S'
    if original_cell not in ('S', 'E'):
        maze[row, col] = 'A'
    yield maze, lives, steps

    # Marcar siempre la posición actual con el agente
    maze[row, col] = 'A'
    yield maze, lives, steps

    #Tener las celdas vecinas guardadas
    neighbors = [
        (row, col- 1),   # izquierda
        (row,  col+ 1),  # derecha
        (row+ 1, col),   # abajo
        (row- 1, col),   # arriba
    ]
 
    life_moves   = []   # prioridad máxima
    safe_moves   = []
    danger_moves = []   #tratar de no pasar aca

    # Aqui vamos a revisar a los vecinos para decidir a donde ir. 
    for r, c in neighbors:
        if not (0 <= r < maze.shape[0] and 0 <= c < maze.shape[1]):
            continue
        
        # Si la celda está marcada como visitada ('V'), no la puede volver a visitar
        if maze[r, c] == 'V':
            continue

        # Excelente asignacion en el nombre de las vairables litzy, completamente comprensible. 
        orig = original[r, c] # Son las coordenadas de los vecinos actuales

        if orig == 'W':
            continue
        if orig == 'S':  # Agregar esto
            continue
        if orig in LIFE_CELLS:
            life_moves.append((r, c))
        elif orig in DAMAGE_CELLS:
            danger_moves.append((r, c))
        else:
            safe_moves.append((r, c))
 
    #Aqui se suman para que se junten en uno mismo y ese sea el orden que seguira
    for r, c in life_moves + safe_moves + danger_moves:
        # RECURSIVO GENTE
        yield from maze_solver_impl(maze, original, r, c, lives, poisoned, poison_steps, steps, visited, solutions, row, col, path)
        # Estamos llamando a la funcion que resuelve el laverinto con las coordenadas actualizadas.
 
    #Pone la celda de antes al retroceder
    if last_row != -1 and original[last_row, last_col] not in ('S', 'E'):
        maze[last_row, last_col] = 'V'
    if original_cell not in ('S', 'E'):
        maze[row, col] = original_cell
        yield maze, lives, steps
    if original_cell == 'S':
        maze[row, col] = 'S'
        yield maze, lives, steps
    if prev_state is None:  #Si cuando llegamos aca no habia ningun registro previo, se borra del diccionario
        visited.pop((row, col), None)
    else:
        visited[(row, col)] = prev_state #Si lo habia, al retroceder lo restaura como si en esa ruta no se hubiera pisado
#-------------------------------------------------------------------------------------------------------------------
 
#-------------------------------------------------------------------------------------------------------------------
# La funcion encargada de llamar a la funciones que resuelven el maze y guardar la mejor solucion
def maze_solver(maze):
    si, sj = find_start(maze) # Guardamos los valores de la tupla de manera individual (creo que es para la interfaz)

    if si == -1:
        return
    
    original = maze.copy() # Copiar el laberinto para saber como es
    solutions = []
    visited = {} 

    # Aqui se resuelve llamando a maze_solver, se usa yield from para pasarlo a la interfaz
    # Le pasamos a maze_solver_impl(El maze original que recivimos en la funcion, una copia de este mismo ?? XDXDXD, 
    # las coordenadas del start, las vidas actuales, si no encontramos envenenados, los pasos de veneno que ya recorrimos, el total de pasos que ya recorrimos,
    # la lista que soluciones y la mejor solucion actual)
    yield from maze_solver_impl(maze, original, si, sj, lives= INITIAL_LIVES, poisoned= False, poison_steps = 0, steps = 0, visited= visited, solutions= solutions,)
 
    if not solutions:
        print("\nNo se encontró ninguna solucion.")
    else:
        print(f"\nTotal de soluciones encontradas: {len(solutions)}")
        for s in solutions:
            print(f" pasos = {s['steps']}  vidas = {s['lives']}")
 
        best = max(solutions, key=lambda x: (x['lives'], -x['steps']))
        print(f"\nMejor solucion: vidas = {best['lives']}, pasos = {best['steps']}")

        # Dibujar la mejor solucion en el mapa
        for r, c in best['path']:
            if original[r, c] not in ('S', 'E', 'P', 'M', 'L'):
                maze[r, c] = '*'   # marca el camino con asterisco
        yield maze, best['lives'], best['steps']
#------------------------------------------------------------------------------------------------------------------
 

#------------------------------------------------------------------------------------------------------------------
# Funcion para generar un laberinto aleatorio de n x n usando el Algoritmo de Prim Simplificado.
def generate_random_maze(n = 15):
    # Inicializar todo con paredes ('W')
    maze = [['W' for _ in range(n)] for _ in range(n)]
    
    # Lista de paredes candidatas (celda_dentro, celda_nueva)
    walls = []
    
    # Empezar en (1, 1) y marcarlo como start
    start_r, start_c = 1, 1
    maze[start_r][start_c] = 'S'
    
    # Agregar paredes iniciales candidatas alrededor del inicio (saltando de 2 en 2)
    # Las variables direccion guardan hacia donde nos vamos a dirigir de dos en dos (arriba, abajo, derecha e izquierda)
    for direccion_row, direccion_col in [(0, 2), (0, -2), (2, 0), (-2, 0)]:
        # d_row y d_col se suman a start_r y start_c (1,1)
        # En la primera iteracion es:
        # new_row, new_col = (1 + 0), (1 + 2)
        # new_row, new_col = (1, 3) Siendo esto que nos dirigiremos a la derecha.
        new_row, new_col = start_r + direccion_row, start_c + direccion_col

        # Si new_row es => 1 Y 1 <= new_col < 14 (o cualquier numero -1 wque haya en n)
        if 1 <= new_row < n - 1 and 1 <= new_col < n - 1:
            # Se guardan unicamente las direcciones validas
            # (1, 1, 1, 3)
            walls.append((start_r, start_c, new_row, new_col))

    # Mientras haya coordenadas en walls ejecutamos lo del bloque
    while walls:
        # Elegir una pared al azar para que el laberinto sea aleatorio
        pared = random.randint(0, len(walls) - 1)
        # En la primera iteracion seria:
        # (1, 1, 1, 3)
        wall_row, wall_col, new_row, new_col = walls.pop(pared)
        
        # SOLO si la celda no ah sido "visitada". Como aqui todas las celdas se inicializan en walls (W) entonces
        # la celda que todavia tenga 'W' se condiera como NO visitada
        if maze[new_row][new_col] == 'W':
            # Conectar la celda nueva rompiendo la pared intermedia
            # maze[1 + (1 - 1) // 2][1 + (3 - 1) // 2] = ' '
            # maze[1][2] = ' ' Celda vacia que conectada con la otra celda para generar un pasillo
            maze[wall_row + (new_row - wall_row) // 2][wall_col + (new_col - wall_col) // 2] = ' '
            # maze[1][3] = ' ' Esta es para confirmar la posible coordenada que habiamos guardado
            maze[new_row][new_col] = ' '
            
            # Agregar nuevas paredes candidatas desde la celda recién excavada
            for direccion_row, direccion_col in [(0, 2), (0, -2), (2, 0), (-2, 0)]:
                # En la primera iteracion
                # nn_row, nn_col = (1 + 0), (3 + 2)
                # nn_row, nn_Col = (1, 5)
                new_new_row, new_new_col = new_row + direccion_row, new_col + direccion_col

                # Misma condicion que la de arriba solo que obviamente con las nuevas coordenadas.
                if 1 <= new_new_row < n - 1 and 1 <= new_new_col < n - 1 and maze[new_new_row][new_new_col] == 'W':
                    # Las agregamos a la lista de walls para que despues de considere su expansion
                    walls.append((new_row, new_col, new_new_row, new_new_col))

    # Si N es par, el algoritmo no llega al borde.
    if n % 2 == 0:
        for i in range(1, n - 1):
            if maze[n - 3][i] == ' ': 
                maze[n - 2][i] = ' ' # Conectar hacia abajo
            if maze[i][n - 3] == ' ': 
                maze[i][n - 2] = ' ' # Conectar hacia la derecha


    # Rompemos algunas paredes extra para que existan multiples rutas posibles.
    for _ in range(n // 2): 
        row = random.randint(1, n - 2)
        col = random.randint(1, n - 2)
        if maze[row][col] == 'W':
            # Solo si ayuda a conectar dos pasillos (evita espacios vacios grandes)
            if (maze[row - 1][col] == ' ' and maze[row + 1][col] == ' ') or (maze[row][col - 1] == ' ' and maze[row][col + 1] == ' '):
                maze[row][col] = ' '

    # Buscamos el Fin 'E' en la parte inferior/derecha
    found_exit = False
    for r in range(n - 2, 0, -1):
        for c in range(n - 2, 0, -1):
            if maze[r][c] == ' ':
                maze[r][c] = 'E'
                found_exit = True
                break
        if found_exit: break

    # Agregar elementos aleatorios (Pinchos 'P', Veneno 'M', Vida 'L')
    for r in range(1, n - 1):
        for c in range(1, n - 1):
            if maze[r][c] == ' ':
                rand = random.random()
                if rand < 0.05: maze[r][c] = 'P'
                elif rand < 0.10: maze[r][c] = 'M'
                elif rand < 0.15: maze[r][c] = 'L'

    # Retornar como lista de strings (formato maze_str)
    return ["".join(row) for row in maze]
#------------------------------------------------------------------------------------------------------------------
 
 
#------------------------------------------------------------------------------------------------------------------ 
# 1. Generar laberinto aleatorio con el N configurado arriba
maze_str_random = generate_random_maze(N)
 
# 2. Convertir a numpy array
maze = np.array([list(row) for row in maze_str_random])
 
# 3. Ejecutar la animación
animate_maze(maze_solver(maze), interval=0.01)
