import horario
import os

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

# ------------------------------------------------------------
# Estructura de horarios para los 4 semestres, los inicializamos todos en ""
# [[Lista de los 5 dias de la semana] Esta parte toma la lista interna y la repite 3 veces]
# Lunes Martes Miercoles Jueves Viernes
# None, None, None, None, None
# None, None, None, None, None
# None, None, None, None, None

# Reemplazamos la List Comprehension por un ciclo FOR tradicional para inicializar horarios_semestres
horarios_semestres = {}
for i in range(1, 5):
    matriz_semestre = []
    for _ in range(3):
        # Creamos una fila de 5 elementos None (Lunes a Viernes)
        fila = []
        for _ in range(5):
            fila.append(None)
        matriz_semestre.append(fila)
    horarios_semestres[i] = matriz_semestre

# ------------------------------------------------------------
# Asignaturas por semestre
asignaturas_semestre_2 = {
    'Algoritmos': {
        'Maestro': 'Edson Geovanny Estrada Lopez',
        'Salon': 'Computo 2', 'Bloques': 3, 'Tipo': 'laboratorio'
    },
    'Algebra matricial y vectorial': {
        'Maestro': 'Ing. Juan Norberto Peniche Munoz',
        'Salon': 'A1', 'Bloques': 2, 'Tipo': 'normal'
    },
    'Fisica aplicada': {
        'Maestro': 'Dr. Alberto Gabriel Vega Poot',
        'Salon': 'A1', 'Bloques': 3, 'Tipo': 'normal'
    },
    'Calculo diferencial': {
        'Maestro': 'Mtra. Aylin Garcia Reyes',
        'Salon': 'A1', 'Bloques': 3, 'Tipo': 'normal'
    },
    'Sistemas Operativos': {
        'Maestro': 'Mtro. Alfredo Jose Bolio Dominguez',
        'Salon': 'A1', 'Bloques': 2, 'Tipo': 'normal'
    },
    'Redes de computadoras': {
        'Maestro': 'Ing. Franklin Jesus Gonzales Torres',
        'Salon': 'A1', 'Bloques': 2, 'Tipo': 'normal'
    },
}

asignaturas_semestre_4 = {
    'Estadistica Inferencial': {
        'Maestro': 'Mtra. Aylin Garcia Reyes',
        'Salon': 'A2', 'Bloques': 2, 'Tipo': 'normal'
    },
    'Ingenieria ecnonomica': {
        'Maestro': 'Mtra. Grety del Socorro Basulto Morcillo',
        'Salon': 'A2', 'Bloques': 1, 'Tipo': 'normal'
    },
    'Circuitos electricos y electronicos': {
        'Maestro': 'Mtro. Roberto Carlos Gamboa Ek',
        'Salon': 'A2', 'Bloques': 3, 'Tipo': 'normal'
    },
    'Programacion aplicada a videojuegos': {
        'Maestro': 'Ing. Jesus Alejandro Balam Sandoval',
        'Salon': 'Computo 1', 'Bloques': 2, 'Tipo': 'laboratorio'
    },
    'Base de datos II': {
        'Maestro': 'Mtro. Daniel Alejandro Martinez Lopez',
        'Salon': 'A2', 'Bloques': 2, 'Tipo': 'normal'
    },
    'Fundamentos de diseno': {
        'Maestro': 'Mtra. Ana Bolio Ayora',
        'Salon': 'A2', 'Bloques': 2, 'Tipo': 'normal'
    },
}

