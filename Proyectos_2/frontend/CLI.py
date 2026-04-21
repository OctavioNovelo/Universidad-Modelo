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
    while True:
        try:
            opcion = int(input(mensaje))
            if min_val <= opcion <= max_val:
                return opcion
            else:
                print(f"Error: Por favor seleccione una opción entre {min_val} y {max_val}.")
        except ValueError:
            print("Error: Entrada no válida. Por favor, ingrese un número.")

def nmap_cli(contexto):
    while True:
        limpiar_pantalla()
        print("\n--- Opciones ---\n")
        print("1) Internet Lento")
        print("2) Internet Fallando")
        print("3) Full Pack")
        print("4) Shadow Hunter (Detectar Intrusos Ocultos)")
        print("5) Auditoría de Administracion (Paneles de Control Expuestos)")
        print("6) Ghost ID (Identificación de Dispositivos)")
        print("7) Monitor de consumo (Deteccion de consumo)")
        print("8) Personalización")
        print("9) Detalles")
        print("10) Regresar\n")

        opcion = leer_opcion("Seleccione una opción: ", 1, 10)

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
                print("\n Esto puede tomar bastante tiempo, ¿quieres continuar? \n")
                print("1) Si")
                print("2) No \n")
                confirm = leer_opcion("Seleccione una opción: ", 1, 2)
                if confirm == 1:
                    limpiar_pantalla()
                    context = ejec.ejecutar_herramienta(contexto["tool"], contexto["os_folder"])
                    tools.nmap.full_pack(context)
            case 4:
                limpiar_pantalla()
                print("\n Buscando dispositivos ocultos... Esto requiere sigilo.\n")
                context = ejec.ejecutar_herramienta(contexto["tool"], contexto["os_folder"])
                tools.nmap.ghost_hunter(context)
            case 5:
                limpiar_pantalla()
                context = ejec.ejecutar_herramienta(contexto["tool"], contexto["os_folder"])
                tools.nmap.admin_audit(context)
            case 6:
                limpiar_pantalla()
                print("\n Intentando identificar marcas y modelos de dispositivos...\n")
                context = ejec.ejecutar_herramienta(contexto["tool"], contexto["os_folder"])
                tools.nmap.detectar_os_agresivo(context)
            case 7:
                limpiar_pantalla()
                context = ejec.ejecutar_herramienta(contexto["tool"], contexto["os_folder"])
                tools.nmap.streaming_gaming_monitor(context)
            case 8:
                limpiar_pantalla()
                context = ejec.ejecutar_herramienta(contexto["tool"], contexto["os_folder"])
                tools.nmap.personalizado(context)
            case 9:
                nmap_detalles(contexto)
            case 10:
                return

def nmap_detalles (contexto):
    limpiar_pantalla()
    print("\n" + "="*80)
    print(f"{'DETALLES TÉCNICOS Y FUNCIONALES DE HERA (Nmap Module)':^80}")
    print("="*80 + "\n")

    print("1) Internet Lento (Escaneo de Host & Puertos Rápidos)")
    print("   - OBJETIVO: Identificar qué dispositivos están activos y qué servicios básicos consumen.")
    print("   - TÉCNICA: Escaneo SYN (-sS) sobre los 100 puertos más comunes (-F).")
    print("   - NOTA: Ideal para una vista rápida de la red sin generar mucho tráfico.\n")

    print("2) Internet Fallando (Auditoría de Vulnerabilidades)")
    print("   - OBJETIVO: Detectar si hay fallos de seguridad o servicios mal configurados.")
    print("   - TÉCNICA: Detección de versiones (-sV) y ejecución del motor de scripts 'vuln'.")
    print("   - NOTA: Puede tardar varios minutos dependiendo del tamaño de la red.\n")

    print("3) Full Pack (Diagnóstico Integral)")
    print("   - OBJETIVO: Realizar un análisis completo (Lento + Fallando) de una sola vez.")
    print("   - TÉCNICA: Ejecución secuencial de los módulos 1 y 2.\n")

    print("4) Cacería de Sombras (Ghost Hunter - Evasión de IDS/Firewalls)")
    print("   - OBJETIVO: Detectar dispositivos 'invisibles' (intrusos) que no responden a Pings.")
    print("   - TÉCNICA: Escaneo SYN fragmentado (-f), longitud de datos extra y omisión de Ping (-Pn).")
    print("   - NOTA: Diseñado para saltar reglas básicas de firewalls que ocultan dispositivos.\n")

    print("5) Auditoría Admin (Localizador de Paneles de Gestión)")
    print("   - OBJETIVO: Encontrar interfaces de administración expuestas (Routers, Cámaras, NAS).")
    print("   - TÉCNICA: Escaneo específico de puertos 21, 22, 23, 80, 443, 8080 y 8443 con -sV.")
    print("   - NOTA: Crucial para prevenir accesos no autorizados por credenciales por defecto.\n")

    print("6) Ghost ID (Identificación de Dispositivos - Fingerprinting)")
    print("   - OBJETIVO: Saber exactamente qué marca y modelo es cada dirección IP detectada.")
    print("   - TÉCNICA: Escaneo Agresivo (-A) que incluye OS detection, Script scanning y Traceroute.")
    print("   - NOTA: Proporciona nombres claros como 'iPhone 13', 'Samsung SmartTV' o 'Tesla MCU'.\n")

    print("7) Monitor de Streaming/Gaming (Análisis de Tráfico Pesado)")
    print("   - OBJETIVO: Identificar dispositivos que saturan el ancho de banda con video o juegos.")
    print("   - TÉCNICA: Escaneo de puertos UDP/TCP asociados a Steam, Netflix, Spotify y PSN/Xbox Live.")
    print("   - NOTA: Útil para diagnosticar 'Lag' en juegos o problemas de buffer en streaming.\n")

    print("8) Personalización (Modo Experto)")
    print("   - OBJETIVO: Control total sobre las banderas de Nmap para casos específicos.")
    print("   - TÉCNICA: Selección manual de protocolos (TCP/UDP/SCTP), banderas SYN/Connect/FIN y timing (T1-T5).")
    print("   - NOTA: Recomendado solo para usuarios avanzados con conocimientos de redes.\n")

    print("="*80)
    leer_opcion("Presione 1 para regresar al menú anterior: ", 1, 1)
    return

def mostrar_resultados_formateados(resultados):
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
        print("3) Full Pack")
        print("4) Shadow Hunter")
        print("5) Auditoría de Administracion")
        print("6) Ghost ID")
        print("7) Monitor de consumo")
        print("8) Personalizado\n")
        cat = leer_opcion("Categoría: ", 1, 8)
        
        nombres_archivos = {
            1: "internet_lento", 2: "vulnerabilidades", 3: "full_pack",
            4: "ghost_hunter", 5: "admin_audit", 6: "ghost_id",
            7: "streaming_gaming", 8: "personalizado"
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
            # En una versión real, copiaríamos el XML actual a uno .old después de cada escaneo.
            # Por ahora, compararemos con un supuesto archivo .old si existe.
            old_path = result_path.with_suffix('.xml.old')
            if not old_path.exists():
                print(f"\n[!] No hay un escaneo anterior para comparar en {file_name}.")
                print("Para habilitar esto, renombra el archivo .xml actual a .xml.old manualmente.")
            else:
                cambios = parser.comparar_escaneos(f"{result_path}.xml", str(old_path))
                print("\n --- NUEVOS DISPOSITIVOS / PUERTOS DETECTADOS ---")
                mostrar_resultados_formateados(cambios)
            input("\n Enter para continuar...")
