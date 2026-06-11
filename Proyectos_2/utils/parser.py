# utils/parser.py
import xml.etree.ElementTree as ET
from pathlib import Path
import os

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

def categorizar_severidad(script_id, output):
    """Categoriza la severidad basada en palabras clave en el output del script."""
    out_lower = output.lower()
    if any(k in out_lower for k in ["critical", "rce", "remote code execution", "fatal"]):
        return "critical", "Crítica"
    if any(k in out_lower for k in ["high", "vulnerable", "exploit", "cve-20"]):
        return "high", "Alta"
    if any(k in out_lower for k in ["medium", "warning", "bypass", "weak"]):
        return "medium", "Media"
    return "low", "Baja"

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
        
        # Estado del host
        status_el = host.find('status')
        host_status = status_el.get('state') if status_el is not None else "unknown"

        for port in host.findall('.//port'):
            estado_el = port.find('state')
            servicio_el = port.find('service')
            
            fila = {
                'IP': ip,
                'Puerto': port.get('portid'),
                'Estado': estado_el.get('state') if estado_el is not None else "N/D",
                'Servicio': servicio_el.get('name') if servicio_el is not None else "N/D",
                'HostStatus': host_status,
                'Vulnerabilidades': [] 
            }
            
            for script in port.findall('script'):
                script_id = script.get('id')
                script_output = script.get('output').strip() if script.get('output') else ""
                
                sev_key, sev_label = categorizar_severidad(script_id, script_output)
                
                fila['Vulnerabilidades'].append({
                    'id': script_id,
                    'output': script_output,
                    'severity': sev_key,
                    'sev_label': sev_label
                })

            filas_tabla.append(fila)
    return filas_tabla

def buscar_escaneos(directorio, base_name, extension=".xml"):
    """
    Finds all scan files for a category and sorts them by modification time (newest first).
    Handles base filenames and numbered versions (e.g., scan.xml, scan_1.xml, etc.).
    """
    path = Path(directorio)
    if not path.exists():
        return []
    
    # Pattern to match the base name and numbered versions
    archivos = []
    for f in path.glob(f"{base_name}*{extension}"):
        # Filter to ensure we don't pick up other categories (e.g., 'internet_lento' vs 'internet_lento_vulnerabilidades')
        # Check if the filename is exactly base_name + extension or base_name + "_" + number + extension
        name = f.name
        if name == f"{base_name}{extension}":
            archivos.append(f)
        elif name.startswith(f"{base_name}_") and name[len(base_name)+1:-len(extension)].isdigit():
            archivos.append(f)
            
    # Sort by modification time, newest first
    archivos.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    return [str(a) for a in archivos]

def obtener_datos_completos(os_folder):
    """Lee todos los archivos XML en el directorio de resultados y los combina."""
    base_path = Path(__file__).parent.parent
    resultados_dir = base_path / "utils" / "Resultados" / os_folder / "Nmap"
    
    todos_los_datos = []
    if not resultados_dir.exists():
        return todos_los_datos

    for archivo in resultados_dir.glob("*.xml"):
        if archivo.suffix == ".xml":
            datos = generar_tabla_xml(str(archivo))
            if datos and "Error" not in datos[0]:
                todos_los_datos.extend(datos)
    
    return todos_los_datos

def obtener_estadisticas_dashboard(os_folder):
    datos = obtener_datos_completos(os_folder)
    
    ips_unicas = set()
    vulns_por_sev = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    total_vulns = 0
    
    vulnerabilidades_lista = []
    
    for d in datos:
        ips_unicas.add(d['IP'])
        for v in d['Vulnerabilidades']:
            vulns_por_sev[v['severity']] += 1
            total_vulns += 1
            vulnerabilidades_lista.append({
                'severity': v['severity'],
                'sev_label': v['sev_label'],
                'desc': f"[{v['id']}] {v['output'][:100]}...",
                'device': d['IP'],
                'status': 'open'
            })
            
    riesgo = "BAJO"
    if vulns_por_sev["critical"] > 0: riesgo = "CRÍTICO"
    elif vulns_por_sev["high"] > 0: riesgo = "ALTO"
    elif vulns_por_sev["medium"] > 0: riesgo = "MEDIO"

    # Obtener la fecha del último escaneo
    base_path = Path(__file__).parent.parent
    resultados_dir = base_path / "utils" / "Resultados" / os_folder / "Nmap"
    last_scan = "N/A"
    if resultados_dir.exists():
        archivos = list(resultados_dir.glob("*.xml"))
        if archivos:
            latest_file = max(archivos, key=lambda x: x.stat().st_mtime)
            from datetime import datetime
            last_scan = datetime.fromtimestamp(latest_file.stat().st_mtime).strftime('%d/%m/%y')

    return {
        "active_devices": len(ips_unicas),
        "total_vulns": total_vulns,
        "risk_level": riesgo,
        "vulns_by_severity": vulns_por_sev,
        "vulnerabilities": vulnerabilidades_lista,
        "devices": list(ips_unicas),
        "last_scan": last_scan
    }

def comparar_escaneos(ruta_xml_nuevo, ruta_xml_base):
    """Compares two scans and returns what is NEW in the current scan."""
    try:
        nuevo = generar_tabla_xml(ruta_xml_nuevo)
        base = generar_tabla_xml(ruta_xml_base)
    except Exception as e:
        return [{"Error": f"Error al comparar archivos: {e}"}]
    
    if not base or (isinstance(base[0], dict) and "Error" in base[0]): 
        return nuevo # If no base exists or is invalid, everything is new
    
    if not nuevo or (isinstance(nuevo[0], dict) and "Error" in nuevo[0]):
        return nuevo # Return the error from the new file
    
    # Create a set of known IPs and Ports for efficient lookup
    conocidos = set((f['IP'], f['Puerto']) for f in base)
    
    diferencias = []
    for f in nuevo:
        if (f['IP'], f['Puerto']) not in conocidos:
            diferencias.append(f)
            
    return diferencias
