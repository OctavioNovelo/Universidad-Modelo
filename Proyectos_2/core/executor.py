# core/executor.py
import subprocess
import platform
import os
import re
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


def ejecutar_herramienta(tool, os_folder):
    base_path = Path(__file__).parent.parent
    os_name = platform.system()
    

    bin_name  = nmap_bin[os_name.lower()]['bin_name']
    bin_path  = base_path / "tools" / "tools_bin" / os_folder / tool / bin_name

    if not bin_path.exists():
        raise FileNotFoundError(f"Binario no encontrado: {bin_path}")

    if os_name != "Windows":
        os.chmod(bin_path, 0o755)

    redes = []
    if os_name == "Windows":
        # Ejecutamos ipconfig
        ip_result = subprocess.run("ipconfig", shell=True, capture_output=True, text=True)
        
        # Separamos por líneas para un procesamiento más granular
        lineas = ip_result.stdout.split('\n')
        adaptador_actual = ""
        bloques = []
        
        # Agrupamos líneas por adaptador
        temp_bloque = []
        for linea in lineas:
            if linea.strip() and not linea.startswith(" "):
                if temp_bloque:
                    bloques.append("\n".join(temp_bloque))
                temp_bloque = [linea]
            elif linea.strip():
                temp_bloque.append(linea)
        if temp_bloque:
            bloques.append("\n".join(temp_bloque))
        
        for bloque in bloques:
            # Filtro agresivo de interfaces virtuales y no deseadas
            # Incluimos VirtualBox, Host-Only, VMware, Docker, WSL, etc.
            if re.search(r'(docker|vmware|virtual|vbox|wsl|vethernet|loopback|pseudo|teredo|isatap|host-only|npcap)', bloque, re.IGNORECASE):
                continue
            
            # Buscamos la línea de la IP
            match = re.search(r'IPv4.*:\s*(\d+\.\d+\.\d+\.)(\d+)', bloque)
            if match:
                red_base = f"{match.group(1)}0/24"
                
                # Descartamos localhost y APIPA (169.254.x.x)
                if not red_base.startswith('127.') and not red_base.startswith('169.254.'):
                    if red_base not in redes:
                        redes.append(red_base)
    else:
        ip_result = subprocess.run("ip route | grep kernel | grep -vE 'docker|br-' | awk '{print $1}'", shell=True, capture_output=True, text=True)
        
        redes = [red for red in ip_result.stdout.strip().split("\n") if red]

    return {"bin_path": bin_path, "os_folder": os_folder, "redes": redes, "os_type": os_name}