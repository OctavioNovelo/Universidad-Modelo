import subprocess
import horario

# Cada celda será un diccionario o none si está libre.
# Al principio definimos todo como none
horarios_semestres = {
    1: [[None for _ in range(5)] for _ in range(3)],
    2: [[None for _ in range(5)] for _ in range(3)],
    3: [[None for _ in range(5)] for _ in range(3)],
    4: [[None for _ in range(5)] for _ in range(3)]
}

# ------------------------------------------------------------
# Diccionarios de asignaturas por semestre
asignaturas_semestre_2 = {
    'Algoritmos': {'Maestro': 'Edson Geovanny Estrada Lopez', 'Salon': 'Computo 2'},
    'Algebra matricial y vectorial': {'Maestro': 'Ing. Juan Norberto Peniche Munoz', 'Salon': 'A1'},
    'Fisica aplicada': {'Maestro': 'Dr. Alberto Gabriel Vega Poot', 'Salon': 'A1'},
    'Calculo diferencial': {'Maestro': 'Mtra. Aylin Garcia Reyes', 'Salon': 'A1'},
    'Sistemas Operativos': {'Maestro': 'Mtro. Alfredo Jose Bolio Dominguez', 'Salon': 'A1'},
    'Redes de computadoras': {'Maestro': 'Ing. Franklin Jesus Gonzales Torres', 'Salon': 'A1'},
}

asignaturas_semestre_4 = {
    'Estadistica Inferencial': {'Maestro': 'Mtra. Aylin Garcia Reyes', 'Salon': 'A2'},
    'Ingenieria ecnonomica': {'Maestro': 'Ing. Juan Norberto Peniche Munoz', 'Salon': 'A2'},
    'Circuitos electricos y electronicos': {'Maestro': 'Edson Geovanny Estrada Lopez', 'Salon': 'A2'},
    'Programacion aplicada a videojuegos': {'Maestro': 'Ing. Jesus Alejandro Balam Sandoval', 'Salon': 'Computo 1'},
    'Base de datos II': {'Maestro': 'Mtro. Alfredo Jose Bolio Dominguez', 'Salon': 'A2'},
    'Fundamentos de diseno': {'Maestro': 'Mtro. Daniel Alejandro Martinez Lopez', 'Salon': 'A2'},
}

asignaturas_semestre_6 = {
    'Sistemas graficos': {'Maestro': 'Mtro. Alfredo Jose Bolio Dominguez', 'Salon': 'A3'},
    'Desarrollo Web II': {'Maestro': 'Mtro. Daniel Alejandro Martinez Lopez', 'Salon': 'A3'},
    'Proyeccion y modelado de software': {'Maestro': 'Edson Geovanny Estrada Lopez', 'Salon': 'Computo 2'},
    'Internet de las cosas': {'Maestro': 'Ing. Franklin Jesus Gonzales Torres', 'Salon': 'A3'},
    'Aministracion de procesos de negocios': {'Maestro': 'Mtra. Vanessa Cob Gutierrez', 'Salon': 'A3'},
    'Desarrollo movil I': {'Maestro': 'Ing. Jesus Alejandro Balam Sandoval', 'Salon': 'A3'},
}

asignaturas_semestre_8 = {
    'Desarrollo de videojuegos': {'Maestro': 'Ing. Jesus Alejandro Balam Sandoval', 'Salon': 'A4'},
    'Analisis politico y socieconomico de mexico': {'Maestro': 'Mtra. Vanessa Cob Gutierrez', 'Salon': 'A4'},
    'Innovacion y emprendimiento': {'Maestro': 'Mtra. Kenia Nayrhovy Osorio Lopez', 'Salon': 'A4'},
    'Ambientes y arquitectura de microservidores': {'Maestro': 'Edson Geovanny Estrada Lopez', 'Salon': 'A4'},
    'Seguridad de software': {'Maestro': 'Mtro. Alfredo Jose Bolio Dominguez', 'Salon': 'A4'},
    'Desarrollo basado en agentes': {'Maestro': 'Mtro. Daniel Alejandro Martinez Lopez', 'Salon': 'Computo 1'},
}

# Listas de materias por semestre.
materias_semestre_2 = list(asignaturas_semestre_2.keys())[:6]
materias_semestre_4 = list(asignaturas_semestre_4.keys())[:6]
materias_semestre_6 = list(asignaturas_semestre_6.keys())[:6]
materias_semestre_8 = list(asignaturas_semestre_8.keys())[:6]
# ------------------------------------------------------------

def menu():
    print("\n --- Generador de horarios --- \n")
    print("\n 1) Generar Horarios.")
    print("\n 2) Ver horarios.")
    print("\n 3) Salir. \n")

def seleccion():
    subprocess.run(["clear"])
    menu()
    opcion = input("Selecciona una opción: ")
    match opcion:
        case '1':
            subprocess.run(["clear"])
            a = input("El horario puede tener horas muertas? (s/n): ").lower()
            sandwich = False
            if a == 's':
                sandwich = True

            # Diccionarios de asignaturas (Esta incluye a los profesores y salones)
            asignaturas_por_sem = {
                1: asignaturas_semestre_2,
                2: asignaturas_semestre_4,
                3: asignaturas_semestre_6,
                4: asignaturas_semestre_8
            }

            # Estas son las diferentes materias que hay por semestre
            materias_por_sem = {
                1: materias_semestre_2,
                2: materias_semestre_4,
                3: materias_semestre_6,
                4: materias_semestre_8
            }

            print("\nGenerando horarios...\n")
            horario.generar_horarios(horarios_semestres, asignaturas_por_sem, materias_por_sem, sandwich)

            # ------------------------------------------------------------
            # En este bloque exportamos los horarios
            for i in range(1, 5):
                nombres = {
                    1: "Segundo Semestre",
                    2: "Cuarto Semestre",
                    3: "Sexto Semestre",
                    4: "Octavo Semestre"
                }
                horario.guardar_horario(horarios_semestres[i], nombres[i], i)
            # ------------------------------------------------------------

            print("\nTodos los horarios han sido generados.\n")
            input("Presiona una tecla para continuar...")

        case '2':
            subprocess.run(["clear"])
            print("\n Horario de qué semestre desea ver? ")
            print("\n 1) Segundo semestre.")
            print("\n 2) Cuarto semestre.")
            print("\n 3) Sexto semestre.")
            print("\n 4) Octavo semestre.\n")

            a = int(input(": "))
            
            if a in horarios_semestres:
                subprocess.run(["clear"])
                horario.mostrar_horario(horarios_semestres[a], a)
            else:
                print("Opción no válida.")
        
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
