# This is the beginning of the Auditor project
from frontend.CLI import CLI
import sys
from core.compiler import ToolCompiler
from pathlib import Path

def main():
    if "--compile" in sys.argv:
        print("[*] Compiling tools...")
        ToolCompiler(Path(__file__).parent).compile_nmap()
        return

    CLI().run()
    
if __name__ == "__main__":
    main()
