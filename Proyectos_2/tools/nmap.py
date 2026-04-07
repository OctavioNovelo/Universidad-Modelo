import subprocess
from pathlib import Path

nmap_bin = {
    'linux':   {'bin_name': 'nmap'},
    'windows': {'bin_name': 'nmap.exe'},
    'macos':   {'bin_name': 'nmap'}
}


def internet_lento(context):
    base_path   = Path(__file__).parent.parent
    hosts_file  = base_path / "utils" / "Resultados" / context["os_folder"] / "Nmap" / "hosts.txt"
    result_path = base_path / "utils" / "Resultados" / context["os_folder"] / "Nmap" / "internet_lento.txt"

    hosts_file.parent.mkdir(parents=True, exist_ok=True)

    # Guardamos las redes en el archivo para pasarlo con -iL
    with open(hosts_file, "w") as f:
        for red in context["redes"]:
            f.write(red + "\n")

    subprocess.run(["sudo", str(context["bin_path"]), "-sS",
                    "-F",
                    "-Pn",
                    "-n",
                    "-O",
                    "-T4",
                    "-iL", str(hosts_file),
                    "-oN", str(result_path)
                    ])

def internet_fallando(context):
    base_path   = Path(__file__).parent.parent
    hosts_file  = base_path / "utils" / "Resultados" / context["os_folder"] / "Nmap" / "hosts.txt"
    result_path = base_path / "utils" / "Resultados" / context["os_folder"] / "Nmap" / "vulnerabilidades.txt"

    hosts_file.parent.mkdir(parents = True, exist_ok = True)


    # Guardamos las redes en el archivo para pasarlo con -iL
    with open(hosts_file, "w") as f:
        for red in context["redes"]:
            f.write(red + "\n")
    
    subprocess.run(["sudo", str(context["bin_path"]), "-sV",
                    "--script", "vuln",
                    "-Pn",
                    "-n",
                    "-T3",
                    "-O",
                    "-iL", str(hosts_file),
                    "-oN", str(result_path)
                    ])

# Personalizacion
# Esto estara caom ya que sera un CLI con todas las opciones de personalizacion que Nmap ofrece
# Tipo de escaneo 
# Tecnicas de escaneo
# Especificacion y/o Limitacion de puertos
# Obtencion de info (OS, Version, etc)
# Vulnerabilidades
