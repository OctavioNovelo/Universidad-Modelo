# Aqui reciviremos el primer input para ejecutar la herramienta.
import core.executor
import platform

def obtener_sistema_operativo():
    return platform.system()
os = obtener_sistema_operativo()

def opciones (opcion = lambda s: s):
    match opcion:
        case 1:
            print("\n Abriendo Nmap \n")
            tool = "Nmap"
            core.executor.ejecutar_segun_os(os, tool)
            core.executor.confirm = True
            return core.executor.confirm
        case 2:
            print("\n Abriendo J.T.R \n")
        case 3:
            print("\n Luego Vemos \n")
