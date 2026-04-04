#from tools.nmap import NmapCommands # Lo comandos de nmap.py
#from core.executor import ToolExecutor
from pathlib import Path
import platform
import frontend.option
import subprocess
import tools.nmap

# Inicializamos interfaz
def cli ():
    print("Que desea hacer ?\n")

    print("1) Escaneo de Red\n")
    print("2) Revision de seguridad\n")
    print("3) Luego veo\n")

    opcion = int(input())
    frontend.option.opciones(opcion)

# Estaba cansado, pero la interfaz es irrelevante si es 
# windows o linux, HACER la diferencia en nmap.py donde
# windows y linux si cambia, segun yo.
def nmap_lin_cli ():
    print("\n Que problema queires resolver ? \n")
    print("1) Internet Lento \n")
    print("2) Internet Fallando \n")
    print("3) Full Pack \n")
    print("4) Detalles \n")
    print("5) Personalizacion \n")
    print("6) Regresar \n")

    opcion = int(input())

    match opcion:
        case 1:
            tools.nmap.internetLento()
        case 2:
            pass
        case 3:
            pass
        case 4:
            nmap_detalles()
        case 5:
            pass
        case 6:
            subprocess.run(["clear"])
            cli()


def nmap_detalles ():
    subprocess.run(["clear"])
    print("\n A countinuacion encontramos los detalles de cada opcion del menu principal \n")
    print("\n 1) Internet Lento \n")
    print("Si sientes que tu internet esta lento (no confundir con fallando, checa su descripcion), " \
    "puede ser por el consumo de los dispositivos conectados, identifica los dispositivos de tu red y revisa su consumo. \n")
    print("\n 2) Internet Fallando \n")
    print("El internet falla cuando el acceso a paginas o busques son imposibles por mas tiempo que uno espere, a diferencia " \
    "de cuando este lento que tarda en acceder. \n")
    print("\n 3) Full Pack \n")
    print("Si no se sabe muy bien como clasificar su error, esta realizara todas las opciones al mismo tiempo, tarda un poco mas. \n")
    print("\n 5) Personalizacion \n")
    print("Permite realizar un escaneo personalizado, recomendado para usuarios mas avanzados o si se busca informacion mas especifica. \n")
    print("\n 1) Regresar \n")

    opcion = int(input())

    match opcion:
        case 1:
            subprocess.run(["clear"])
            if (frontend.option.os == "Linux"):
                {
                    frontend.CLI.nmap_lin_cli()
                }
            elif (frontend.option.os == "Windows"):
                {
                    # frontend.CLI.nmap_win_cli()
                }
        case _:
            subprocess.run(["clear"])
            if (frontend.option.os == "Linux"):
                {
                    frontend.CLI.nmap_lin_cli()
                }
            elif (frontend.option.os == "Windows"):
                {
                    # frontend.CLI.nmap_win_cli()
                }
