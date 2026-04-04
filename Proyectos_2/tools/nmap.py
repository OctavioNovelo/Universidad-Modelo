import subprocess
from pathlib import Path
import frontend.option
# Las opciones de modificacion de nmap
# Aqui correremos comandos y se modificaran los parametros

nmap_command = ""



def internetLento ():
    subprocess.run(["clear"])

    base_path = Path(__file__).parent.parent
    bin_path = base_path / "tools" / "tools_bin" / frontend.option.os / "Nmap" / "nmap"
    result_path = base_path / "utils" / "Resultados" / frontend.option.os / "Nmap" / "prueba"

    # Hay que resolver esto, las ips que me dan no son la direccion de red.
    result = subprocess.run("ip route | grep kernel | awk '{print $1}'", shell = True, capture_output = True, text = True)
    ip = result.stdout.strip().replace("\n", " ")

    subprocess.run(["sudo", str(bin_path), "-sS", "-oN", result_path, ip])