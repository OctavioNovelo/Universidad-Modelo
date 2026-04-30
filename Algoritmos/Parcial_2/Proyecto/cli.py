def menu():
    print("\n --- Generador de horarios --- \n")
    print("\n 1) Generar Horarios.")
    print("\n 2) Ver horarios. \n")

'''
def seleccion():
    menu()
    opcion = input("Selecciona una opción: ")
    # Ajustamos el match para comparar strings
    match opcion:
        case '1':
            # Preguntar si se quiere horario sándwich
            resp = input("¿Horario sándwich (bloque B libre)? (s/n): ").lower()
            sandwich = resp == 's'
            generar_horario(horario, asignaturas, sandwich)
            print("Horario generado.\n")
        case '2':
            mostrar_horario(horario)
        case _:
            print("Opción no válida.\n")
'''