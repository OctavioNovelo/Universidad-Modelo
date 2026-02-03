from tools.nmap import NmapCommands # Lo comandos de nmap.py
from core.executor import ToolExecutor
from pathlib import Path

# Inicializamos interfaz
class CLI:
    # Ejecuta el ejecutor
    def __init__(self):
        self.executor = ToolExecutor(Path(__file__).parent.parent)

    def run(self):
        print("1) Fast scan")
        print("2) Version scan")
        print("3) OS scan")
        print("4) Aggressive scan")

        opt = int(input("> "))
        target = input("Target: ")

        args = NmapCommands.build(opt, target)
        result = self.executor.run("nmap", args)

        print(result["stdout"])
