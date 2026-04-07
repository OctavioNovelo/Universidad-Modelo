# core/executor.py
import subprocess
import platform
import os
from pathlib import Path
from tools.nmap import nmap_bin

def obtener_sistema_operativo():
    return platform.system()

def obtener_carpeta_os(os_name):
    if 'Win' in os_name:
        return 'Windows'
    elif 'Darwin' in os_name or 'mac' in os_name:
        return 'macos'
    elif 'Linux' in os_name:
        return 'Linux'
    else:
        raise ValueError(f"Sistema operativo no soportado: {os_name}")

def obtener_ruta_binario(tool, os_folder):
    base_path = Path(__file__).parent.parent
    bin_name = nmap_bin[os_folder.lower()]['bin_name']
    return base_path / "tools" / "tools_bin" / os_folder / tool / bin_name

def obtener_ruta_resultado(tool, os_folder, nombre_archivo):
    base_path = Path(__file__).parent.parent
    return base_path / "utils" / "Resultados" / os_folder / tool / nombre_archivo

def ejecutar_herramienta(tool, os_folder):
    base_path = Path(__file__).parent.parent
    bin_name  = nmap_bin[os_folder.lower()]['bin_name']
    bin_path  = base_path / "tools" / "tools_bin" / os_folder / tool / bin_name

    if not bin_path.exists():
        raise FileNotFoundError(f"Binario no encontrado: {bin_path}")

    os.chmod(bin_path, 0o755)

    ip_result = subprocess.run("ip route | grep kernel | grep -vE 'docker|br-' | awk '{print $1}'", shell = True, capture_output = True, text = True)
    redes = ip_result.stdout.strip().split("\n")

    return {"bin_path": bin_path, "os_folder": os_folder, "redes": redes}