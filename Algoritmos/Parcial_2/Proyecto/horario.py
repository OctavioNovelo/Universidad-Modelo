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

# NOTA: El uso de .get y .setdefault se debe a que al ustar usando diccionarios, si tratamos de acceder a datos que no existen el programa
# no regresa "nada" si no que da un error llamado KeyError. Por eso debemos tener cuidado con la informacion que obtenemos, como seguirdad
# usamos .get y .setdefault que son basicamenge como IF-ELSE IF ya que literalmente hace SI encuentras esto damelo SI NO crea este placeholder. 
# NO es mamoneria, simplemente es porque el uso de diccionarios lo requiere. 

# NOTA MENTAL: El codigo creo que se construye en el camino.
import random
import os
# Comprensiones de listas

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

    # Diccionario, aqui guardaemos los bloques del horario, con profesor, materia y salon asignados. 
    asignacion = {}

    # Este es un diccionario llamado usadas que guarda las materias de la lista materias con un value de 0. 
    # Este es el diccionario donde veremos con que frecuencia aparece cada materia. 
    usadas = {
        m: 0 
        for m in materias
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
        
        # Sacamos la tupla/coordenadas/bloque
        # dias, bloques
        d, b = huecos[index]

        '''
        # Materias candidatas para asignar ese dia
        # Es basicamente un "filtro" donde por nivel de urgencia se decide que materias poner en que bloque
        # Por cada materia en materias se revisa si en la lista "usadas" el numero de veces que YA APARECIO para ver si es menor
        # que el numero de veces que esa materia se REQUIERE que aparezca Y se revisa si esa materia NO ESTA en MATERIAS_POR_DIA[dias]
        # El nivel de urgencia se mide con la cantidad requerida - la cantidad de veces que ya salio.
        # Basicamente:
            - sorted() sirve para ordenar la lista que se le pase, en este caso usamos reverse = True. 
            - La materia se agrega a la lista unicamente si pasa por el filtro.
            - Se ordena 
        # Este metodo (materia for materia in materias if usadas[materia] < requeridos[materias] and materia not in materias_por_dia[d]]) se le conoce como 
        # expresiones generadoras y nos sirve para aumentar la velocidad del codigo, ya que 
        # permite solicitar elementos de un GRAN conjuntos de datos ya que no almacena todos los datos en la RAM si no que los crea
        # por cada iteracion. Como caracteristica los objetos generadores solo se pueden iterar una vez, una vez consumido este esapcio en memoria
        # se libera. En este caso cada materia pasa a ser materia (iterable) y se consume en la misma linea al agregarlo a la lista de
        # candidatas, libnerando la memoria y dejando espacio para la siguiente materia.
        # NO confundir con un ciclo FOR, son similares pero no iguales.
        # La sintaxis de sorted es (iterable, regla (en este caso que despues de restar acomoden de menor a mayor pero como reverse == True va de mayor a menor), reverse = bool)
        ''' 
        candidatas = sorted([materia for materia in materias if usadas[materia] < requeridos[materia] and materia not in materias_por_dia[d]], key = lambda m: requeridos[m] - usadas[m], reverse = True)

        # Por cada materia en candidatos ahora revisamos si el PROFESOR de esa materia esta disponible
        # Filtro del profesor
        for mat in candidatas:
            # NOTA MENTAL: Me puse a pensar si es mas eficiente guardarlo en variables o llamarlas directamente cuando quiera eso en especifico
            prof = asignaturas[mat]['Maestro'] # Nombre del profe
            tipo = asignaturas[mat].get('Tipo', 'normal') # Tipo de materias

            # 1. Profesor ya ocupado en este mismo (d,b)?
            # prof_ocupado ocupa el diccionario de disponibilidad_profesores (3 x 5)
            # .get funciona asi: get busca el bloque d, b en prof_ocupado, SI LO ENCUENTRA, entonces entramos a la condicion y continuamos
            # con el siguiente profesor (Recuerden como funciona continue), SI NO LO ENCUENTRA, entonces get retorna un 
            # conjunto vacio "set()", lo que significa que el maestro esta libre en esa hora.
            if prof in prof_ocupado.get((d, b), set()):
                continue

            # 2. Disponibilidad del profesor
            # Si no encontramos al profesor en la lista creamos un perfil temporal donde SIEMPRE esta dispo ese nuevo profesor
            # No me gusta pero si no me da error XDXDXD
            disp = disponibilidad_profesores.get(prof, {'disponibilidad': [[True]*3 for _ in range(5)]})
            # Si ese dia y bloque NO es True, continue y pasamos al otro profesor
            if not disp['disponibilidad'][d][b]:
                continue
            # Si ese dia es True entonces avanzamos al siguiente filtro

            # 3. Horas restantes del profesor
            # Revisamos si las horas restantes son mayores a 0, en ese caso el profesor aun puede impartir materias
            # Si las horas restantes del profesor es menor o igual a 0 (osea que ya no puede dar clases) entonces pasamos al siguente
            # profesor. 
            if prof_horas_restantes.get(prof, 0) <= 0:
                continue

            # 4. Laboratorio
            salon = asignaturas[mat]['Salon']
            # Solo nos preocupamos si la materia requiere un laboratorio
            if tipo == 'laboratorio':
                # Buscamos en lab_ocupado, si retorna un conjunto vacio entonces SI podemos usar ese laboratorio
                if salon in lab_ocupado.get((d, b), set()):
                    continue  # ocupado

            # Asignar provisionalmente
            asignacion[(d, b)] = (mat, prof, salon)

            usadas[mat] += 1 # Aumentamos un uso a la materia.
            materias_por_dia[d].add(mat) # Agregamos la materia a la lista.

            # setdefault sirve similar el get pero para escribir y asegurar.
            # Si SI eiste algo en el bloque (d, b) devuelve la informacion que hay en ese bloque
            # Si NO existe nada en el bloque (d, b) se creara un conjunto vacio y se asignara el profesor.
            prof_ocupado.setdefault((d, b), set()).add(prof)

            if tipo == 'laboratorio':
                lab_ocupado.setdefault((d, b), set()).add(salon)

            prof_horas_restantes[prof] -= 1 

            # BACKTRACKING !!!
            if backtrack(index + 1):
                return True
                # SI las asignaciones en los otros semestres es exitosa entonces retornaremos True indicando que los horarios se 
                # generaron correctamente.
            # Me causa mucha gracia el backtracking, siento que estoy tirando un blackflash iyk yk, osea nada q ver vrd.


            # Deshacer cambios
            del asignacion[(d, b)] # Eliminamos la primera asignacion
            usadas[mat] -= 1 # Eliminamos su uso
            materias_por_dia[d].remove(mat) # Eliminamos la materia de la lista de materias diaria
            prof_ocupado[(d, b)].remove(prof) # Eliminamos el profesor de la lista de prof_ocupado

            if not prof_ocupado[(d, b)]:
                del prof_ocupado[(d, b)]
            
            if tipo == 'laboratorio':
                lab_ocupado[(d, b)].remove(salon)

                if not lab_ocupado[(d, b)]:
                    del lab_ocupado[(d, b)]
            
            prof_horas_restantes[prof] += 1 # Le sumamos las horas que le habiamos quitado al profesor

        # No se logro realizar los horarios    
        return False

    if backtrack(0):
        # Volcar asignación al horario
        # Sabemos que asignacion contiene toda la info del bloque actual
        # La sacamos de ahi y la guardamos en info (un diccionario copia de asignaturas)
        # prof esta puesto para no romper la sintaxis de la informacion.
        for (d, b), (mat, prof, salon) in asignacion.items():
            info = asignaturas[mat].copy()
            info['Asignatura'] = mat
            info['Salon'] = salon
            horario[b][d] = info
        return True
    return False
# Nota mental: NO se exactamente para que es est ultimo, no se su utilidad.


def generar_horarios(horarios_dict, asignaturas_dict, materias_dict, sandwich, disponibilidad_profesores):
    """
    Genera todos los semestres con backtracking y restricciones completas:
    - Bloques fijos
    - No repetición en el mismo día
    - Disponibilidad y horas máximas de profesores
    - Laboratorios de cómputo (salones reales)
    - Huecos (entrada/salida/sandwich) según parámetro
    """

    # Ordena los semestres de menor a mayor
    semestres = sorted(horarios_dict.keys())

    # ---- Sumamos las horas totales que el profe debe impartir dependiendo de las materias ----
    # .items basicamente es la tupla de datos.
    for prof, datos in disponibilidad_profesores.items(): # Agarra a un prof junto con sus horas_max
        horas_necesarias = 0

        for sem in semestres: # Revisamos cada diccionario de materias
            asignaturas = asignaturas_dict[sem]

            for mat, info in asignaturas.items(): # Revisa cada materia de cada diccionario
                # Si el maestro de esa materia es igual al nombre del profesor entonces se le suman
                # la cantidad de bloques esa materia es necesario que aparezca
                if info['Maestro'] == prof:
                    horas_necesarias += info['Bloques']

        # Si las horas necesarias TOTALES (ya considerando todas las materias que da en todos los semestres) es
        # MAS que el maximo de horas que el profesor puede dar, mostramos un error.
        if horas_necesarias > datos['max_horas']:
            raise ValueError(f"El profesor {prof} requiere {horas_necesarias} bloques, "f"pero su máximo es {datos['max_horas']}.")


    # Estructuras globales
    prof_ocupado = {}
    lab_ocupado = {}


    # Aprovehcando que este esta solo lo explicao.
    # Esto se le conoce (no me preguntes porque existe) como Dictionary Comprehension,
    # creamos otro diccionario llamado prof_horas_restantes, pasandole info especifica, nos ayuda evitando escribir
    # nuevos diccionarios de agrapa.
    # Cuando se itera sobre disponibilidad guardamos la tupla nombre, max_horas en prof y datos respectivamente
    # y estas tuplas clave-valor se agregan al diccionario PROF_HORAS_RESTANTES en formato
    # prof: datos['max_horas'] 
    prof_horas_restantes = {prof: datos['max_horas'] for prof, datos in disponibilidad_profesores.items()} 

    # Llenamos todo con None, otra vez ...
    for sem in semestres:
        horario = horarios_dict[sem]
        for fila in horario:
            for d in range(DIAS):
                fila[d] = None

        materias = materias_dict[sem] # Guardamos la materia actual (nombres)
        asignaturas = asignaturas_dict[sem] # Guardamos la asignatura actual (datos)
        requeridos = {mat: asignaturas[mat]['Bloques'] for mat in materias} # Dictionary Comprehension
        total_bloques = sum(requeridos.values()) # Se suma la cantidad bloques totales para saber cuantos bloques se llenaran 

        huecos_ocupados = _definir_huecos_ocupados(sandwich, total_bloques)

        exito = restricciones(horario, materias, requeridos, asignaturas, huecos_ocupados, prof_ocupado, lab_ocupado, disponibilidad_profesores, prof_horas_restantes)
        if not exito:
            print(f"No se pudo generar el horario del semestre {sem}. Reintentando...")
            for _ in range(10):
                huecos_ocupados = _definir_huecos_ocupados(sandwich, total_bloques)
                exito = restricciones(horario, materias, requeridos, asignaturas, huecos_ocupados, prof_ocupado, lab_ocupado, disponibilidad_profesores, prof_horas_restantes)
                if exito:
                    break
            if not exito:
                print(f"Falló la generación de horario del semestre {sem}.")



def _definir_huecos_ocupados(sandwich, total_bloques):
    """
    Devuelve una lista de (d,b) que estarán ocupados (len == total_bloques).
    Si sandwich = True, se reparten huecos de forma que como máximo un bloque
    libre por día (entrada, sandwich o salida) y se respeta el total de bloques.
    Si no, se eligen aleatoriamente los slots necesarios.
    """

    # Dictionary Comprehension
    # Creamos un diccionario todos_huecos en formato "d, b" siendo de 5 (0-4/Lunes-Viernes) por 3 (0-3/A, B, C). 
    todos_huecos = [(d, b) for d in range(DIAS) for b in range(BLOQUES)]
    # Sabemos que son 5 dias y 3 bloques, dando un total de todos_huecos = 15.
    # Podriamos agregar un condicionardor a que si es menor a 10 no se pueden acomodar los horarios


    # Aleatoriedad en los dias con dia libre y los dias sin dia libre
    if sandwich:
        libres = 15 - total_bloques
        # random.sample() escoge de 
        dias_con_hueco = random.sample(range(5), libres) if libres > 0 else []

        # bloques_libres = Por cada dia con hueco guardaremos los bloques libre en formatos aletorios, 
        # de A, B y C.
        bloques_libres = {d: random.choice([0,1,2]) for d in dias_con_hueco}
        slots = []

        # Avanzamos dia a dia
        for d in range(5):
            # Si el dia de hoy esta dentro de los bloques_libres
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
def format_horario(horario, semestre = None):
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


# Muetra el horario 
def mostrar_horario(horario, semestre = None):
    print(format_horario(horario, semestre))


# Exporta los horarios 
def guardar_horario(horario, nombre_archivo, semestre = None, titulo_custom = None):
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    ruta_horarios = os.path.join(ruta_base, "Horarios")

    if not os.path.exists(ruta_horarios):
        os.makedirs(ruta_horarios)

    ruta_completa = os.path.join(ruta_horarios, f"{nombre_archivo}.txt")

    with open(ruta_completa, "w", encoding = "utf-8") as f:
        f.write("--- REPORTE DE HORARIO ---\n\n")
        
        # Si titulo_custom existe, lo usamos para el reporte
        if titulo_custom:
            original_format = format_horario(horario, semestre)
            f.write(original_format.replace("Horario", titulo_custom))
        else:
            f.write(format_horario(horario, semestre))
            
        f.write("\n\n" + "-"*30 + "\n")
        f.write("Detalles de las Asignaturas:\n")
        f.write("-"*30 + "\n")
        materias_vistas = set()
        for fila in horario:
            for celda in fila:
                if celda and not isinstance(celda, str) and celda['Asignatura'] not in materias_vistas:
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
                if celda and celda.get('Tipo') == 'laboratorio':
                    salon = celda['Salon']
                    if salon in labs:
                        # Guardamos la celda completa para poder usar format_horario y guardar_horario
                        labs[salon][b][d] = celda

    # Mostrar cada laboratorio
    for nombre_lab, matriz in labs.items():
        print(f"\n--- Uso de {nombre_lab} ---")
        lin = format_horario(matriz, semestre=None)
        # Reemplazar título genérico
        lin = lin.replace("Horario", f"Laboratorio {nombre_lab}")
        print(lin)

def guardar_horarios_laboratorios(horarios_semestres):
    """
    Exporta los horarios de los laboratorios a archivos .txt
    """
    labs = {'Computo 1': None, 'Computo 2': None}
    for lab in labs:
        labs[lab] = [[None for _ in range(5)] for _ in range(3)]

    for sem, horario in horarios_semestres.items():
        for b in range(3):
            for d in range(5):
                celda = horario[b][d]
                if celda and celda.get('Tipo') == 'laboratorio':
                    salon = celda['Salon']
                    if salon in labs:
                        labs[salon][b][d] = celda

    for nombre_lab, matriz in labs.items():
        nombre_archivo = f"Horario_{nombre_lab.replace(' ', '_')}"
        guardar_horario(matriz, nombre_archivo, semestre=None, titulo_custom=f"Laboratorio {nombre_lab}")