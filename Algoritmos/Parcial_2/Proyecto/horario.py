'''
El horario tiene solamente 3 bloques

A  7-9
B  9-11     SOLO este puede se considerar como horario muerto. Horario Sandwich
C  11-1

Cada semestre cuenta con 6 asignaturas que se esparcen en la semana.
Cada materia debe aparecer al menos 1 vez y maximo 3 veces a la semana.
Cada materia debe tener un profesor asignado.
Cada materia debe tener un salon asignado.

Pueden haber N profesores.
Los profesor puede tener solo 1 materia.
Ciertos profesores pueden NO tener un asignatura. 

Se deben mostrar los horarios en un tabla.
'''
import random
import os

def generar_horario(horario, asignaturas, materias, sandwich = False):
    # Limpiar horario
    for fila in horario:
        for dia in range(5):
            fila[dia] = None

    if sandwich:
        # Generar variedad de combinaciones por día (Sandwich, Entrada, Salida)
        posibles = []
        for d in range(5):
            # Seleccionamos 2 bloques de 3 para asegurar variedad y cumplir la lógica de los comentarios:
            # [0, 2] -> A y C activos (B será Sandwich si queda vacío)
            # [0, 1] -> A y B activos (C será Salida)
            # [1, 2] -> B y C activos (A será Entrada)
            opcion = random.choice([[0, 2], [0, 1], [1, 2]])
            for b in opcion:
                posibles.append((b, d))
        huecos = len(posibles) # 10 huecos totales
    else:
        # Todo lleno (15 huecos)
        posibles = [(b, d) for d in range(5) for b in range(3)]
        huecos = len(posibles)

    # Aquie hay que poner, que si la primera hora tiene una clase a primera hora, la segunda hora se considera
    # el sandwich, pero que si no HAY clase a primera hora, la segunda hora se considera la entrada.
    # Se aplica la misma logica a la salida, si la ultima hora es la segunda hora entonces no es horario sandwich, es la hora de la salida.

    # Aqui decidimos la frecuencia con la que aparece una asignatura mínimo 1, máximo 3, suma igual a huecos
    frecuencias = [1] * 6
    restantes = huecos - 6
    while restantes > 0:
        idx = random.randrange(6)
        if frecuencias[idx] < 3:
            frecuencias[idx] += 1
            restantes -= 1

    # Crear lista de materias repetidas según frecuencias
    pool = []
    for mat, freq in zip(materias, frecuencias):
        pool.extend([mat] * freq)
    
    # Mezclar para que no salgan bloques seguidos de la misma materia
    random.shuffle(pool)

    # Rellenar los huecos seleccionados
    idx_pool = 0
    for b, d in posibles:
        materia = pool[idx_pool]
        idx_pool += 1
        info = asignaturas[materia].copy()
        info['Asignatura'] = materia
        horario[b][d] = info


def format_horario(horario, semestre=None):
    # Nuestra tabala es una matriz bidimencional
    dias = ['LUNES', 'MARTES', 'MIÉRCOLES', 'JUEVES', 'VIERNES']
    # Definimos los encabezados incluyendo la columna HORARIO
    encabezados = ['HORA'] + dias
    # Definimos los nombres de los bloques para la primera columna
    bloques_nombre = ['7:00 - 9:00', '9:00 - 11:00', '11:00 - 13:00']
    
    # Mapeo de semestres para el título
    nombres_semestres = {
        1: "Segundo Semestre",
        2: "Cuarto Semestre",
        3: "Sexto Semestre",
        4: "Octavo Semestre"
    }
    
    titulo = nombres_semestres.get(semestre, "Horario")

    # Recolectar el contenido de cada celda
    filas_texto = []
    for i, fila in enumerate(horario):
        # Iniciamos cada fila con la etiqueta del horario (A, B o C)
        fila_actual = [bloques_nombre[i]]
        for d, celda in enumerate(fila):
            if celda is None:
                if i == 1:  # bloque B (9-11)
                    # Lógica de Sandwich, Entrada y Salida basada en comentarios
                    if horario[0][d] is not None and horario[2][d] is not None:
                        texto = "" # Sandwich
                    elif horario[0][d] is None:
                        texto = "" # Entrada
                    elif horario[2][d] is None:
                        texto = "" # Salida
                    else: # Este para que ? 
                        texto = "Libre"
                elif i == 0: # bloque A (7-9)
                    texto = "" # Entrada 
                elif i == 2: # bloque C (11-1)
                    texto = "" # Salida
                else: # RT este para que ? 
                    texto = "Libre"
            else:
                texto = celda['Asignatura']  # solo la materia
            fila_actual.append(texto)
        filas_texto.append(fila_actual)

    # Calcular ancho de cada columna (ahora son 6 columnas en total)
    anchos = []
    for col in range(6):
        max_len = len(encabezados[col])
        for fila in filas_texto:
            max_len = max(max_len, len(fila[col]))
        anchos.append(max(max_len, 10))  # mínimo 10 para estética

    anchura_total = sum(anchos) + 7
    
    # Función para crear una línea separadora (|---|...|)
    def separador():
        return '|' + '|'.join('-' * ancho for ancho in anchos) + '|'

    resultado = []
    resultado.append("=" * anchura_total)
    resultado.append(titulo.center(anchura_total))
    resultado.append("=" * anchura_total)
    
    # Encabezado de la tabla
    encabezado_str = '|' + '|'.join(encabezados[col].center(anchos[col]) for col in range(6)) + '|'
    resultado.append(encabezado_str)
    resultado.append(separador())

    # Filas de datos
    for i, fila in enumerate(filas_texto):
        linea = '|' + '|'.join(fila[col].center(anchos[col]) for col in range(6)) + '|'
        resultado.append(linea)
    
    return "\n".join(resultado)

def mostrar_horario(horario, semestre=None):
    print(format_horario(horario, semestre))

def guardar_horario(horario, nombre_archivo, semestre=None):
    # Definir la ruta de la carpeta Horarios
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    ruta_horarios = os.path.join(ruta_base, "Horarios")
    
    # Crear la carpeta si no existe
    if not os.path.exists(ruta_horarios):
        os.makedirs(ruta_horarios)
        
    ruta_completa = os.path.join(ruta_horarios, f"{nombre_archivo}.txt")
    
    with open(ruta_completa, "w", encoding="utf-8") as f:
        f.write("--- REPORTE DE HORARIO ---\n\n")
        f.write(format_horario(horario, semestre))
        f.write("\n\n" + "-"*30 + "\n")
        f.write("Detalles de las Asignaturas:\n")
        f.write("-"*30 + "\n")
        
        materias_vistas = set()
        for fila in horario:
            for celda in fila:
                if celda and celda['Asignatura'] not in materias_vistas:
                    f.write(f"Materia: {celda['Asignatura']}\n")
                    f.write(f"Maestro: {celda['Maestro']}\n")
                    f.write(f"Salón:   {celda['Salon']}\n")
                    f.write("-" * 20 + "\n")
                    materias_vistas.add(celda['Asignatura'])
    
    return ruta_completa

# Comentarlo.
# Debemos crear un diccionario x semestre.
# Agregar la verificacion de que el profe pueda dar clase a otros semestres en ese horarioc
# Modificar los salones.
# NO todos los dias deben tener horarios libres, agreguemos una aleatoriedad como en el laberinto.