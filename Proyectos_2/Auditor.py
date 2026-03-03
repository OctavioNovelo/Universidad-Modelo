# This is the beginning of the Auditor project
from utils import Input
from core import executor
import sys
from pathlib import Path

def main():
    so = Input.obtener_sistema_operativo()
    executor.ejecutar_segun_os(so, tool)

# Es para ejecutar el programa
if __name__ == "__main__":
    main()
