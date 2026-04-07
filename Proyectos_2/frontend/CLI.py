# frontend/CLI.py
import platform
import subprocess
import frontend.option
import core.executor as ejec
import tools


def obtener_os():
    return platform.system()

def limpiar_pantalla():
    if obtener_os() == "Windows":
        subprocess.run(['cls'], shell=True)
    else:
        subprocess.run(['clear'])

def cli():
    os_name = obtener_os()  # el OS se obtiene aquí, cuando se necesita
    print("¿Qué desea hacer?\n")
    print("1) Escaneo de Red\n") # El escaneo de red nos permitira ver quien y que estan haciendo en la red
    print("2) Revisión de seguridad\n") # Esto servira para poner a prueba la seguridad de nuestra propia infrestructura
    print("3) Luego veo\n")

    opcion = int(input())
    contexto = frontend.option.opciones(opcion, os_name)

    match contexto["tool"]:
        case "Nmap":
            nmap_cli(contexto)



def nmap_cli(contexto):
    limpiar_pantalla()
    print("\n¿Qué problema quieres resolver?\n")
    print("1) Internet Lento\n") # Si no se reconoce un dipositivo o servicio podria eliminarlo. 
    print("2) Internet Fallando\n") # Si tiene alguna vulnerabilidad actual deberia formatear y actualizar el dispositivo o servicio.
    print("3) Full Pack\n") # Saber todo de una vez, quitas lo que no y actualizas lo que si 
    print("4) Detalles\n")
    print("5) Personalización\n") # Aqui el usuario personalizara la busqueda de nmap
    print("6) Regresar\n")

    opcion = int(input())

    match opcion:
        case 1:
            limpiar_pantalla()
            context = ejec.ejecutar_herramienta(contexto["tool"], contexto["os_folder"])
            tools.nmap.internet_lento(context)
        case 2:
            limpiar_pantalla()
            context = ejec.ejecutar_herramienta(contexto["tool"], contexto["os_folder"])
            tools.nmap.internet_fallando(context)
        case 3:
            ejec.ejecutar_herramienta(contexto["tool"], "full_pack", contexto["os_folder"])
        case 4:
            nmap_detalles(contexto)
        case 5:
            pass
        case 6:
            limpiar_pantalla()
            cli()

def nmap_detalles (contexto):
    limpiar_pantalla()
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
            limpiar_pantalla()
            nmap_cli(contexto)
        case _:
            limpiar_pantalla()
            nmap_cli(contexto)