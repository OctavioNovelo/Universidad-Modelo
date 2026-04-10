# frontend/CLI.py
import platform
import subprocess
import frontend.option
import core.executor as ejec
import tools
import utils.parser as parser
from pathlib import Path

def obtener_os():
    return platform.system()

def limpiar_pantalla():
    if obtener_os() == "Windows":
        subprocess.run(['cls'], shell=True)
    else:
        subprocess.run(['clear'])

def cli():
    os_name = obtener_os()  # el OS se obtiene aquí, cuando se necesita
    print("¿Qué desea hacer? \n")
    print("1) Escaneo de Red") # El escaneo de red nos permitira ver quien y que estan haciendo en la red
    print("2) Revisión de seguridad") # Esto servira para poner a prueba la seguridad de nuestra propia infrestructura
    print("3) Resultados")
    print("4) Luego veo \n")

    opcion = int(input())
    contexto = frontend.option.opciones(opcion, os_name)

    match contexto["tool"]:
        case "Nmap":
            nmap_cli(contexto)
        case "JTR":
            pass
        case "Resultados":
            resultados(contexto)



def nmap_cli(contexto):
    limpiar_pantalla()
    print("\n¿Qué problema quieres resolver?\n")
    print("1) Internet Lento") # Si no se reconoce un dipositivo o servicio podria eliminarlo. 
    print("2) Internet Fallando") # Si tiene alguna vulnerabilidad actual deberia formatear y actualizar el dispositivo o servicio.
    print("3) Full Pack") # Saber todo de una vez, quitas lo que no y actualizas lo que si 
    print("4) Detalles")
    print("5) Personalización") # Aqui el usuario personalizara la busqueda de nmap
    print("6) Regresar\n")

    opcion = int(input())

    match opcion:
        case 1:
            limpiar_pantalla()
            context = ejec.ejecutar_herramienta(contexto["tool"], contexto["os_folder"])
            tools.nmap.internet_lento(context)
        case 2:
            limpiar_pantalla()
            print("\n Esto tardara un algo de tiempo, espera porfavor\n")
            context = ejec.ejecutar_herramienta(contexto["tool"], contexto["os_folder"])
            tools.nmap.internet_fallando(context)
        case 3:
            limpiar_pantalla()
            print("\n Esto puede tomar bastante tiempo, quieres continuar ? \n")
            print("1) Si")
            print("2) No \n")
            confirm = int(input())
            if confirm != 1:
                limpiar_pantalla()
                nmap_cli(contexto)
            else:
                limpiar_pantalla()
                context = ejec.ejecutar_herramienta(contexto["tool"], contexto["os_folder"])
                tools.nmap.full_pack(context)
        case 4:
            nmap_detalles(contexto)
        case 5:
            limpiar_pantalla()
            context = ejec.ejecutar_herramienta(contexto["tool"], contexto["os_folder"])
            tools.nmap.personalizado(context)
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


