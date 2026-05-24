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
import json

# Con esta funciona procesamos los json 
def load_json(filename):
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    ruta_json = os.path.join(ruta_base, "json", filename)
    with open(ruta_json, "r", encoding="utf-8") as f:
        return json.load(f)

# ---------------------------------------------------------------------
# Constantes
DIAS = 5                     # Lunes a Viernes
BLOQUES = 3                  # A, B, C
# ---------------------------------------------------------------------


# AGREGAMOS SANDWICH Y TOTAL BLOQUES
def generador(horarios_dict,materias_dict,asignaturas_dict,prof_ocupado,lab_ocupado,disponibilidad_profesores,prof_horas_restantes,sandwich,pendientes):
    """
    Argumentos:
        horario: matriz 3x5 (Bloques x Dias)
        materias: lista de nombres (6)
        requeridos: frecuencia requerida de cada materia
        asignaturas: diccionario completo de la asignatura
        prof_ocupado: dict (d,b) -> set de profes ocupados
        lab_ocupado: dict (d,b) -> set de salones de cómputo ocupados
        disponibilidad_profesores: diccionario con max_horas y disponibilidad (3 x 5)
        prof_horas_restantes: dict con las horas que le quedan a cada profesor
        sandwich: bool, permite o no el horario sándwich
        total_bloques: int, total de bloques a cubrir
    Retorna True si encontró asignación válida.
    """

    # Diccionario, aqui guardaemos los bloques del horario, con profesor, materia y salon asignados. 
    asignacion = {}

    # Este es un diccionario llamado usadas que guarda las materias de la lista materias con un value de 0. 
    # Este es el diccionario donde veremos con que frecuencia aparece cada materia. 
    usadas = {}
    requeridos = {}
    semestres = list(horarios_dict.keys())
    #NO sirven aun
    for sem in semestres:
        materias_sem = materias_dict[sem]
        asignaturas_sem = asignaturas_dict[sem]
        for mat in materias_sem:
            usadas[(sem, mat)] = 0
            requeridos[(sem, mat)] = asignaturas_sem[mat]['Bloques']
    
    # FILTRO MATERIAS -----------------------------------------------------------------------
    # Esta diccionario lo cree con el unico objetivo de que no se dupliquen las mateiras
    materias_por_dia = {}
    for dia in range(DIAS):
        materias_por_dia[dia] = set() # TRUCASO GENTE
        # Resulta que set() es una funcion que CREA CONJUNTOS.
        # Los conjuntos son estructuras que solo almacenan datos (Lit no tienen orden ni nada, solo los almacena)
        # pero con la ventaja de que NO permite datos duplicados, elimina el duplicado y que es mucho mas rapida
        # cuando queremos hacer operaciones "in" "not in" que es justo lo que necesitamos para saber si el conjunto (el dia)
        # ya tiene la materia que estamos intentando agregar.
        
        # ME CONFUNDI YO SOLO SOY IDIOTA
        # AQUI ESTA LA EXPLICACION DEL SET NA MAS PORQUE ESTA SOLITO
        # LAS MATERIAS QUE AGREGAMOS TIENEN UN CONJUTO VACIO COMO KEY PUES NO NECESITAMOS SU INFO, SOLO SU NOMBRE


        # Creamos 5 conjuntos vacios (dias)
    # ACABA FILTRO MATERIAS ----------------------------------------------------------------------------------------

    # Huecos
    # ANTES USABAMOS LA FUNCION DE HUECOS
    huecos = []
    for d in range(DIAS):
        for b in range(BLOQUES):
            huecos.append((d, b))

    def generar_horarios(index):
        # Caso base: si ya procesamos todas las materias de pendientes,verificamos que todas quedaron completas
        if index == len(pendientes):
            for clave in usadas:
                if usadas[clave] != requeridos[clave]:
                    return False
            return True
        
        # Tomamos la materia que toca colocar en este nivel de recursion
        sem, mat_actual = pendientes[index]
        # Si esta materia ya tiene todos sus bloques colocados por una instancia anterior, simplemente avanzamos sin hacer nada
        if usadas[(sem, mat_actual)] >= requeridos[(sem, mat_actual)]:
            return generar_horarios(index + 1)


        horario_actual = horarios_dict[sem]
        asignaturas_actual = asignaturas_dict[sem]
        # Probamos cada hueco disponible (dia, bloque) uno por uno
        for d, b in huecos:
        # El hueco ya esta ocupado por otra materia, lo saltamos
            if horario_actual[b][d] is not None:
                continue

        # Esta materia ya aparece en este dia, no puede repetirse
            if mat_actual in materias_por_dia[d]:
                continue

        # Ya colocamos todos los bloques necesarios de esta materia
            if usadas[(sem, mat_actual)] >= requeridos[(sem, mat_actual)]:
                continue

        # FILTRO SANDWICH
        # Si sandwich=False, no podemos poner algo en C (bloque 2) si A tiene materia pero B está vacío
            if not sandwich and b == 2:
                bloque_a = horario_actual[0][d]
                bloque_b = horario_actual[1][d]
                if bloque_a is not None and bloque_b is None:
                    continue

        # FILTROS DE PROFESOR
            prof = asignaturas_actual[mat_actual]['Maestro']
            tipo = asignaturas_actual[mat_actual].get('Tipo', 'normal')
            salon = asignaturas_actual[mat_actual]['Salon']

        # El profesor ya esta ocupado en este dia y bloque en otro semestre
            if prof in prof_ocupado.get((d, b), set()):
                continue

        # Disponibilidad del profesor
            dispo_default = []
            for _ in range(3):
                fila_dispo = []
                for _ in range(5):
                    fila_dispo.append(True)
                dispo_default.append(fila_dispo)

            disp = disponibilidad_profesores.get(prof, {'disponibilidad': dispo_default})
            # El profesor no esta disponible en este dia y bloque
            if not disp['disponibilidad'][b][d]:
                continue

        # El profesor ya agoto sus horas maximas permitidas
            if prof_horas_restantes.get(prof, 0) <= 0:
                continue

        # El laboratorio ya esta ocupado en este dia y bloque
            if tipo == 'laboratorio':
                if salon in lab_ocupado.get((d, b), set()):
                    continue

        #  El hueco paso todos los filtros, lo asignamos provisionalmente 
            asignacion[(sem,d, b)] = (sem, mat_actual, prof, salon)
            horario_actual[b][d] = mat_actual
            usadas[(sem, mat_actual)] += 1
            materias_por_dia[d].add(mat_actual)
            prof_ocupado.setdefault((d, b), set()).add(prof)
            if tipo == 'laboratorio':
                lab_ocupado.setdefault((d, b), set()).add(salon)
            prof_horas_restantes[prof] -= 1

            # Avanzamos a la siguiente materia en pendientes
            # Si toda la rama que sigue funciona, retornamos True hacia arriba
            if generar_horarios(index + 1):
                return True

        # La rama fallo, deshacemos este hueco y probamos el siguiente
            del asignacion[(sem,d, b)]
            horario_actual[b][d] = None
            usadas[(sem, mat_actual)] -= 1
            materias_por_dia[d].remove(mat_actual)
            prof_ocupado[(d, b)].remove(prof)

            if not prof_ocupado[(d, b)]:
                del prof_ocupado[(d, b)]

            if tipo == 'laboratorio':
                lab_ocupado[(d, b)].remove(salon)
                if not lab_ocupado[(d, b)]:
                    del lab_ocupado[(d, b)]
            prof_horas_restantes[prof] += 1
            # El for continua automaticamente al siguiente hueco (d, b)

        # Ningún hueco funciono para esta materia en este nivel,
       # le avisamos al nivel anterior que retroceda y pruebe otro hueco    
        return False
    resultado = generar_horarios(0)

    if resultado:
        for sem in horarios_dict:
            for fila in horarios_dict[sem]:
                for d in range(DIAS):
                    fila[d] = None

     
        for (sem,d, b), data in asignacion.items():
            if data is None:
                continue
            _, mat, _, salon = data
            info = asignaturas_dict[sem][mat].copy()
            info['Asignatura'] = mat
            info['Salon'] = salon
            horarios_dict[sem][b][d] = info
        return True

    return False



