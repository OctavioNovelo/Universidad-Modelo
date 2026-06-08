# frontend/CLI.py
import platform
import subprocess
import frontend.option
import core.executor as ejec
import tools
import utils.parser as parser
from pathlib import Path

def obtener_os():
    """Returns the current operating system name."""
    return platform.system()

def limpiar_pantalla():
    """Clears the terminal screen based on the operating system."""
    if obtener_os() == "Windows":
        subprocess.run(['cls'], shell=True)
    else:
        subprocess.run(['clear'])

def cli():
    """Main CLI entry point."""
    os_name = obtener_os()
    while True:
        limpiar_pantalla()
        print("¿Qué desea hacer? \n")
        print("1) Escaneo de Red")
        print("2) Revisión de seguridad")
        print("3) Resultados")
        print("4) Salir \n")

        opcion = leer_opcion("Seleccione una opción: ", 1, 4)
        
        if opcion == 4:
            print("¡Hasta luego!")
            exit()

        contexto = frontend.option.opciones(opcion, os_name)
        if not contexto:
            continue

        match contexto["tool"]:
            case "Nmap":
                nmap_cli(contexto)
            case "JTR":
                print("\nFunción JTR no implementada aún.\n")
                input("Presiona Enter para continuar...")
            case "Resultados":
                resultados(contexto)

def leer_opcion(mensaje, min_val, max_val):
    """Helper to read and validate user input within a range."""
    while True:
        try:
            opcion = int(input(mensaje))
            if min_val <= opcion <= max_val:
                return opcion
            else:
                print(f"Error: Por favor seleccione una opción entre {min_val} y {max_val}.")
        except ValueError:
            print("Error: Entrada no válida. Por favor, ingrese un número.")

def confirmar_escaneo(titulo, descripcion):
    """Shows a verification page with scan details and asks for confirmation."""
    limpiar_pantalla()
    print("\n" + "="*80)
    print(f"{titulo:^80}")
    print("="*80 + "\n")
    print(descripcion + "\n")
    print("="*80)
    print("¿Desea continuar con esta operación?")
    print("1) Sí")
    print("2) Regresar\n")
    
    confirm = leer_opcion("Seleccione una opción: ", 1, 2)
    return confirm == 1

