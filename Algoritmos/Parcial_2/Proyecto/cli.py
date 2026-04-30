import subprocess
import horario

# --- Estructura del horario: 3 bloques (A, B, C) x 5 días ---
# Cada celda será un diccionario o None si está libre.
# Ahora guardamos los 4 semestres
horarios_semestres = {
    1: [[None for _ in range(5)] for _ in range(3)],
    2: [[None for _ in range(5)] for _ in range(3)],
    3: [[None for _ in range(5)] for _ in range(3)],
    4: [[None for _ in range(5)] for _ in range(3)]
}

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

def menu():
    print("\n --- Generador de horarios --- \n")
    print("\n 1) Generar Horarios.")
    print("\n 2) Ver horarios.")
    print("\n 3) Salir. \n")

def seleccion():
    subprocess.run(["clear"])
    menu()
    opcion = input("Selecciona una opción: ")
    # Ajustamos el match para comparar strings
    match opcion:
        case '1':
            subprocess.run(["clear"])
            # Preguntar si se quiere horario sándwich
            # Simplificar esto, yo no lo escribiria asi XDXDXD
            resp = input("El horario puede tener horas muertas? (s/n): ").lower()
            sandwich = resp == 's' # Wtf, como funciona esto ? 
            
            nombres = {
                1: "Segundo Semestre",
                2: "Cuarto Semestre",
                3: "Sexto Semestre",
                4: "Octavo Semestre"
            }
            
            print("\nGenerando horarios...\n")
            for i in range(1, 5):
                horario.generar_horario(horarios_semestres[i], asignaturas, materias, sandwich)
                ruta = horario.guardar_horario(horarios_semestres[i], nombres[i], i)
                # print(f"-> {nombres[i]} exportado en: {ruta}")
            
            print("\nTodos los horarios han sido generados.\n")
            input("Presiona una tecla para continuar...")
            
        case '2':
            subprocess.run(["clear"])
            print("\n Horario de qué semestre desea ver? ")
            print("\n 1) Segundo semestre.")
            print("\n 2) Cuarto semestre.")
            print("\n 3) Sexto semestre.")
            print("\n 4) Octavo semestre.\n")
            try:
                resp = int(input("Selección: "))
                if resp in horarios_semestres:
                    subprocess.run(["clear"])
                    horario.mostrar_horario(horarios_semestres[resp], resp)
                else:
                    print("Opción no válida.")
            except ValueError:
                print("Por favor, ingresa un número válido.")
            print("\n Presiona una tecla para continuar... \n")
            input()
            
        case '3':
            subprocess.run(["clear"])
            print("\n Adios! \n")
            exit()
            
        case _:
            print("Opción no válida.\n")
            input("Presiona una tecla para continuar...")

if __name__ == "__main__":
    while (True):
        seleccion()
