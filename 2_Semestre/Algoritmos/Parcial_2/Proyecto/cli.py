import horario
import os
import json

def load_json(filename):
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    ruta_json = os.path.join(ruta_base, "json", filename)
    with open(ruta_json, "r", encoding="utf-8") as f:
        return json.load(f)

# NOTA: Esta funcion es como el "Guardar Partida". Como ahora los datos no estan pegados aqui en el codigo
# si cambiamos algo en el menu (como un profe o una materia) solo se cambia en la RAM. 
# Si no "escribimos" ese cambio de vuelta al archivo .json, al cerrar el programa todo muere y explota y es lo mismo uk ? .
def save_json(filename, data):
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    ruta_json = os.path.join(ruta_base, "json", filename)
    
    # Si es la disponibilidad, la guardamos con un formato especial para que siga pareciendo una matriz
    # y no un tripal de mil lineas que no se entiende. Si es cualquier otra cosa, json.dump normal y ya.
    if filename == 'disponibilidad_profesores.json':
        def format_dispo(dispo):
            rows = []
            for row in dispo:
                rows.append('            ' + json.dumps(row))
            return '[\n' + ',\n'.join(rows) + '\n        ]'

        output = '{\n'
        items = []
        for key, info in data.items():
            item_json = '    \"' + key + '\": {\n'
            item_json += '        \"max_horas\": ' + str(info['max_horas']) + ',\n'
            item_json += '        \"disponibilidad\": ' + format_dispo(info['disponibilidad']) + '\n'
            item_json += '    }'
            items.append(item_json)
        output += ',\n'.join(items) + '\n}'
        with open(ruta_json, "w", encoding="utf-8") as f:
            f.write(output)
    else:
        with open(ruta_json, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

# ------------------------------------------------------------
# Estructura de horarios para los 4 semestres, los inicializamos todos en ""
# [[Lista de los 5 dias de la semana] Esta parte toma la lista interna y la repite 3 veces]
# Lunes Martes Miercoles Jueves Viernes
# None, None, None, None, None
# None, None, None, None, None
# None, None, None, None, None


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
asignaturas_semestre_2 = load_json('asignaturas_semestre_2.json')
asignaturas_semestre_4 = load_json('asignaturas_semestre_4.json')
asignaturas_semestre_6 = load_json('asignaturas_semestre_6.json')
asignaturas_semestre_8 = load_json('asignaturas_semestre_8.json')

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
# Cada día tiene 3 bloques disponibles (True)
disponibilidad_profesores = load_json('disponibilidad_profesores.json')
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
            # Imprimimos los maestros con un ID (indice + 1) para que sea mas facil identificarlos
            # Tambien mostramos sus horas maximas de trabajo.
            profesores = list(disponibilidad_profesores.keys())
            for i, prof in enumerate(profesores):
                datos = disponibilidad_profesores[prof]
                print(f"{i + 1}) {prof:40} | Max bloques: {datos['max_horas']}")
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
                    dispo = [[True for _ in range(5)] for _ in range(3)]
                    disponibilidad_profesores[nombre] = {
                        'max_horas': horas,
                        'disponibilidad': dispo
                    }
                    save_json('disponibilidad_profesores.json', disponibilidad_profesores)
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
                save_json('disponibilidad_profesores.json', disponibilidad_profesores)
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
                    print(f"\n--- Disponibilidad de {nombre} ---")
                    # Encabezado de los bloques
                    print("            " + "     ".join(bloques_nombres))
                    
                    # Dibujamos la tabla numerada del 1 al 15
                    for i, dia in enumerate(dias_nombres):
                        estado = []
                        for b in range(3):
                            # Calculamos el numero del slot (1-15)
                            n_slot = (i * 3) + b + 1
                            
                            # Si esta disponible mostramos el numero, si no, una X
                            if disponibilidad_profesores[nombre]['disponibilidad'][b][i]:
                                val = f"[{n_slot:2}]"
                            else: 
                                val = "[ X ]"

                            estado.append(val)

                        print(f"{dia:10}  {'   '.join(estado)}")

                    print("\n( # = Disponible, X = NO Disponible)")
                    print("\nIngrese los números de los bloques a cambiar")
                    print("Ej. '1 2 3' para cambiar todo el Lunes")
                    print("'0' para volver.")
                    
                    try:
                        seleccion_slots = input(": ").split()
                        if not seleccion_slots: continue
                        if seleccion_slots[0] == '0':
                            save_json('disponibilidad_profesores.json', disponibilidad_profesores)
                            break

                        for s_str in seleccion_slots:
                            slot = int(s_str)
                            if 1 <= slot <= 15:
                                # Convertimos el numero de slot de vuelta a indices (i, b)
                                d_idx = (slot - 1) // 3
                                b_idx = (slot - 1) % 3
                                
                                # Invertimos el estado actual
                                curr = disponibilidad_profesores[nombre]['disponibilidad'][b_idx][d_idx]
                                disponibilidad_profesores[nombre]['disponibilidad'][b_idx][d_idx] = not curr
                            else:
                                print(f"Bloque {slot} fuera de rango.")
                        
                    except (ValueError, IndexError):
                        print("Entrada inválida detectada.")
                        input("Presiona una tecla para continuar...")
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
                    save_json('disponibilidad_profesores.json', disponibilidad_profesores)
                    print("Máximo de horas actualizado.")
                except ValueError:
                    print("Entrada inválida.")
            input("\nPresiona una tecla para continuar...")
        elif op == '6':
            print("Adios !!")
            break

def gestionar_materias():
    # Mapeo de semestre a su respectivo archivo JSON
    archivos_json = {
        1: 'asignaturas_semestre_2.json',
        2: 'asignaturas_semestre_4.json',
        3: 'asignaturas_semestre_6.json',
        4: 'asignaturas_semestre_8.json'
    }
    
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
                    
                    # Validamos que no exceda los 15 bloques
                    total_actual = sum(d['Bloques'] for d in asig.values())
                    if total_actual + bloques > 15:
                        print(f"\n[!] Error: No se pueden agregar {bloques} bloques.")
                        print(f"El semestre ya tiene {total_actual} bloques ocupados de 15 disponibles.")
                    else:
                        asig[nombre] = {
                            'Maestro': maestro,
                            'Salon': salon,
                            'Bloques': bloques,
                            'Tipo': tipo
                        }
                        if nombre not in mats:
                            mats.append(nombre)
                        
                        save_json(archivos_json[sem_val], asig)
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
                    save_json(archivos_json[sem_key], asig)
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
                    
                    # Validamos que no exceda los 15 bloques (excluyendo el valor anterior de esta misma materia)
                    total_otros = sum(d['Bloques'] for k, d in asig.items() if k != nombre)
                    if total_otros + bloques_val > 15:
                        print(f"\n[!] Error: No se pueden asignar {bloques_val} bloques.")
                        print(f"Las demás materias ya ocupan {total_otros} bloques de 15 disponibles.")
                    else:
                        asig[nombre] = {
                            'Maestro': maestro,
                            'Salon': salon,
                            'Bloques': bloques_val,
                            'Tipo': tipo
                        }
                        save_json(archivos_json[sem_key], asig)
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
            nombres_raw = load_json('nombres_semestres.json')
            nombres = {int(k): v for k, v in nombres_raw.items()}
            for i in range(1, 5):
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