def nmap_cli(contexto):
    """Nmap-specific menu and logic."""
    while True:
        limpiar_pantalla()
        print("\n--- Opciones ---\n")
        print("1) Internet Lento")
        print("2) Internet Fallando")
        print("3) Deteccion de dispositivos ocultos")
        print("4) Auditoria de Access Points")
        print("5) Identificacion de Dipositivos")
        print("6) Monitor de consumo")
        print("7) Full Pack")
        print("8) Personalización")
        print("9) Regresar\n")

        opcion = leer_opcion("Seleccione una opción: ", 1, 9)

        match opcion:
            case 1:
                desc = ("- OBJETIVO: Identificar qué dispositivos están activos y qué servicios básicos consumen.\n"
                        "- TÉCNICA: Escaneo SYN sobre los 100 puertos más comunes.\n"
                        "- NOTA: Ideal para una vista rápida de la red sin generar mucho tráfico.")
                if confirmar_escaneo("INTERNET LENTO", desc):
                    limpiar_pantalla()
                    context = ejec.ejecutar_herramienta(contexto["tool"], contexto["os_folder"])
                    tools.nmap.internet_lento(context)
            case 2:
                desc = ("- OBJETIVO: Detectar si hay fallos de seguridad o servicios mal configurados.\n"
                        "- TÉCNICA: Detección de versiones y ejecución del motor de scripts.\n"
                        "- NOTA: Puede tardar varios minutos dependiendo del tamaño de la red.")
                if confirmar_escaneo("INTERNET FALLANDO", desc):
                    limpiar_pantalla()
                    print("\n Esto tardara un algo de tiempo, espera porfavor\n")
                    context = ejec.ejecutar_herramienta(contexto["tool"], contexto["os_folder"])
                    tools.nmap.vulnerabilidades(context)
            case 3:
                desc = ("- OBJETIVO: Detectar dispositivos 'invisibles' que no responden a Pings.\n"
                        "- TÉCNICA: Escaneo SYN fragmentado, longitud de datos extra y omisión de Ping.\n"
                        "- NOTA: Diseñado para saltar reglas básicas de firewalls que ocultan dispositivos. Evita IDS y Firewalls")
                if confirmar_escaneo("GHOST HUNTER (DISPOSITIVOS OCULTOS)", desc):
                    limpiar_pantalla()
                    print("\n Buscando dispositivos ocultos... Esto requiere sigilo.\n")
                    context = ejec.ejecutar_herramienta(contexto["tool"], contexto["os_folder"])
                    tools.nmap.dispositivos_ocultos(context)
            case 4:
                desc = ("- OBJETIVO: Encontrar interfaces de administración expuestas (Routers, Cámaras, NAS).\n"
                        "- TÉCNICA: Escaneo específico de puertos 21, 22, 23, 80, 443, 8080 y 8443 con -sV.\n"
                        "- NOTA: Crucial para prevenir accesos no autorizados por credenciales por defecto.")
                if confirmar_escaneo("AUDITORÍA DE ACCESS POINTS", desc):
                    limpiar_pantalla()
                    context = ejec.ejecutar_herramienta(contexto["tool"], contexto["os_folder"])
                    tools.nmap.admin_audit(context)
            case 5:
                desc = ("- OBJETIVO: Saber exactamente qué marca y modelo es cada dirección IP detectada.\n"
                        "- TÉCNICA: Escaneo Agresivo (-A) que incluye OS detection, Script scanning y Traceroute.\n"
                        "- NOTA: Proporciona nombres claros como 'iPhone 13', 'Samsung SmartTV' o 'Tesla MCU'.")
                if confirmar_escaneo("GHOST ID (IDENTIFICACIÓN DE DISPOSITIVOS)", desc):
                    limpiar_pantalla()
                    print("\n Intentando identificar marcas y modelos de dispositivos...\n")
                    context = ejec.ejecutar_herramienta(contexto["tool"], contexto["os_folder"])
                    tools.nmap.indentificar_dispositivos(context)
            case 6:
                desc = ("- OBJETIVO: Identificar dispositivos que saturan el ancho de banda con video o juegos.\n"
                        "- TÉCNICA: Escaneo de puertos UDP/TCP asociados a Steam, Netflix, Spotify y PSN/Xbox Live.\n"
                        "- NOTA: Útil para diagnosticar 'Lag' en juegos o problemas de buffer en streaming.")
                if confirmar_escaneo("MONITOR DE CONSUMO", desc):
                    limpiar_pantalla()
                    context = ejec.ejecutar_herramienta(contexto["tool"], contexto["os_folder"])
                    tools.nmap.monitor_consumo(context)
            case 7:
                desc = ("- OBJETIVO: Realizar un análisis completo.\n"
                        "- TÉCNICA: Ejecución secuencial de los módulos 1 y 2.")
                if confirmar_escaneo("FULL PACK", desc):
                    limpiar_pantalla()
                    context = ejec.ejecutar_herramienta(contexto["tool"], contexto["os_folder"])
                    tools.nmap.full_pack(context)
            case 8:
                desc = ("- OBJETIVO: Control total sobre las banderas de Nmap para casos específicos.\n"
                        "- TÉCNICA: Selección manual de protocolos (TCP/UDP/SCTP), banderas SYN/Connect/FIN y timing (T1-T5).\n"
                        "- NOTA: Recomendado solo para usuarios avanzados con conocimientos de redes.")
                if confirmar_escaneo("PERSONALIZACIÓN", desc):
                    limpiar_pantalla()
                    context = ejec.ejecutar_herramienta(contexto["tool"], contexto["os_folder"])
                    tools.nmap.personalizado(context)
            case 9:
                return

