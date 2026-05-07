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
    'Algoritmos': {'Maestro': 'Edson Geovanny Estrada Lopez','Salon': 'Computo 2', 'Bloques': 2, 'Tipo': 'laboratorio'},
    'Algebra matricial y vectorial': {'Maestro': 'Ing. Juan Norberto Peniche Munoz','Salon': 'A1', 'Bloques': 2, 'Tipo': 'normal'},
    'Fisica aplicada': {'Maestro': 'Dr. Alberto Gabriel Vega Poot','Salon': 'A1', 'Bloques': 2, 'Tipo': 'normal'},
    'Calculo diferencial': {'Maestro': 'Mtra. Aylin Garcia Reyes','Salon': 'A1', 'Bloques': 3, 'Tipo': 'normal'},
    'Sistemas Operativos': {'Maestro': 'Mtro. Alfredo Jose Bolio Dominguez','Salon': 'A1', 'Bloques': 2, 'Tipo': 'normal'},
    'Redes de computadoras': {'Maestro': 'Ing. Franklin Jesus Gonzales Torres','Salon': 'A1', 'Bloques': 2, 'Tipo': 'normal'}
}

asignaturas_semestre_4 = {
    'Estadistica Inferencial': {'Maestro': 'Mtra. Aylin Garcia Reyes', 'Salon': 'A2', 'Bloques': 2, 'Tipo': 'normal'},
    'Ingenieria ecnonomica': {'Maestro': 'Mtra. Grety del Socorro Basulto Morcillo', 'Salon': 'A2', 'Bloques': 1, 'Tipo': 'normal'},
    'Circuitos electricos y electronicos': {'Maestro': 'Mtro. Roberto Carlos Gamboa Ek', 'Salon': 'A2', 'Bloques': 3, 'Tipo': 'normal'},
    'Programacion aplicada a videojuegos': {'Maestro': 'Ing. Jesus Alejandro Balam Sandoval', 'Salon': 'Computo 1', 'Bloques': 2, 'Tipo': 'laboratorio'},
    'Base de datos II': {'Maestro': 'Mtro. Daniel Alejandro Martinez Lopez', 'Salon': 'A2', 'Bloques': 2, 'Tipo': 'normal'},
    'Fundamentos de diseno': {'Maestro': 'Mtra. Ana Bolio Ayora', 'Salon': 'A2', 'Bloques': 2, 'Tipo': 'normal'},
}

asignaturas_semestre_6 = {
    'Sistemas graficos': {'Maestro': 'Mtra. Ana Bolio Ayora', 'Salon': 'A3', 'Bloques': 2, 'Tipo': 'normal'},
    'Desarrollo Web II': {'Maestro': 'Mtro. Daniel Alejandro Martinez Lopez', 'Salon': 'A3', 'Bloques': 2, 'Tipo': 'normal'},
    'Proyeccion y modelado de software': {'Maestro': 'Edson Geovanny Estrada Lopez', 'Salon': 'Computo 2', 'Bloques': 2, 'Tipo': 'laboratorio'},
    'Internet de las cosas': {'Maestro': 'Ing. Franklin Jesus Gonzales Torres', 'Salon': 'A3', 'Bloques': 2, 'Tipo': 'normal'},
    'Aministracion de procesos de negocios': {'Maestro': 'Mtra. Grety del Socorro Basulto Morcillo', 'Salon': 'A3', 'Bloques': 2, 'Tipo': 'normal'},
    'Desarrollo movil I': {'Maestro': 'Ing. Jesus Alejandro Balam Sandoval', 'Salon': 'A3', 'Bloques': 2, 'Tipo': 'normal'},
}

