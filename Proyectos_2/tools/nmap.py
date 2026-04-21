import subprocess
from pathlib import Path
import frontend.CLI

nmap_bin = {
    'linux':   {'bin_name': 'nmap'},
    'windows': {'bin_name': 'nmap.exe'},
    'macos':   {'bin_name': 'nmap'}
}

def ejecutar_comando(args):
    if frontend.CLI.obtener_os() != "Windows":
        return ["sudo"] + args
    return args

def internet_lento(context, timing_level=4):
    base_path = Path(__file__).parent.parent
    hosts_file = base_path / "utils" / "Resultados" / context["os_folder"] / "Nmap" / "hosts.txt"
    result_path = base_path / "utils" / "Resultados" / context["os_folder"] / "Nmap" / "internet_lento"

    hosts_file.parent.mkdir(parents=True, exist_ok=True)
    with open(hosts_file, "w") as f:
        for red in context["redes"]: f.write(red + "\n")

    args = [str(context["bin_path"]), "-sS", "-F", "-Pn", "-n", "-O", f"-T{timing_level}", 
            "-iL", str(hosts_file),
            "-oN", f"{result_path}_normal.txt",
            "-oG", f"{result_path}_grepable.txt",
            "-oX", f"{result_path}.xml"]
    subprocess.run(ejecutar_comando(args))

def internet_fallando(context, timing_level=3):
    base_path = Path(__file__).parent.parent
    hosts_file = base_path / "utils" / "Resultados" / context["os_folder"] / "Nmap" / "hosts.txt"
    result_path = base_path / "utils" / "Resultados" / context["os_folder"] / "Nmap" / "vulnerabilidades"

    hosts_file.parent.mkdir(parents=True, exist_ok=True)
    with open(hosts_file, "w") as f:
        for red in context["redes"]: f.write(red + "\n")
    
    args = [str(context["bin_path"]), "-sV", "--script", "vuln", "-Pn", "-n", f"-T{timing_level}", "-O",
            "-iL", str(hosts_file),
            "-oN", f"{result_path}_normal.txt",
            "-oG", f"{result_path}_grepable.txt",
            "-oX", f"{result_path}.xml"]
    subprocess.run(ejecutar_comando(args))

def full_pack(context):
    internet_lento(context)
    internet_fallando(context)

def ghost_hunter(context, timing_level=2):
    """Detecta intrusos ocultos usando escaneos fragmentados y sin ping."""
    base_path = Path(__file__).parent.parent
    result_path = base_path / "utils" / "Resultados" / context["os_folder"] / "Nmap" / "ghost_hunter"
    hosts_file = base_path / "utils" / "Resultados" / context["os_folder"] / "Nmap" / "hosts.txt"

    args = [str(context["bin_path"]), "-sS", "-Pn", "-f", "--data-length", "24", f"-T{timing_level}", "-n",
            "-iL", str(hosts_file),
            "-oN", f"{result_path}_normal.txt",
            "-oG", f"{result_path}_grepable.txt",
            "-oX", f"{result_path}.xml"]
    
    subprocess.run(ejecutar_comando(args))

def admin_audit(context, timing_level=4):
    """Busca paneles de administración expuestos."""
    base_path = Path(__file__).parent.parent
    result_path = base_path / "utils" / "Resultados" / context["os_folder"] / "Nmap" / "admin_audit"
    hosts_file = base_path / "utils" / "Resultados" / context["os_folder"] / "Nmap" / "hosts.txt"

    # Puertos comunes de gestión: HTTP, HTTPS, Telnet, SSH, FTP, etc.
    args = [str(context["bin_path"]), "-p", "21,22,23,80,443,8080,8443", f"-T{timing_level}", "-sV",
            "-iL", str(hosts_file),
            "-oN", f"{result_path}_normal.txt",
            "-oG", f"{result_path}_grepable.txt",
            "-oX", f"{result_path}.xml"]
    
    subprocess.run(ejecutar_comando(args))

