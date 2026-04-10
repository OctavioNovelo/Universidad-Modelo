# utils/parser.py
import xml.etree.ElementTree as ET
from pathlib import Path

def buscar_en_gnmap(ruta_gnmap, termino_busqueda):
    resultados = []
    try:
        with open(ruta_gnmap, "r") as f:
            for linea in f:
                # Ignoramos los comentarios de nmap
                if not linea.startswith("#") and termino_busqueda.lower() in linea.lower():
                    resultados.append(linea.strip())
        return resultados
    except FileNotFoundError:
        return ["Error: No se encontró el archivo de resultados. Ejecuta un escaneo primero."]

import xml.etree.ElementTree as ET

def generar_tabla_xml(ruta_xml):
    try:
        tree = ET.parse(ruta_xml)
        root = tree.getroot()
    except Exception as e:
        print(f"Error al leer el XML: {e}")
        return []

    filas_tabla = [] # Lista plana para la tabla

    for host in root.findall('host'):
        address = host.find("address[@addrtype='ipv4']")
        ip = address.get('addr') if address is not None else "Desconocido"
        
        for port in host.findall('.//port'):
            estado_el = port.find('state')
            servicio_el = port.find('service')
            
            # Creamos una fila por cada puerto, usando las llaves exactas del CLI
            fila = {
                'IP': ip,
                'Puerto': port.get('portid'),
                'Estado': estado_el.get('state') if estado_el is not None else "N/D",
                'Servicio': servicio_el.get('name') if servicio_el is not None else "N/D",
                'Vulnerabilidades': [] 
            }
            
            # Extraer vulnerabilidades de los scripts
            for script in port.findall('script'):
                script_id = script.get('id')
                script_output = script.get('output').strip()
                fila['Vulnerabilidades'].append(f"[{script_id}] {script_output}")

            filas_tabla.append(fila)

    return filas_tabla