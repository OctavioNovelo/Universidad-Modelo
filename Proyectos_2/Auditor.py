# This is the beginning of the Auditor project
from frontend.CLI import CLI
import sys
from core.compiler import ToolCompiler
from pathlib import Path

def main():
    # Use the --compile argument to compile the program(s)
    if "--compile" in sys.argv:
        print("[*] Compiling tools...")
        ToolCompiler(Path(__file__).parent).compile_nmap()
        return
    
    # Run the CLI
    CLI().run()

# Es para ejecutar el programa
if __name__ == "__main__":
    main()
