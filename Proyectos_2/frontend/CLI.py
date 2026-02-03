# frontend/cli.py
from tools.nmap import NmapCommands
from core.executor import ToolExecutor
from pathlib import Path

class CLI:
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