asignaturas_semestre_8 = {
    'Desarrollo de videojuegos': {'Maestro': 'Ing. Jesus Alejandro Balam Sandoval', 'Salon': 'A4', 'Bloques': 3, 'Tipo': 'normal'},
    'Analisis politico y socieconomico de mexico': {'Maestro': 'Mtra. Vanessa Cob Gutierrez', 'Salon': 'A4', 'Bloques': 2, 'Tipo': 'normal'},
    'Innovacion y emprendimiento': {'Maestro': 'Mtra. Kenia Nayrhovy Osorio Lopez', 'Salon': 'A4', 'Bloques': 2, 'Tipo': 'normal'},
    'Ambientes y arquitectura de microservidores': {'Maestro': 'Edson Geovanny Estrada Lopez', 'Salon': 'A4', 'Bloques': 3, 'Tipo': 'normal'},
    'Seguridad de software': {'Maestro': 'Mtro. Alfredo Jose Bolio Dominguez', 'Salon': 'A4', 'Bloques': 2, 'Tipo': 'normal'},
    'Desarrollo basado en agentes': {'Maestro': 'Mtro. Daniel Alejandro Martinez Lopez', 'Salon': 'Computo 1', 'Bloques': 3, 'Tipo': 'laboratorio'},
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
    ('Edson Geovanny Estrada Lopez', 15),
    ('Ing. Juan Norberto Peniche Munoz', 10),
    ('Dr. Alberto Gabriel Vega Poot', 8),
    ('Mtra. Aylin Garcia Reyes', 7),
    ('Mtro. Alfredo Jose Bolio Dominguez', 9),
    ('Ing. Franklin Jesus Gonzales Torres', 6),
    ('Ing. Jesus Alejandro Balam Sandoval', 8),
    ('Mtro. Daniel Alejandro Martinez Lopez', 10),
    ('Mtra. Vanessa Cob Gutierrez', 7),
    ('Mtra. Kenia Nayrhovy Osorio Lopez', 6),
    ('Mtra. Ana Bolio Ayora', 8),
    ('Mtra. Grety del Socorro Basulto Morcillo', 7),
    ('Mtro. Roberto Carlos Gamboa Ek', 9)
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
    print("\n 4) Modificar datos.")
    print("\n 5) Salir. \n")


# Esta funcion lista a los profesores para poder llamar el listado cuando se necesario
# en vez de escribir esto como 4 veces mas XDXDXD
def seleccionar_profesor():
    profesores = list(disponibilidad_profesores.keys())
    if not profesores:
        print("No hay profesores registrados.")
        return None
    
    print("\n--- Seleccionar Profesor ---")
    for i, prof in enumerate(profesores):
        print(f"{i + 1}) {prof}")
    
    try:
        idx_str = input("\nSeleccione el número del profesor (o 0 para cancelar): ")
        if not idx_str: return None
        idx = int(idx_str) - 1
        if idx == -1:
            return None
        if 0 <= idx < len(profesores):
            return profesores[idx]
        else:
            print("Selección inválida.")
            return None
    except ValueError:
        print("Entrada inválida.")
        return None

def gestionar_profesores():
    while True:
        limpiar_pantalla()
        print("\n --- Profesores --- \n")
        print("1) Listar Profesores")
        print("2) Agregar Profesor")
        print("3) Eliminar Profesor")
        print("4) Disponibilidad de profesores")
        print("5) Modificar Horas de trabajo")
        print("6) Volver\n")
        
        op = input("Selecciona una opción: ")
        if op == '1':
            limpiar_pantalla()
            print("\n--- Lista de Profesores ---")
            # Imprimimos  los maestros y sus horas maximas en formato (prof, datos)
            for prof, datos in disponibilidad_profesores.items():
                print(f"- {prof} (Max bloques: {datos['max_horas']})")
            input("\nPresiona una tecla para continuar...")
        elif op == '2':
            nombre = input("Nombre del profesor: ")
            if nombre in disponibilidad_profesores:
                print("El profesor ya existe.")
            else:
                # Uso try para manejar los errores mas facilmente, tambien resulta que es ligeramente mas rapido.
                # Tambien, si falla no hace explotar todo. Continua el codigo. 
                try:
                    horas = int(input("Máximo de horas (1 bloque = 2 horas): "))
                    # YA sabemos como funciona esto gente no se hagan. 
                    dispo = [[True for _ in range(3)] for _ in range(5)]
                    disponibilidad_profesores[nombre] = {
                        'max_horas': horas,
                        'disponibilidad': dispo
                    }
                    print("Profesor agregado.")
                except ValueError:
                    print("Horas inválidas.")
            input("\nPresiona una tecla para continuar...")
        elif op == '3':
            limpiar_pantalla()
            nombre = seleccionar_profesor()
            if nombre:
                # Borramos con del al profesor
                del disponibilidad_profesores[nombre]
                print(f"Profesor {nombre} eliminado.")
            input("\nPresiona una tecla para continuar...")
        elif op == '4':
            limpiar_pantalla()
            nombre = seleccionar_profesor()
            if nombre:
                dias_nombres = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
                bloques_nombres = ["7-9", "9-11", "11-1"]
                while True:
                    limpiar_pantalla()
                    print(f"\n--- Horario de {nombre} ---")
                    # .join sirve para unificar todos los elementos de un iterable en uno solo.
                    # Literalmente es lo mismo que + pero es mas "pythonico" segun google XDXDXDXD
                    # Osea que bloques_nombres ya no seran varios, sera solo 1 y estara separado por " "
                    print("   " + "  ".join(bloques_nombres))
                    # Gente esto esta muy hard.
                    # enumerate es una funcion que itera sobre dias_nombres y le da a la tupla de datos el indice actual
                    # Es como darle esteroides a un FOR. 
                    for i, dia in enumerate(dias_nombres):
                        estado = []
                        for b in range(3):
                            # Revisamos toda la tabla de disponibilidad del profesor acutal y le asignamos
                            # O (queria ponerle SI y NO pero no me termino de gusta como se veia, obte por tictac toe)
                            # si se encuentra en la lista de profes disponibles y una X si NO se encuentra. 
                            # Esto lo revisa dia, lo que nos permite la correcta visualizacion.
                            if disponibilidad_profesores[nombre]['disponibilidad'][i][b]:
                                val = "O"
                            else: 
                                val = "X"

                            # Agregamos val a la lista que estamos mostrando
                            estado.append(val)

                        print(f"{dia:10} {'      '.join(estado)}")

                    print("\n(O = Disponible, X = NO Disponible)")
                    print("\nIngrese el número de día (1-5) y bloque (1-3) para cambiar " \
                    "Ej. '1 1' es Lunes 7am, o '0' para volver.")
                    try:
                        a = input(": ").split() # Es para separar ambos numeros, hay muchas formas de escribirlo asi que decidi limitarlo a este formato
                        if not a: continue
                        if a[0] == '0': break

                        d_idx = int(a[0]) - 1 # indice del dia
                        b_idx = int(a[1]) - 1 # indice del bloque
                        
                        if 0 <= d_idx < 5 and 0 <= b_idx < 3:
                            # Justificar o cambiar a algo mas simple
                            curr = disponibilidad_profesores[nombre]['disponibilidad'][d_idx][b_idx]
                            disponibilidad_profesores[nombre]['disponibilidad'][d_idx][b_idx] = not curr
                        else:
                            print("Indices fuera de rango.")
                            input()
                    # Siento que aqui se nota lo util que es try y except 
                    except (ValueError, IndexError):
                        print("Entrada inválida.")
                        input()
            else:
                input("\nPresiona una tecla para continuar...")
        elif op == '5':
            limpiar_pantalla()
            nombre = seleccionar_profesor()
            if nombre:
                try:
                    print(f"Máximo actual de horas para {nombre}: {disponibilidad_profesores[nombre]['max_horas']}")
                    nuevas_horas = int(input("Ingrese el nuevo máximo de horas: "))
                    disponibilidad_profesores[nombre]['max_horas'] = nuevas_horas
                    print("Máximo de horas actualizado.")
                except ValueError:
                    print("Entrada inválida.")
            input("\nPresiona una tecla para continuar...")
        elif op == '6':
            print("Adios !!")
            break

def gestionar_materias():
    asignaturas_por_sem = {
        1: (asignaturas_semestre_2, materias_semestre_2),
        2: (asignaturas_semestre_4, materias_semestre_4),
        3: (asignaturas_semestre_6, materias_semestre_6),
        4: (asignaturas_semestre_8, materias_semestre_8)
    }
    while True:
        limpiar_pantalla()
        print("\n --- Gestión de Materias --- \n")
        print("1) Listar Materias")
        print("2) Agregar Materia")
        print("3) Eliminar Materia")
        print("4) Modificar Materia")
        print("5) Volver\n")
        
        op = input("Selecciona una opción: ")
        if op == '1':
            limpiar_pantalla()
            for sem_key, (asig, mats) in asignaturas_por_sem.items():
                print(f"\n--- Semestre {sem_key*2} ---")
                for m in mats:
                    d = asig[m]
                    print(f"- {m}: {d['Maestro']} | {d['Salon']} | {d['Bloques']} bloques | {d['Tipo']}")
            input("\nPresiona una tecla para continuar...")
        elif op == '2':
            try:
                sem_val = int(input("Semestre (2, 4, 6, 8): ")) // 2
                if sem_val not in asignaturas_por_sem:
                    print("Semestre inválido.")
                else:
                    nombre = input("Nombre de la materia: ")
                    maestro = input("Maestro: ")
                    salon = input("Salón: ")
                    bloques = int(input("Bloques: "))
                    tipo = input("Tipo (normal/laboratorio): ")
                    
                    asig, mats = asignaturas_por_sem[sem_val]
                    asig[nombre] = {
                        'Maestro': maestro,
                        'Salon': salon,
                        'Bloques': bloques,
                        'Tipo': tipo
                    }
                    if nombre not in mats:
                        mats.append(nombre)
                    print("Materia agregada.")
            except ValueError:
                print("Entrada inválida.")
            input("\nPresiona una tecla para continuar...")
        elif op == '3':
            nombre = input("Nombre de la materia a eliminar: ")
            encontrada = False
            for sem_key, (asig, mats) in asignaturas_por_sem.items():
                if nombre in asig:
                    del asig[nombre]
                    if nombre in mats:
                        mats.remove(nombre)
                    encontrada = True
                    print(f"Materia eliminada del semestre {sem_key*2}.")
            if not encontrada:
                print("Materia no encontrada.")
            input("\nPresiona una tecla para continuar...")
        elif op == '4':
            nombre = input("Nombre de la materia a modificar: ")
            encontrada = False
            for sem_key, (asig, mats) in asignaturas_por_sem.items():
                if nombre in asig:
                    encontrada = True
                    print(f"Modificando {nombre} (Semestre {sem_key*2})")
                    maestro = input(f"Nuevo Maestro [{asig[nombre]['Maestro']}]: ") or asig[nombre]['Maestro']
                    salon = input(f"Nuevo Salón [{asig[nombre]['Salon']}]: ") or asig[nombre]['Salon']
                    try:
                        bloques_str = input(f"Nuevos Bloques [{asig[nombre]['Bloques']}]: ")
                        bloques_val = int(bloques_str) if bloques_str else asig[nombre]['Bloques']
                    except ValueError:
                        bloques_val = asig[nombre]['Bloques']
                    tipo = input(f"Nuevo Tipo (normal/laboratorio) [{asig[nombre]['Tipo']}]: ") or asig[nombre]['Tipo']
                    
                    asig[nombre] = {
                        'Maestro': maestro,
                        'Salon': salon,
                        'Bloques': bloques_val,
                        'Tipo': tipo
                    }
                    print("Materia modificada.")
            if not encontrada:
                print("Materia no encontrada.")
            input("\nPresiona una tecla para continuar...")
        elif op == '5':
            break

def gestion_datos():
    while True:
        limpiar_pantalla()
        print("\n --- Gestión de Datos --- \n")
        print("1) Gestionar Profesores")
        print("2) Gestionar Materias")
        print("3) Volver\n")
        
        op = input("Selecciona una opción: ")
        if op == '1':
            gestionar_profesores()
        elif op == '2':
            gestionar_materias()
        elif op == '3':
            break

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
            horario.llenar_horario(horarios_semestres, asignaturas_por_sem, materias_por_sem, sandwich, disponibilidad_profesores)

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
            gestion_datos()

        case '5':
            limpiar_pantalla()
            print("\n Adios! \n")
            exit()

        case _:
            print("Opción no válida.\n")
            input("Presiona una tecla para continuar...")

if __name__ == "__main__":
    while True:
        seleccion()
