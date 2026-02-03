import subprocess
from pathlib import Path
import os

# Ejecuta el programa
class ToolExecutor:
    # El path del binario
    def __init__(self, base_dir: Path):
        self.bin_dir = base_dir / "tools_bin"
    
    # Definicion de la herramiento que se va a usar (en este caso solo es nmap)
    def run(self, tool: str, args: list[str]):
        binary = self.bin_dir / tool / tool

        # Si no esta, suelta error
        if not binary.exists():
            raise RuntimeError(f"{tool} no está compilado")
        
        # Le da permisos de execucion
        os.chmod(binary, 0o755)

        # Se guarda el output 
        result = subprocess.run(
            [str(binary)] + args,
            capture_output = True,
            text = True
        )

        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