def llenar_horario(horarios_dict, asignaturas_dict, materias_dict, sandwich, disponibilidad_profesores):
    semestres = horarios_dict.keys()

    # Sumamos las horas totales que el profe debe impartir dependiendo de las materias
    # .items basicamente son todas las tupla del diccionario DISPONIBILIDAD_PROFESORES.
    for prof, datos in disponibilidad_profesores.items(): # Agarra a un prof junto con sus horas_max
        horas_necesarias = 0

        for sem in semestres: # Revisamos cada diccionario de materias (materias_semestre_2, 4, 6, 8)
            # Asignaturas guarda el DICCIONARIO de las materias que contiene (profesores, salones, bloques, tipo)
            # Por cada hueco/espacio en la cuadricula del horario (semestres) asignaturas guarda todas las keys 
            # de la materia de turno. 
            asignaturas = asignaturas_dict[sem]

            for mat, profe in asignaturas.items(): # Revisa cada materia de cada diccionario (las materias individuales)
                # Si el maestro de esa materia es igual al nombre del profesor entonces se le suman
                # la cantidad de bloques que esa materia tiene que aparecer
                # De esta forma calculamos la cantidad de bloques que cada profesor debe ensenar. 
                if profe['Maestro'] == prof:
                    horas_necesarias += profe['Bloques']
                    
        # Si las horas necesarias TOTALES (ya considerando todas las materias que da en todos los semestres) es
        # MAS que el maximo de horas que el profesor puede dar, mostramos un error.
        if horas_necesarias > datos['max_horas']:
            print(f"El profesor {prof} requiere {horas_necesarias} bloques, "f"pero su máximo es {datos['max_horas']}.")
            input("Presione una tecla para continuar...")
            return False


    # Estructuras globales
    prof_ocupado = {}
    lab_ocupado = {}


    # Creamos otro diccionario llamado prof_horas_restantes, pasandole info especifica.
    # Cuando se itera sobre disponibilidad guardamos la tupla nombre, max_horas en prof y datos respectivamente
    # y estas tuplas clave-valor se agregan al diccionario PROF_HORAS_RESTANTES en formato
    # prof: datos['max_horas'] 
    prof_horas_restantes = {}
    for prof, datos in disponibilidad_profesores.items():
        prof_horas_restantes[prof] = datos['max_horas']

    # Llenamos todo con None, otra vez ...
    for sem in semestres:
        horario = horarios_dict[sem]
        for fila in horario:
            for d in range(DIAS):
                fila[d] = None
    pendientes = []

    for sem in semestres:
        materias = materias_dict[sem]
        asignaturas = asignaturas_dict[sem]
        for mat in materias:
            bloques = asignaturas[mat]['Bloques']
            for _ in range(bloques):
                pendientes.append((sem, mat))               
          

    exito = generador(horarios_dict,materias_dict, asignaturas_dict,prof_ocupado,lab_ocupado,disponibilidad_profesores,prof_horas_restantes,sandwich,pendientes)     
          
    if not exito:
        print("No se pudo generar un horario válido.")

        for s in semestres:
            h = horarios_dict[s]
            for fila in h:
                for d in range(DIAS):
                    fila[d] = None
        return False
    return True

