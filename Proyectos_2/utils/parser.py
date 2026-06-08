# utils/parser.py
import xml.etree.ElementTree as ET
from pathlib import Path

def buscar_en_gnmap(ruta_gnmap, termino_busqueda):
    """Searches for a term within a .gnmap file."""
    resultados = []
    try:
        with open(ruta_gnmap, "r") as f:
            for linea in f:
                if not linea.startswith("#") and termino_busqueda.lower() in linea.lower():
                    resultados.append(linea.strip())
        return resultados
    except FileNotFoundError:
        return ["Error: No se encontró el archivo de resultados. Ejecuta un escaneo primero."]

def generar_tabla_xml(ruta_xml):
    """Parses an Nmap XML file and returns a list of results."""
    try:
        tree = ET.parse(ruta_xml)
        root = tree.getroot()
    except Exception as e:
        return [{"Error": f"No se pudo leer el archivo: {e}"}]

    filas_tabla = []
    for host in root.findall('host'):
        address = host.find("address[@addrtype='ipv4']")
        ip = address.get('addr') if address is not None else "Desconocido"
        
        for port in host.findall('.//port'):
            estado_el = port.find('state')
            servicio_el = port.find('service')
            
            fila = {
                'IP': ip,
                'Puerto': port.get('portid'),
                'Estado': estado_el.get('state') if estado_el is not None else "N/D",
                'Servicio': servicio_el.get('name') if servicio_el is not None else "N/D",
                'Vulnerabilidades': [] 
            }
            
            for script in port.findall('script'):
                script_id = script.get('id')
                script_output = script.get('output').strip() if script.get('output') else ""
                fila['Vulnerabilidades'].append(f"[{script_id}] {script_output}")

            filas_tabla.append(fila)
    return filas_tabla

def comparar_escaneos(ruta_xml_nuevo, ruta_xml_base):
    """Compares two scans and returns what is NEW in the current scan."""
    nuevo = generar_tabla_xml(ruta_xml_nuevo)
    base = generar_tabla_xml(ruta_xml_base)
    
    if not base or "Error" in base[0]: return nuevo # If no base exists, everything is new
    
    # Create a set of known IPs and Ports
    conocidos = set((f['IP'], f['Puerto']) for f in base)
    
    diferencias = []
    for f in nuevo:
        if (f['IP'], f['Puerto']) not in conocidos:
            diferencias.append(f)
            
    return diferencias