def detectar_os_agresivo(context, timing_level=4):
    """Identificación profunda de dispositivos (Ghost ID)."""
    base_path = Path(__file__).parent.parent
    result_path = base_path / "utils" / "Resultados" / context["os_folder"] / "Nmap" / "ghost_id"
    hosts_file = base_path / "utils" / "Resultados" / context["os_folder"] / "Nmap" / "hosts.txt"

    args = [str(context["bin_path"]), "-A", f"-T{timing_level}", "-Pn",
            "-iL", str(hosts_file),
            "-oN", f"{result_path}_normal.txt",
            "-oG", f"{result_path}_grepable.txt",
            "-oX", f"{result_path}.xml"]
    
    subprocess.run(ejecutar_comando(args))

def streaming_gaming_monitor(context, timing_level=4):
    """Busca protocolos de alto consumo (Streaming/Gaming)."""
    base_path = Path(__file__).parent.parent
    result_path = base_path / "utils" / "Resultados" / context["os_folder"] / "Nmap" / "streaming_gaming"
    hosts_file = base_path / "utils" / "Resultados" / context["os_folder"] / "Nmap" / "hosts.txt"

    # Puertos de Steam, Netflix, Spotify, y juegos comunes
    args = [str(context["bin_path"]), "-p", "1935,3478,3479,3480,5060,5061,80,443,27015-27030", f"-T{timing_level}", "-sV",
            "-iL", str(hosts_file),
            "-oN", f"{result_path}_normal.txt",
            "-oG", f"{result_path}_grepable.txt",
            "-oX", f"{result_path}.xml"]
    
    subprocess.run(ejecutar_comando(args))

def personalizado(context):
    base_path = Path(__file__).parent.parent
    hosts_file = base_path / "utils" / "Resultados" / context["os_folder"] / "Nmap" / "hosts.txt"
    result_path = base_path / "utils" / "Resultados" / context["os_folder"] / "Nmap" / "personalizado"

    hosts_file.parent.mkdir(parents=True, exist_ok=True)
    with open(hosts_file, "w") as f:
        for red in context["redes"]: f.write(red + "\n")

    print("\n Escaneo Personalizado \n")
    print("1) TCP  2) UDP  3) SCTP  4) Regresar \n")
    opcion = frontend.CLI.leer_opcion("Seleccione: ", 1, 4)
    if opcion == 4: return
    
    args = [str(context["bin_path"])]
    # Timing
    print("\n Nivel de Intensidad (1: Sigiloso - 5: Agresivo, 4 recomendado) \n")
    t_level = frontend.CLI.leer_opcion("Timing (1-5): ", 1, 5)
    args.append(f"-T{t_level}")

    if opcion == 1:
        print("1) SYN  2) Connect  3) FIN  4) NULL  5) Xmas\n")
        t_opt = frontend.CLI.leer_opcion("Tipo: ", 1, 5)
        args.append(["-sS", "-sT", "-sF", "-sN", "-sX"][t_opt-1])
    elif opcion == 2: args.append("-sU")
    elif opcion == 3: args.append("-sY")

    frontend.CLI.limpiar_pantalla()
    print("\n Puertos \n")
    print("1) Especificar  2) Top Ports  3) Port Ratio  4) Todos\n")
    p_opt = frontend.CLI.leer_opcion("Opción: ", 1, 4)
    if p_opt == 1: args.extend(["-p", input("Puertos (ej: 80,443): ")])
    elif p_opt == 2: args.extend(["--top-ports", str(frontend.CLI.leer_opcion("Cantidad: ", 1, 10000))])
    elif p_opt == 3: args.extend(["--port-ratio", str(frontend.CLI.leer_opcion("Ratio (0-1): ", 0, 1))])
    elif p_opt == 4: args.append("-p-")

    args.extend(["-iL", str(hosts_file), "-oN", f"{result_path}_normal.txt", "-oG", f"{result_path}_grepable.txt", "-oX", f"{result_path}.xml"])
    subprocess.run(ejecutar_comando(args))
