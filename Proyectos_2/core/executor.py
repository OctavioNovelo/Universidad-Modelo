# core/executor.py
import subprocess
from pathlib import Path
import os

class ToolExecutor:
    def __init__(self, base_dir: Path):
        self.bin_dir = base_dir / "tools_bin"

    def run(self, tool: str, args: list[str]):
        binary = self.bin_dir / tool / tool

        if not binary.exists():
            raise RuntimeError(f"{tool} no está compilado")

        os.chmod(binary, 0o755)

        result = subprocess.run(
            [str(binary)] + args,
            capture_output=True,
            text=True
        )

        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