# --------------------------------------------------------------------------------------
# Formato y visualización
def format_horario(horario, semestre = None):
    dias = ['LUNES', 'MARTES', 'MIÉRCOLES', 'JUEVES', 'VIERNES']
    encabezados = ['HORA'] + dias
    bloques_nombre = ['7:00 - 9:00', '9:00 - 11:00', '11:00 - 13:00']

    nombres_semestres_raw = load_json('nombres_semestres.json')
    nombres_semestres = {}
    for k, v in nombres_semestres_raw.items():
        nombres_semestres[int(k)] = v
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
    
    # Reemplazamos Generator Expression dentro de join por ciclo FOR tradicional
    encabezado_piezas = []
    for col in range(6):
        texto_ajustado = ajustar(encabezados[col], anchos[col])
        encabezado_piezas.append(texto_ajustado.center(anchos[col]))
    encabezado_str = '|' + '|'.join(encabezado_piezas) + '|'
    
    resultado.append(encabezado_str)
    resultado.append(separador)
    for fila in filas_texto:
        # Reemplazamos Generator Expression dentro de join por ciclo FOR tradicional
        fila_piezas = []
        for col in range(6):
            fila_piezas.append(fila[col].center(anchos[col]))
        linea = '|' + '|'.join(fila_piezas) + '|'
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


# Profe estas dos se las pedi a chat ya me habia cansado uwu.
def mostrar_horarios_laboratorios(horarios_semestres):
    """
    Muestra dos tablas (Computo 1 y Computo 2) con las materias que los ocupan.
    """
    labs = load_json('labs.json')
    # Inicializar matrices vacías (5 días x 3 bloques)

    for lab in labs:
        # Reemplazamos List Comprehension por ciclo FOR tradicional
        matriz_lab = []
        for _ in range(3):
            fila_lab = []
            for _ in range(5):
                fila_lab.append(None)
            matriz_lab.append(fila_lab)
        labs[lab] = matriz_lab

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
    labs = load_json('labs.json')
    for lab in labs:
        # Reemplazamos List Comprehension por ciclo FOR tradicional
        matriz_lab = []
        for _ in range(3):
            fila_lab = []
            for _ in range(5):
                fila_lab.append(None)
            matriz_lab.append(fila_lab)
        labs[lab] = matriz_lab

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
# --------------------------------------------------------------------------------------