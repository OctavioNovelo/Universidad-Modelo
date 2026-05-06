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

# ---------------------------------------------------------------------
# Constantes
DIAS = 5                     # Lunes a Viernes
BLOQUES = 3                  # A, B, C
# ---------------------------------------------------------------------

def restricciones(horario, materias, requeridos, asignaturas, huecos_ocupados, prof_ocupado, lab_ocupado, disponibilidad_profesores, prof_horas_restantes):
    """
    Argumentos:
        horario: matriz 3x5 (Bloques x Dias)
        materias: lista de nombres (6)
        requeridos: frecuencia requerida de cada materia
        asignaturas: diccionario completo de la asignatura
        slots_ocupados: lista de (d, b) ordenados
        prof_ocupado: dict (d,b) -> set de profes ocupados
        lab_ocupado: dict (d,b) -> set de salones de cómputo ocupados
        disponibilidad_profesores: diccionario con max_horas y disponibilidad (3 x 5)
        prof_horas_restantes: dict con las horas que le quedan a cada profesor
    Retorna True si encontró asignación válida.
    """

    # Diccionario, recordar que sirve principalmente para guardar pares
    asignacion = {}

    # Este es un diccionario llamado usadas que guarda las materias de la lista materias con un value de 0. 
    # Este es el diccionario donde veremos con que frecuencia aparece cada materia. 
    usadas = {
        materias: 0 
        for materias in materias
        }
    
    # Esta diccionario lo cree con el unico objetivo de que no se dupliquen las mateiras
    materias_por_dia = {
        dia: set() # TRUCASO GENTE
        # Resulta que set() es una funcion que CREA CONJUNTOS.
        # Los conjuntos son estructuras que solo almacenan datos (Lit no tienen orden ni nada, solo los almacena)
        # pero con la ventaja de que NO permite valores duplicados, elimina el duplicado y que es mucho mas rapida
        # cuando queremos hacer operaciones "in" "not in" que es justo lo que necesitamos para saber si el conjunto (el dia)
        # ya tiene la materia que estamos intentando agregar.
        
        for dia in range(DIAS)
        # Creamos 5 conjuntos vacios (dias)
        }
    
    # Huecos guarda la lista de huecos_ocupados (actualemente vacia), la funcion _definir_huecos_ocupados es quien define esta lista.
    # sorted es una funciona que por default ordena de menor a mayor, sin embargo con key = '' podemos definir como queremos que ordene.
    huecos = sorted(huecos_ocupados)

    # 
    def backtrack(index):
        # Si index == al tamano de la lista huecos
        if index == len(huecos):
            # all regresa verdadero UNICAMENTE si TODOS los argumentos dentro del parentesi son verdaderos.
            # Comparamos si la cantidad de veces que aparece una materia es igual a la cantidad de veces que se requiere que aparezca
            # Esta info la sacamos de la lista usadas con el parametro como el nombre de la materia, que es mat por cada materia en el diccionario de materias. XDXDXD
            return all(usadas[mat] == requeridos[mat] for mat in materias)
        
        # Sacamos la tupla de huecos
        # dias, bloques
        d, b = huecos[index]

        # Materias candidatas para asignar ese dia 
        candidatas = sorted(
            [mat for mat in materias if usadas[mat] < requeridos[mat]
             and mat not in materias_por_dia[d]],
            key=lambda m: requeridos[m] - usadas[m]
        )

        for mat in candidatas:
            prof = asignaturas[mat]['Maestro']
            tipo = asignaturas[mat].get('Tipo', 'convencional')

            # 1. Profesor ya ocupado en este mismo (d,b)?
            if prof in prof_ocupado.get((d, b), set()):
                continue

            # 2. Disponibilidad del profesor
            disp = disponibilidad_profesores.get(prof, {
                'disponibilidad': [[True]*3 for _ in range(5)]
            })
            if not disp['disponibilidad'][d][b]:
                continue

            # 3. Horas restantes del profesor
            if prof_horas_restantes.get(prof, 0) <= 0:
                continue

            # 4. Laboratorio (si la materia lo requiere)
            salon = asignaturas[mat]['Salon']
            if tipo == 'computo':
                # ¿Está libre el salón de cómputo en este (d,b)?
                if salon in lab_ocupado.get((d, b), set()):
                    continue  # ocupado

            # Asignar provisionalmente
            asignacion[(d, b)] = (mat, prof, salon)
            usadas[mat] += 1
            materias_por_dia[d].add(mat)
            prof_ocupado.setdefault((d, b), set()).add(prof)
            if tipo == 'computo':
                lab_ocupado.setdefault((d, b), set()).add(salon)
            prof_horas_restantes[prof] -= 1

            if backtrack(index + 1):
                return True

            # Deshacer cambios
            del asignacion[(d, b)]
            usadas[mat] -= 1
            materias_por_dia[d].remove(mat)
            prof_ocupado[(d, b)].remove(prof)
            if not prof_ocupado[(d, b)]:
                del prof_ocupado[(d, b)]
            if tipo == 'computo':
                lab_ocupado[(d, b)].remove(salon)
                if not lab_ocupado[(d, b)]:
                    del lab_ocupado[(d, b)]
            prof_horas_restantes[prof] += 1

        return False

    if backtrack(0):
        # Volcar asignación al horario
        for (d, b), (mat, prof, salon) in asignacion.items():
            info = asignaturas[mat].copy()
            info['Asignatura'] = mat
            info['Salon'] = salon  # mantiene el salón original
            horario[b][d] = info
        return True
    return False

