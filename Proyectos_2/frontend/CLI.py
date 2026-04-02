#from tools.nmap import NmapCommands # Lo comandos de nmap.py
#from core.executor import ToolExecutor
from pathlib import Path
import platform
from frontend.option import opciones

# Inicializamos interfaz
def cli ():
    print("Que desea hacer ?\n")

    print("1) Escaneo de Red\n")
    print("2) Revision de seguridad\n")
    print("3) Luego veo\n")

    opcion = int(input())
    opciones(opcion)
    