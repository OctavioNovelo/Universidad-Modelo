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
from cli import menu
import random
import subprocess

# --- Estructura del horario: 3 bloques (A, B, C) x 5 días ---
# Cada celda será un diccionario o None si está libre.
horario = [[None for _ in range(5)] for _ in range(3)]


asignaturas = {
    'Algoritmos': {'Maestro': 'Edson Geovanny Estrada Lopez', 'Salon': 'A1'},
    'Algebra matricial y vectorial': {'Maestro': 'Ing. Juan Norberto Peniche Munoz', 'Salon': 'A2'},
    'Fisica aplicada': {'Maestro': 'Dr. Alberto Gabriel Vega Poot', 'Salon': 'A3'},
    'Calculo diferencial': {'Maestro': 'Mtra. Aylin Garcia Reyes', 'Salon': 'B1'},
    'Sistemas Operativos': {'Maestro': 'Mtro. Alfredo Jose Bolio Dominguez', 'Salon': 'B2'},
    'Redes de computadoras': {'Maestro': 'Ing. Franklin Jesus Gonzales Torres', 'Salon': 'B3'},
}


# Guardamos las materias en un lista
materias = list(asignaturas.keys())[:6]


def generar_horario(horario, asignaturas, sandwich = False):
    # Determinar bloques disponibles
    bloques_activos = [0, 2]          # índices de A y C


    if not sandwich:
        bloques_activos.append(1)     # se incluye B si no es sandwich


    huecos = len(bloques_activos) * 5   # 10 o 15 huecos donde podemos poner materias


    # Aqui decidimos la frecuencia con la que aparece una asignatura mínimo 1, máximo 3, suma igual a huecos
    # El indice  1 de frecuencias es la primera materia, se asoscia ese indice con la lista de frecuencias para saber
    # con que frecuencia apareceran las materias.
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
        random.shuffle(pool)


    # Limpiar horario
    for fila in horario:
        for dia in range(5):
            fila[dia] = None


    # Rellenar huecos activos por día y bloque (se recorre ordenado para distribución)
    idx_pool = 0
    for dia in range(5):
        for bloque in bloques_activos:
            materia = pool[idx_pool]
            idx_pool += 1
            info = asignaturas[materia].copy()
            info['Asignatura'] = materia
            horario[bloque][dia] = info


    # En bloque B (si sandwich=True) queda todo None -> se mostrará como "Sandwich"


def mostrar_horario(horario):
    # Nuestra tabala es una matriz bidimencional
    dias = ['LUNES', 'MARTES', 'MIÉRCOLES', 'JUEVES', 'VIERNES']
    bloques_nombre = ['A (7-9)', 'B (9-11)', 'C (11-1)']

    # Recolectar el contenido de cada celda
    filas_texto = []
    for i, fila in enumerate(horario):
        fila_actual = []
        for celda in fila:
            if celda is None:
                if i == 1:  # bloque B
                    texto = "Sandwich"
                else:
                    texto = "Libre"
            else:
                texto = celda['Asignatura']  # solo la materia
            fila_actual.append(texto)
        filas_texto.append(fila_actual)

    # Calcular ancho de cada columna
    anchos = []
    for col in range(5):
        max_len = len(dias[col])
        for fila in filas_texto:
            max_len = max(max_len, len(fila[col]))
        anchos.append(max(max_len, 10))  # mínimo 10 para estética

    # Función para crear una línea separadora (|---|...|)
    def separador():
        return '|' + '|'.join('-' * ancho for ancho in anchos) + '|'

    # Encabezado
    encabezado = '|' + '|'.join(dias[col].center(anchos[col]) for col in range(5)) + '|'
    print(encabezado)
    print(separador())

    # Filas de datos
    for i, fila in enumerate(filas_texto):
        linea = '|' + '|'.join(fila[col].center(anchos[col]) for col in range(5)) + '|'
        print(linea)
    print()  # línea en blanco al final


def seleccion():
    subprocess.run(["clear"])
    menu()
    opcion = input("Selecciona una opción: ")
    # Ajustamos el match para comparar strings
    match opcion:
        case '1':
            subprocess.run(["clear"])
            # Preguntar si se quiere horario sándwich
            resp = input("¿Horario sándwich (bloque B libre)? (s/n): ").lower()
            sandwich = resp == 's'
            generar_horario(horario, asignaturas, sandwich)
            print("Horario generado.\n")
        case '2':
            subprocess.run(["clear"])
            mostrar_horario(horario)
            print("\n Presiona una tecla para continuar... \n")
            input()
        case _:
            print("Opción no válida.\n")


while (True):
    seleccion()

# Corregir la opcion de horario sandwich, actualmente combia toda la fila B en sandwich.
# Comentarlo.
# Agregarle la columna de horarios.
# Crear una lista que guarde los horarios de los distintos semestres.
# Debemos crear una biblioteca x semestre.
# Agregar la variacion para diferentes entradas y salidas.
# Agregar la verificacion de que el profe pueda dar clase a otros semestres en ese horarioc