def generar_horarios(horarios_dict, asignaturas_dict, materias_dict, sandwich,
                     disponibilidad_profesores):
    """
    Genera todos los semestres con backtracking y restricciones completas:
    - Bloques fijos
    - No repetición en el mismo día
    - Disponibilidad y horas máximas de profesores
    - Laboratorios de cómputo (salones reales)
    - Huecos (entrada/salida/sandwich) según parámetro
    """
    semestres = sorted(horarios_dict.keys())

    # ---- Comprobación previa de horas máximas ----
    for prof, datos in disponibilidad_profesores.items():
        horas_necesarias = 0
        for sem in semestres:
            asignaturas = asignaturas_dict[sem]
            for mat, info in asignaturas.items():
                if info['Maestro'] == prof:
                    horas_necesarias += info['Bloques']
        if horas_necesarias > datos['max_horas']:
            raise ValueError(f"El profesor {prof} requiere {horas_necesarias} bloques, "
                             f"pero su máximo es {datos['max_horas']}.")

    # Estructuras globales
    prof_ocupado = {}
    lab_ocupado = {}
    prof_horas_restantes = {prof: datos['max_horas']
                            for prof, datos in disponibilidad_profesores.items()}

    for sem in semestres:
        horario = horarios_dict[sem]
        for fila in horario:
            for d in range(DIAS):
                fila[d] = None

        materias = materias_dict[sem]
        asignaturas = asignaturas_dict[sem]
        requeridos = {mat: asignaturas[mat]['Bloques'] for mat in materias}
        total_bloques = sum(requeridos.values())

        huecos_ocupados = _definir_huecos_ocupados(sandwich, total_bloques)

        exito = restricciones(
            horario, materias, requeridos, asignaturas, huecos_ocupados,
            prof_ocupado, lab_ocupado, disponibilidad_profesores, prof_horas_restantes
        )
        if not exito:
            print(f"No se pudo generar el horario del semestre {sem}. Reintentando...")
            for _ in range(10):
                huecos_ocupados = _definir_huecos_ocupados(sandwich, total_bloques)
                exito = restricciones(
                    horario, materias, requeridos, asignaturas, huecos_ocupados,
                    prof_ocupado, lab_ocupado, disponibilidad_profesores, prof_horas_restantes
                )
                if exito:
                    break
            if not exito:
                print(f"❌ Falló la generación del semestre {sem} después de varios intentos.")

