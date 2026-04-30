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

def generar_horarios(horarios_dict, asignaturas_dict, materias_dict, sandwich=False):
    """
    horarios_dict: diccionario de matrices 3x5 (los horarios vacios)
    asignaturas_dict: diccionario de asignaturas (nombre, maestro y salon)
    materias_dict: diccionario de las materias por semestre (Las materias del 2, 4, 6 y 8 semestre son diferentes)
    """

    semestres = sorted(horarios_dict.keys())   # [1,2,3,4]
    # .keys sirve para acceder a los datos key del diccionario
    # horarios_dict.keys() = ""
    # En esta caso lit esta vacio porque son los horarios 3x5.

    # ------------------------------------------------------------
    # Logica
    # 1. Determinar los slots ocupados para cada semestre
    slots_por_semestre = {}   # sem -> lista de (dia, bloque)
    for sem in semestres:
        horario = horarios_dict[sem] # 1

        # Limpiamos los horarios 
        for fila in horario:
            for d in range(5):
                fila[d] = None

        slots = [] # Otra variable de slots

        # ------------------------------------------------------------
        # Logica para los diferentes combinaciones de los horarios libres
        if sandwich:
            # Si 0 < k < 1 entonces ese dia tendra una hora libre
            k = random.randint(0, 1)                 
            dias_libre = random.sample(range(5), k) # Como asi ?
            libre_por_dia = {}
            for d in dias_libre:
                libre_por_dia[d] = random.choice([0, 1, 2])   # A, B o C libre
                # Las combinaciones sirven para determinar si el dia tiene horario sandwich, entra tarde y sale temprano.

            for d in range(5):
                if d in libre_por_dia:
                    bloque_libre = libre_por_dia[d]
                    for b in range(3):
                        if b != bloque_libre:
                            slots.append((d, b))
                else:
                    for b in range(3):
                        slots.append((d, b))

        else:
            for d in range(5):
                for b in range(3):
                    slots.append((d, b))

        slots_por_semestre[sem] = slots
        # ------------------------------------------------------------

    # 2. Registro global de profesores ocupados en cada (dia, bloque)
    ocupacion_profesor = {}   # (dia, bloque) -> set de nombres de profesores

    # 3. Generar cada semestre secuencialmente
    for sem in semestres:
        horario = horarios_dict[sem]
        materias = materias_dict[sem]
        asignaturas = asignaturas_dict[sem]
        slots = slots_por_semestre[sem]

        # Frecuencias
        frecuencias = [1] * 6
        restantes = len(slots) - 6
        while restantes > 0:
            idx = random.randrange(6)
            # que hace randrange ? 
            if frecuencias[idx] < 3:
                frecuencias[idx] += 1
                restantes -= 1

        # Pool de materias (con su profesor)
        pool_original = []
        for mat, freq in zip(materias, frecuencias):
            # Que hace zip() ?
            prof = asignaturas[mat]['Maestro'].strip()
            pool_original.extend([(mat, prof)] * freq)

        exito = False # Esto para que ? Lol lmao
        max_intentos = 5000 # Maximo de intento para formar horarios
        for _ in range(max_intentos):
            pool = pool_original[:]
            random.shuffle(pool)
            
            asignacion_temp = {}  # (d,b) -> (materia, profesor) o None
            materias_colocadas = set()
            
            # ------------------------------------------------------------
            # La logica de aqui es de lo mas importante ya que es lo que le estabilidad a los horarios
            valido = True # Este igual, para que ?
            for idx, (d, b) in enumerate(slots):
                mat, prof = pool[idx]

                # 1. Comprobar profesor ya ocupado (CONFLICTO)
                # Si hay conflicto, esta hora se convierte en HORA LIBRE
                if prof in ocupacion_profesor.get((d, b), set()):
                    asignacion_temp[(d, b)] = None
                    continue

                # 2. Comprobar no repetir materia en bloque contiguo
                if b == 1:   # Bloque B: verificar con A (0)
                    if (d, 0) in asignacion_temp and asignacion_temp[(d, 0)] and asignacion_temp[(d, 0)][0] == mat:
                        valido = False
                        break
                elif b == 2: # Bloque C: verificar con B (1)
                    if (d, 1) in asignacion_temp and asignacion_temp[(d, 1)] and asignacion_temp[(d, 1)][0] == mat:
                        valido = False
                        break

                asignacion_temp[(d, b)] = (mat, prof)
                materias_colocadas.add(mat)
            # ------------------------------------------------------------

            # Verificar que TODAS las materias del semestre aparezcan al menos una vez
            if valido and len(materias_colocadas) == 6:
                # Asignación exitosa
                for (d, b), data in asignacion_temp.items():
                    if data:
                        mat, prof = data
                        info = asignaturas[mat].copy()
                        info['Asignatura'] = mat
                        info['Maestro'] = prof
                        horario[b][d] = info
                        ocupacion_profesor.setdefault((d, b), set()).add(prof)
                    else:
                        horario[b][d] = None # Queda como hora libre por conflicto
                exito = True
                break

        # Wtf que esto ? 
        if not exito:
            # Fallback que TAMBIÉN respeta la ocupación de profesores
            # (Si no se logra en max_intentos, asignamos lo que se pueda)
            random.shuffle(pool_original)
            materias_asignadas_fallback = set()
            for idx, (d, b) in enumerate(slots):
                mat, prof = pool_original[idx]
                prof_stripped = prof.strip()
                if prof_stripped not in ocupacion_profesor.get((d, b), set()):
                    info = asignaturas[mat].copy()
                    info['Asignatura'] = mat
                    info['Maestro'] = prof_stripped
                    horario[b][d] = info
                    ocupacion_profesor.setdefault((d, b), set()).add(prof_stripped)
                else:
                    horario[b][d] = None # Libre por conflicto incluso en fallback


# Esta funcion le da formato a las tablas 
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