def mostrar_resultados_formateados(resultados):
    """Displays formatted scan results. Outputs need to be customized for each tool."""
    if not resultados:
        print("No se encontraron coincidencias.")
        return
    if isinstance(resultados[0], dict) and "Error" in resultados[0]:
        print(resultados[0]["Error"])
        return

    print(f"\n{'IP':<16} | {'PUERTO':<8} | {'SERVICIO':<15} | {'ESTADO':<10}")
    print("-" * 70)
    for res in resultados:
        if isinstance(res, dict):
            print(f"{res['IP']:<16} | {res['Puerto']:<8} | {res['Servicio']:<15} | {res['Estado']:<10}")
            if res.get('Vulnerabilidades'):
                for v in res['Vulnerabilidades']:
                    print(f"   └── [!] {v}")
        else:
            print(res)

def resultados(context):
    """Results management menu."""
    while True:
        limpiar_pantalla()
        base_path = Path(__file__).parent.parent
        
        print("\n Resultados \n")
        print("1) Ver todos los resultados")
        print("2) Actualizar resultados (Comparamos con el escaneo anterior)")
        print("3) Regresar \n")
        
        opcion = leer_opcion("Elige una opción: ", 1, 3)
        
        if opcion == 3: return

        limpiar_pantalla()
        print("\n Selecciona la categoría: \n")
        print("1) Internet Lento")
        print("2) Internet Fallando")
        print("3) Ghost Hunter")
        print("4) Auditoría de Administracion")
        print("5) Ghost ID")
        print("6) Monitor de consumo")
        print("7) Full Pack")
        print("8) Personalizado\n")
        cat = leer_opcion("Categoría: ", 1, 8)
        
        # Mapping categories to filenames
        nombres_archivos = {
            1: "internet_lento", 2: "vulnerabilidades", 3: "dispositivos_ocultos",
            4: "admin_audit", 5: "ind_disp", 6: "consumo",
            7: "full_pack", 8: "personalizado"
        }
        
        file_name = nombres_archivos[cat]
        result_path = base_path / "utils" / "Resultados" / context["os_folder"] / "Nmap" / file_name

        if opcion == 1:
            while True:
                limpiar_pantalla()
                print(f"\n--- Visualizando: {file_name} ---")
                print("1) Información específica")
                print("2) Tabla de resumen")
                print("3) Regresar \n")
                
                sub_opt = leer_opcion("Opción: ", 1, 3)
                if sub_opt == 3: break
                
                if sub_opt == 1:
                    limpiar_pantalla()
                    info = input("\n ¿Qué buscas? (Ej: 'open', '80', 'ip'): ")
                    res = parser.buscar_en_gnmap(f"{result_path}_grepable.txt", info)
                    print("\n --- Coincidencias ---")
                    for line in res: print(line)
                    input("\n Enter para continuar...")
                else:
                    limpiar_pantalla()
                    datos = parser.generar_tabla_xml(f"{result_path}.xml")
                    mostrar_resultados_formateados(datos)
                    input("\n Enter para continuar...")
        
        elif opcion == 2:
            limpiar_pantalla()
            print("\n Buscando cambios significativos en la red...")
            # In a real version, we would copy the current XML to a .old one after each scan.
            # For now, we compare with a supposed .old file if it exists.
            old_path = result_path.with_suffix('.xml.old')
            if not old_path.exists():
                print(f"\n[!] No hay un escaneo anterior para comparar en {file_name}.")
                print("Para habilitar esto, renombra el archivo .xml actual a .xml.old manualmente.")
            else:
                cambios = parser.comparar_escaneos(f"{result_path}.xml", str(old_path))
                print("\n --- NUEVOS DISPOSITIVOS / PUERTOS DETECTADOS ---")
                mostrar_resultados_formateados(cambios)
            input("\n Enter para continuar...")