def resultados(context):
        limpiar_pantalla()
        base_path = Path(__file__).parent.parent
        
        print("\n Resultados \n")
        print("1) Internet lento")
        print("2) Internet fallando")
        print("3) Full Pack")
        print("4) Personalizado")
        print("5) Regresar \n")
        
        opcion = int(input("Elige una opción: "))
        
        match opcion:
            case 1:
                while True:
                    limpiar_pantalla()
                    print("\n 1) Informacion especifica")
                    print(" 2) Tabla de resumen")
                    print(" 3) Regresar \n")

                    option = int(input("Elige una opción: "))

                    match option:
                        case 1:
                            limpiar_pantalla()
                            result_path = base_path / "utils" / "Resultados" / context["os_folder"] / "Nmap" / "internet_lento_grepable"

                            info = input("\n ¿Qué buscas? (ej: 'open', '80', '192.168'): ")
                            resultados = parser.buscar_en_gnmap(f"{result_path}.txt", info)

                            print("\n --- Resultados Encontrados ---")
                            for res in resultados:
                                print(res)
                            input("\n Presiona Enter para continuar...")
                        case 2: 
                            limpiar_pantalla()
                            result_path = base_path / "utils" / "Resultados" / context["os_folder"] / "Nmap" / "internet_lento"
                            datos = parser.generar_tabla_xml(f"{result_path}.xml")
                            print("\n --- Tabla Resumen de Escaneo ---")
                            if not datos:
                                print("No hay datos para mostrar.")
                            elif "Error" in datos[0]:
                                print(datos[0]["Error"])
                            else:
                                # Damos formato de tabla simple usando f-strings
                                print(f"{'IP':<16} | {'PUERTO':<8} | {'ESTADO':<10} | {'SERVICIO':<15}")
                                print("-" * 55)
                                for fila in datos:
                                    print(f"{fila['IP']:<16} | {fila['Puerto']:<8} | {fila['Estado']:<10} | {fila['Servicio']:<15}")
                            
                            input("\n Presiona Enter para continuar...")
                        case 3:
                            return
                        case _:
                            print("\n Opcion no Valida \n")
                        
            case 2: # Internet fallando / Vulnerabilidades
                while True: # Bucle para no salir al menú principal
                    limpiar_pantalla()
                    print("\n 1) Informacion especifica (Buscador)")
                    print(" 2) Tabla de resumen (con Vulnerabilidades)")
                    print(" 3) Regresar \n")

                    option = input("Elige una opción: ") # Usamos string para evitar errores si presionan letras
                    
                    if option == "3": break

                    match option:
                        case "1":
                            limpiar_pantalla()
                            result_path = base_path / "utils" / "Resultados" / context["os_folder"] / "Nmap" / "vulnerabilidades_grepable"
                            
                            # BUCLE DE BÚSQUEDA INDIVIDUAL
                            while True:
                                print("\n" + "-"*30)
                                info = input("¿Qué buscas? (ej: 'open', '445' | 'q' para volver): ").strip()
                                if info.lower() in ['q', 'salir', 'exit']: break
                                
                                resultados = parser.buscar_en_gnmap(f"{result_path}.txt", info)
                                print("\n--- Coincidencias ---")
                                for res in resultados:
                                    print(res)
                        case "2":
                            limpiar_pantalla()
                            result_path = base_path / "utils" / "Resultados" / context["os_folder"] / "Nmap" / "vulnerabilidades"
                            datos = parser.generar_tabla_xml(f"{result_path}.xml")
                            
                            print(f"\n{'IP':<16} | {'PUERTO':<8} | {'ESTADO':<10} | {'SERVICIO':<15}")
                            print("-" * 65)
                            
                            for fila in datos:
                                print(f"{fila['IP']:<16} | {fila['Puerto']:<8} | {fila['Estado']:<10} | {fila['Servicio']:<15}")
                                # Imprimir vulnerabilidades si existen
                                if fila['Vulnerabilidades']:
                                    for vuln in fila['Vulnerabilidades']:
                                        print(f"   └── [!] {vuln}")
                            
                            input("\nPresiona Enter para continuar...")
                        case 3:
                            return
                        case _:
                            print("\n Opcion no Valida \n")
            case 3:
                while True:
                    limpiar_pantalla()
                    print("\n 1) Informacion especifica")
                    print(" 2) Tabla de resumen")
                    print(" 3) Regresar \n")

                    option = int(input("Elige una opción: "))

                    match option:
                        case 1:
                            limpiar_pantalla()
                            result_path = base_path / "utils" / "Resultados" / context["os_folder"] / "Nmap" / "full_pack_grepable"

                            info = input("\n ¿Qué buscas? (ej: 'open', '80', '192.168'): ")
                            resultados = parser.buscar_en_gnmap(f"{result_path}.txt", info)

                            print("\n --- Resultados Encontrados ---")
                            for res in resultados:
                                print(res)
                            input("\n Presiona Enter para continuar...")
                        case 2: 
                            limpiar_pantalla()
                            result_path = base_path / "utils" / "Resultados" / context["os_folder"] / "Nmap" / "full_pack"
                            datos = parser.generar_tabla_xml(f"{result_path}.xml")
                            print("\n --- Tabla Resumen de Escaneo ---")
                            if not datos:
                                print("No hay datos para mostrar.")
                            elif "Error" in datos[0]:
                                print(datos[0]["Error"])
                            else:
                                # Damos formato de tabla simple usando f-strings
                                print(f"{'IP':<16} | {'PUERTO':<8} | {'ESTADO':<10} | {'SERVICIO':<15}")
                                print("-" * 55)
                                for fila in datos:
                                    print(f"{fila['IP']:<16} | {fila['Puerto']:<8} | {fila['Estado']:<10} | {fila['Servicio']:<15}")
                            
                            input("\n Presiona Enter para continuar...")
                        case 3:
                            return
                        case _:
                            print("\n Opcion no Valida \n")
            case 4:
                while True:
                    limpiar_pantalla()
                    print("\n 1) Informacion especifica")
                    print(" 2) Tabla de resumen")
                    print(" 3) Regresar \n")

                    option = int(input("Elige una opción: "))

                    match option:
                        case 1:
                            limpiar_pantalla()
                            result_path = base_path / "utils" / "Resultados" / context["os_folder"] / "Nmap" / "personalizado_grepable"

                            info = input("\n ¿Qué buscas? (ej: 'open', '80', '192.168'): ")
                            resultados = parser.buscar_en_gnmap(f"{result_path}.txt", info)

                            print("\n --- Resultados Encontrados ---")
                            for res in resultados:
                                print(res)
                            input("\n Presiona Enter para continuar...")
                        case 2: 
                            limpiar_pantalla()
                            result_path = base_path / "utils" / "Resultados" / context["os_folder"] / "Nmap" / "personalizado"
                            datos = parser.generar_tabla_xml(f"{result_path}.xml")
                            print("\n --- Tabla Resumen de Escaneo ---")
                            if not datos:
                                print("No hay datos para mostrar.")
                            elif "Error" in datos[0]:
                                print(datos[0]["Error"])
                            else:
                                # Damos formato de tabla simple usando f-strings
                                print(f"{'IP':<16} | {'PUERTO':<8} | {'ESTADO':<10} | {'SERVICIO':<15}")
                                print("-" * 55)
                                for fila in datos:
                                    print(f"{fila['IP']:<16} | {fila['Puerto']:<8} | {fila['Estado']:<10} | {fila['Servicio']:<15}")
                            
                            input("\n Presiona Enter para continuar...")
                        case 3:
                            return
                        case _:
                            print("\n Opcion no Valida \n")
            case _:
                print("Opción inválida.")