def _definir_huecos_ocupados(sandwich, total_bloques):
    """
    Devuelve una lista de (d,b) que estarán ocupados (len == total_bloques).
    Si sandwich=True, se reparten huecos de forma que como máximo un bloque
    libre por día (entrada, sandwich o salida) y se respeta el total de bloques.
    Si no, se eligen aleatoriamente los slots necesarios.
    """
    todos_huecos = [(d, b) for d in range(DIAS) for b in range(BLOQUES)]
    if sandwich and total_bloques < 10:
        print("Con tan pocos bloques no se puede mantener un solo hueco por día; "
              "se ignorará el modo sandwich.")
        sandwich = False

    if sandwich:
        libres = 15 - total_bloques
        dias_con_hueco = random.sample(range(5), libres) if libres > 0 else []
        bloques_libres = {d: random.choice([0,1,2]) for d in dias_con_hueco}
        slots = []
        for d in range(5):
            if d in bloques_libres:
                bloque_libre = bloques_libres[d]
                for b in range(3):
                    if b != bloque_libre:
                        slots.append((d, b))
            else:
                for b in range(3):
                    slots.append((d, b))
        return slots
    else:
        return random.sample(todos_huecos, total_bloques)

# -------- Funciones de formato y visualización ---------
def format_horario(horario, semestre=None):
    dias = ['LUNES', 'MARTES', 'MIÉRCOLES', 'JUEVES', 'VIERNES']
    encabezados = ['HORA'] + dias
    bloques_nombre = ['7:00 - 9:00', '9:00 - 11:00', '11:00 - 13:00']
    nombres_semestres = {
        1: "Segundo Semestre",
        2: "Cuarto Semestre",
        3: "Sexto Semestre",
        4: "Octavo Semestre"
    }
    titulo = nombres_semestres.get(semestre, "Horario")

    filas_texto = []
    for i, fila in enumerate(horario):
        fila_actual = [bloques_nombre[i]]
        for d, celda in enumerate(fila):
            if celda is None:
                texto = ""
            elif isinstance(celda, str):
                texto = celda
            else:
                texto = celda['Asignatura']
            fila_actual.append(texto)
        filas_texto.append(fila_actual)

    MAX_COL = 20
    ANCHO_HORA = 13
    anchos = [ANCHO_HORA]
    for col in range(1, 6):
        max_len = len(encabezados[col])
        for fila in filas_texto:
            max_len = max(max_len, len(fila[col]))
        anchos.append(min(max_len, MAX_COL))

    def ajustar(texto, ancho):
        if len(texto) > ancho:
            return texto[:ancho-1] + '…'
        return texto

    for fila in filas_texto:
        fila[0] = ajustar(fila[0], anchos[0])
        for col in range(1, 6):
            fila[col] = ajustar(fila[col], anchos[col])

    anchura_total = sum(anchos) + 7
    separador = '|' + '|'.join('-' * ancho for ancho in anchos) + '|'

    resultado = []
    resultado.append("=" * anchura_total)
    resultado.append(titulo.center(anchura_total))
    resultado.append("=" * anchura_total)
    encabezado_str = '|' + '|'.join(ajustar(encabezados[col], anchos[col]).center(anchos[col]) for col in range(6)) + '|'
    resultado.append(encabezado_str)
    resultado.append(separador)
    for fila in filas_texto:
        linea = '|' + '|'.join(fila[col].center(anchos[col]) for col in range(6)) + '|'
        resultado.append(linea)
    return "\n".join(resultado)

def mostrar_horario(horario, semestre=None):
    print(format_horario(horario, semestre))

def guardar_horario(horario, nombre_archivo, semestre=None):
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    ruta_horarios = os.path.join(ruta_base, "Horarios")
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

def mostrar_horarios_laboratorios(horarios_semestres):
    """
    Muestra dos tablas (Computo 1 y Computo 2) con las materias que los ocupan.
    """
    labs = {'Computo 1': None, 'Computo 2': None}
    # Inicializar matrices vacías (5 días x 3 bloques)
    for lab in labs:
        labs[lab] = [[None for _ in range(5)] for _ in range(3)]

    # Recorrer todos los semestres y rellenar
    for sem, horario in horarios_semestres.items():
        for b in range(3):
            for d in range(5):
                celda = horario[b][d]
                if celda and celda.get('Tipo') == 'computo':
                    salon = celda['Salon']
                    if salon in labs:
                        labs[salon][b][d] = f"{celda['Asignatura']} (Sem {sem})"

    # Mostrar cada laboratorio
    for nombre_lab, matriz in labs.items():
        print(f"\n--- Uso de {nombre_lab} ---")
        lin = format_horario(matriz, semestre=None)
        # Reemplazar título genérico
        lin = lin.replace("Horario", f"Laboratorio {nombre_lab}")
        print(lin)