asignaturas_semestre_6 = {
    'Sistemas graficos': {
        'Maestro': 'Mtra. Ana Bolio Ayora',
        'Salon': 'A3', 'Bloques': 2, 'Tipo': 'normal'
    },
    'Desarrollo Web II': {
        'Maestro': 'Mtro. Daniel Alejandro Martinez Lopez',
        'Salon': 'A3', 'Bloques': 2, 'Tipo': 'normal'
    },
    'Proyeccion y modelado de software': {
        'Maestro': 'Edson Geovanny Estrada Lopez',
        'Salon': 'Computo 2', 'Bloques': 2, 'Tipo': 'laboratorio'
    },
    'Internet de las cosas': {
        'Maestro': 'Ing. Franklin Jesus Gonzales Torres',
        'Salon': 'A3', 'Bloques': 2, 'Tipo': 'normal'
    },
    'Aministracion de procesos de negocios': {
        'Maestro': 'Mtra. Grety del Socorro Basulto Morcillo',
        'Salon': 'A3', 'Bloques': 2, 'Tipo': 'normal'
    },
    'Desarrollo movil I': {
        'Maestro': 'Ing. Jesus Alejandro Balam Sandoval',
        'Salon': 'A3', 'Bloques': 2, 'Tipo': 'normal'
    },
}

asignaturas_semestre_8 = {
    'Desarrollo de videojuegos': {
        'Maestro': 'Ing. Jesus Alejandro Balam Sandoval',
        'Salon': 'A4', 'Bloques': 3, 'Tipo': 'normal'
    },
    'Analisis politico y socieconomico de mexico': {
        'Maestro': 'Mtra. Vanessa Cob Gutierrez',
        'Salon': 'A4', 'Bloques': 2, 'Tipo': 'normal'
    },
    'Innovacion y emprendimiento': {
        'Maestro': 'Mtra. Kenia Nayrhovy Osorio Lopez',
        'Salon': 'A4', 'Bloques': 2, 'Tipo': 'normal'
    },
    'Ambientes y arquitectura de microservidores': {
        'Maestro': 'Edson Geovanny Estrada Lopez',
        'Salon': 'A4', 'Bloques': 3, 'Tipo': 'normal'
    },
    'Seguridad de software': {
        'Maestro': 'Mtro. Alfredo Jose Bolio Dominguez',
        'Salon': 'A4', 'Bloques': 2, 'Tipo': 'normal'
    },
    'Desarrollo basado en agentes': {
        'Maestro': 'Mtro. Daniel Alejandro Martinez Lopez',
        'Salon': 'Computo 1', 'Bloques': 3, 'Tipo': 'laboratorio'
    },
}

# Listas de materias por semestre
# La funcion list sirve para poder convertir un objeto en una lista para poder manipularla
# Como usamos diccionarios cuando usamos asigaturas_semestre_2.keys() lo que nos regresa es un 
# objeto de tipo dict_keys. Este objeto nos permite ver los cambios en tiempo real realizados en el diccionario, sin embargo no nos permite revisar por indices.
# Usando list() convertimos dict_keys en una lista para poder acceder a los datos en forma de indices. 
# Hay que considerar que list() es una copia y NO refleja sus cambios en el diccionario original.
materias_semestre_2 = list(asignaturas_semestre_2.keys())
materias_semestre_4 = list(asignaturas_semestre_4.keys())
materias_semestre_6 = list(asignaturas_semestre_6.keys())
materias_semestre_8 = list(asignaturas_semestre_8.keys())

# ------------------------------------------------------------
# Disponibilidad de profesores
#   'max_horas': máximo de horas que el profesor puede dar clases 
#   'disponibilidad': matriz 3 x 5 (Bloques x Dias), True = puede dar clase, False = no puede dar clase
        # A, B. C
        # True, True, True  Lunes
        # True, True, True  Martes
        # True, True, True  Miercoles
        # True, True, True  Jueves
        # True, True, True  Viernes

#--------------------------------------------------------------------------
disponibilidad_profesores = {}

