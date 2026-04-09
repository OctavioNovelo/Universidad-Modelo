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

def internet_lento(context):
    base_path = Path(__file__).parent.parent
    hosts_file = base_path / "utils" / "Resultados" / context["os_folder"] / "Nmap" / "hosts.txt"
    result_path = base_path / "utils" / "Resultados" / context["os_folder"] / "Nmap" / "internet_lento"

    hosts_file.parent.mkdir(parents=True, exist_ok=True)

    with open(hosts_file, "w") as f:
        for red in context["redes"]:
            f.write(red + "\n")


    args = [str(context["bin_path"]), "-sS",
            "-F", "-Pn", "-n", "-O", "-T4", 
            "-iL", str(hosts_file),
            "-oN", f"{result_path}_normal.txt",
            "-oG", f"{result_path}_grepable.txt",
            "-oX", f"{result_path}.xml"]

    subprocess.run(ejecutar_comando(args))

def internet_fallando(context):
    base_path = Path(__file__).parent.parent
    hosts_file = base_path / "utils" / "Resultados" / context["os_folder"] / "Nmap" / "hosts.txt"
    result_path = base_path / "utils" / "Resultados" / context["os_folder"] / "Nmap" / "vulnerabilidades"

    hosts_file.parent.mkdir(parents=True, exist_ok=True)

    with open(hosts_file, "w") as f:
        for red in context["redes"]:
            f.write(red + "\n")
    
    args = [str(context["bin_path"]), "-sV",
            "--script", "vuln",
            "-Pn", "-n", "-T3", "-O",
            "-iL", str(hosts_file),
            "-oN", f"{result_path}_normal.txt",
            "-oG", f"{result_path}_grepable.txt",
            "-oX", f"{result_path}.xml"]
    
    subprocess.run(ejecutar_comando(args))

def full_pack(context):
    base_path = Path(__file__).parent.parent
    hosts_file = base_path / "utils" / "Resultados" / context["os_folder"] / "Nmap" / "hosts.txt"
    result_path = base_path / "utils" / "Resultados" / context["os_folder"] / "Nmap" / "full_pack"

    hosts_file.parent.mkdir(parents=True, exist_ok=True)

    with open(hosts_file, "w") as f:
        for red in context["redes"]:
            f.write(red + "\n")

    args = [str(context["bin_path"]), "-sS",
            "-F", "-Pn", "-n", "-O", "-T4", 
            "-iL", str(hosts_file),
            "-oN", f"{result_path}_normal.txt",
            "-oG", f"{result_path}_grepable.txt",
            "-oX", f"{result_path}.xml"]

    subprocess.run(ejecutar_comando(args))

    args = [str(context["bin_path"]), "-sV",
            "--script", "vuln",
            "-Pn", "-n", "-T3", "-O",
            "-iL", str(hosts_file),
            "-oN", f"{result_path}_normal.txt",
            "-oG", f"{result_path}_grepable.txt",
            "-oX", f"{result_path}.xml"]
    
    subprocess.run(ejecutar_comando(args))
    
# Personalizacion
# Tecnicas de escaneo

# Para mantener la arquitectura del backend la opcion de personalizacion no tiene vuelta atras, sin embargo en la version final obviamente tendra
import subprocess
from pathlib import Path
import frontend.CLI # Asumo que lo importas arriba por la llamada a limpiar_pantalla

def personalizado(context):
    base_path = Path(__file__).parent.parent
    hosts_file = base_path / "utils" / "Resultados" / context["os_folder"] / "Nmap" / "hosts.txt"
    result_path = base_path / "utils" / "Resultados" / context["os_folder"] / "Nmap" / "personalizado"

    hosts_file.parent.mkdir(parents=True, exist_ok=True)

    with open(hosts_file, "w") as f:
        for red in context["redes"]:
            f.write(red + "\n")

    print("\n Escaneo Personalizado \n")
    print("\n Tipo de escaneo \n")
    print("1) TCP  2) UDP  3) SCTP  4) Full  5) Regresar \n")
    
    opcion = int(input())
    
    # Inicializamos la lista de argumentos base
    args = [str(context["bin_path"])]

    match opcion:
        case 1:
            print("1) TCP Predeterminado  2) TCP/SYN  3) TCP/FIN  4) TCP Null  5) TCP Xmas  6) TCP Maimon\n")
            type = int(input())
            match type:
                case 1: 
                    args.append("-sT")
                case 2: 
                    args.append("-sS")
                case 3: 
                    args.append("-sF")
                case 4: 
                    args.append("-sN")
                case 5: 
                    args.append("-sX")
                case 6: 
                    args.append("-sM")
                case _: 
                    print("\n Opcion no valida \n")
        case 2:
            args.append("-sU")
        case 3:
            print("1) SCTP/init  2) SCTP Cookie Plus")
            type = int(input())
            match type:
                case 1: 
                    args.append("-sY")
                case 2: 
                    args.append("-sZ")
                case _: 
                    print("\n Opcion no valida \n")
        case 4:
            print("\n Bro, que demonios te pasa, como que todo, si quiera es posible ? Dame chance no soy dios, todavia... \n")
            print("Tu funcion se esta construyendo... \n")
            return
        case _:
            print("\n Opcion no valida \n")
            return

    frontend.CLI.limpiar_pantalla()
    print("\n Puertos \n")
    print("1) Especificar puerto(s)  2) Puertos mas comunes  3) Puertos mas probables  4) Excluir Puertos\n")
    opcion = int(input())

    match opcion:
        case 1:
            print("\n Que puertos quieres escanear: \n")
            print("',' especificos; '-' rango. El maximo es 65.536. No uses espacios porfavor\n")

            ports = str(input())

            # extend agrega ambos elementos intactos a la lista principal
            args.extend(["-p", ports]) 
        case 2:
            print("\n Cuantos puertos de los mas comunes quieres escanear: \n")
            print("Ej: 10 = Escanear los 10 puertos mas comunes \n")

            ports = int(input())

            args.extend(["--top-ports", str(ports)])
        case 3:
            print("\n Que porcentaje quieres usar: \n")
            print("Ej: 33 = Los puertos que tengan una probabilidad del 33% o mas son los que se escanearan \n")

            ports = int(input())

            args.extend(["--port-ratio", str(ports/100)])
        case 4:
            print("\n Que puertos quieres excluir: \n")
            print("',' especificos; '-' rango. El maximo es 65.536 \n")

            ports = str(input())
            args.extend(["--exclude-ports", ports])
        case _:
            print("\n Opcion no valida \n")

    # Agregamos la informacion especifica que nunca sobra
    args.extend(["-O", "-sV"])

    frontend.CLI.limpiar_pantalla()
    print("\n Deseas escanear las vulnerabilidades ? \n")
    print("1) Si  2) No \n")

    opcion = int(input())

    match opcion:
        case 1:
            args.extend(["--script", "vuln"])


    args.extend(["-iL", str(hosts_file), "-oN", f"{result_path}_normal.txt", "-oG", f"{result_path}_grepable.txt", "-oX", f"{result_path}.xml"])
    subprocess.run(ejecutar_comando(args))