import timeit

# Recreamos tus datos de cli.py para la prueba
disponibilidad_profesores = { 
    'Edson Geovanny Estrada Lopez': {'max_horas': 12},
    'Ing. Juan Norberto Peniche Munoz': {'max_horas': 10},
    'Dr. Alberto Gabriel Vega Poot': {'max_horas': 10},
    'Mtra. Aylin Garcia Reyes': {'max_horas': 12},
    'Mtro. Alfredo Jose Bolio Dominguez': {'max_horas': 10},
    'Ing. Franklin Jesus Gonzales Torres': {'max_horas': 10},
    'Ing. Jesus Alejandro Balam Sandoval': {'max_horas': 10},
    'Mtro. Daniel Alejandro Martinez Lopez': {'max_horas': 10},
    'Mtra. Vanessa Cob Gutierrez': {'max_horas': 8},
    'Mtra. Kenia Nayrhovy Osorio Lopez': {'max_horas': 6},
    'Mtra. Ana Bolio Ayora': {'max_horas': 10},
    'Mtra. Grety del Socorro Basulto Morcillo': {'max_horas': 10},
    'Mtro. Roberto Carlos Gamboa Ek': {'max_horas': 10}
}

# --- Metodo 1: Ciclo For Tradicional ---
def test_con_for():
    prof_horas_restantes = {}
    for prof, datos in disponibilidad_profesores.items():
        prof_horas_restantes[prof] = datos['max_horas']
    return prof_horas_restantes

# --- Metodo 2: Dictionary Comprehension (Tu codigo actual) ---
def test_con_comprehension():
    return {prof: datos['max_horas'] for prof, datos in disponibilidad_profesores.items()}

# Ejecutamos cada uno 500,000 veces para notar la diferencia
intentos = 500000
tiempo_for = timeit.timeit(test_con_for, number=intentos)
tiempo_comp = timeit.timeit(test_con_comprehension, number=intentos)

print(f"--- Resultados (Tras {intentos} ejecuciones) ---")
print(f"Ciclo FOR tradicional:   {tiempo_for:.5f} segundos")
print(f"Dict Comprehension:      {tiempo_comp:.5f} segundos")
print(f"Diferencia real:         {abs(tiempo_for - tiempo_comp):.5f} segundos")