profesores_datos = [
    ('Edson Geovanny Estrada Lopez', 12),
    ('Ing. Juan Norberto Peniche Munoz', 10),
    ('Dr. Alberto Gabriel Vega Poot', 10),
    ('Mtra. Aylin Garcia Reyes', 12),
    ('Mtro. Alfredo Jose Bolio Dominguez', 10),
    ('Ing. Franklin Jesus Gonzales Torres', 10),
    ('Ing. Jesus Alejandro Balam Sandoval', 10),
    ('Mtro. Daniel Alejandro Martinez Lopez', 10),
    ('Mtra. Vanessa Cob Gutierrez', 8),
    ('Mtra. Kenia Nayrhovy Osorio Lopez', 6),
    ('Mtra. Ana Bolio Ayora', 10),
    ('Mtra. Grety del Socorro Basulto Morcillo', 10),
    ('Mtro. Roberto Carlos Gamboa Ek', 10)
]

for nombre, horas in profesores_datos:
    matriz_dispo = []
    for _ in range(5):
        # Cada día tiene 3 bloques disponibles (True)
        dia_dispo = []
        for _ in range(3):
            dia_dispo.append(True)
        matriz_dispo.append(dia_dispo)
    
    disponibilidad_profesores[nombre] = {
        'max_horas': horas,
        'disponibilidad': matriz_dispo
    }
#--------------------------------------------------------------------------------

def menu():
    print("\n --- Generador de horarios --- \n")
    print("\n 1) Generar Horarios.")
    print("\n 2) Ver horarios.")
    print("\n 3) Ver horarios de los laboratorios.")
    print("\n 4) Salir. \n")

def seleccion():
    limpiar_pantalla()
    menu()
    opcion = input("Selecciona una opción: ")
    match opcion:
        case '1':
            limpiar_pantalla()
            a = input("¿El horario puede tener horas muertas? (s/n): ").lower()
            sandwich = False
            if a == 's':
                sandwich = True

            # Diccionarios de asignaturas (incluye profesores, salones, bloques, tipo) Aqui solo VEMOS la info
            asignaturas_por_sem = {
                1: asignaturas_semestre_2,
                2: asignaturas_semestre_4,
                3: asignaturas_semestre_6,
                4: asignaturas_semestre_8
            }
            # Lista de asignaturas (incluye profesores, salones, bloques, tipo) Aqui LA podemos MODIFICAR
            materias_por_sem = {
                1: materias_semestre_2,
                2: materias_semestre_4,
                3: materias_semestre_6,
                4: materias_semestre_8
            }

            print("\nGenerando horarios...\n")
            horario.generar_horarios(horarios_semestres, asignaturas_por_sem, materias_por_sem, sandwich, disponibilidad_profesores)

            # Guardar horarios generados
            for i in range(1, 5):
                nombres = {
                    1: "Segundo Semestre",
                    2: "Cuarto Semestre",
                    3: "Sexto Semestre",
                    4: "Octavo Semestre"
                }
                horario.guardar_horario(horarios_semestres[i], nombres[i], i)
            
            # Exportar horarios de laboratorio
            horario.guardar_horarios_laboratorios(horarios_semestres)

            print("\nTodos los horarios han sido generados.\n")
            input("Presiona una tecla para continuar...")

        case '2':
            limpiar_pantalla()
            print("\n Horario de qué semestre desea ver? ")
            print("\n 1) Segundo semestre.")
            print("\n 2) Cuarto semestre.")
            print("\n 3) Sexto semestre.")
            print("\n 4) Octavo semestre.\n")
            a = int(input(": "))
            if a in horarios_semestres:
                limpiar_pantalla()
                horario.mostrar_horario(horarios_semestres[a], a)
            else:
                print("Opción no válida.")
            print("\n Presiona una tecla para continuar... \n")
            input()

        case '3':
            limpiar_pantalla()
            horario.mostrar_horarios_laboratorios(horarios_semestres)
            input("\nPresiona una tecla para continuar...")

        case '4':
            limpiar_pantalla()
            print("\n Adios! \n")
            exit()

        case _:
            print("Opción no válida.\n")
            input("Presiona una tecla para continuar...")

if __name__ == "__main__":
    while True:
        seleccion()
