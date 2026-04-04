import subprocess #Ejecutar programas externos/comandos del sistema
from pathlib import Path #Manejo de rutas de archivos
import os #Acceso a funciones del sistema operativo


def ejecutar_segun_os(os_name, tool):
    subprocess.run(["clear"])
    # Aqui buscamos la carpeta con el nombre del sistema y el archivo
    config_os = {
        'linux': {'folder': 'Linux', 'bin_name': 'nmap'},
        'windows': {'folder': 'Windows', 'bin_name': 'nmap.exe'},
        'macos': {'folder': 'macos', 'bin_name': 'nmap'}
    }
    
    # aqui si el nombre contiene win se ocupa la configuracion de windows y asi (asegura por asi decirlo)
    if 'Win' in os_name:
        config = config_os['windows']
    elif 'Dar' in os_name or 'mac' in os_name:
        config = config_os['macos']
    elif 'Linux' in os_name:
        config = config_os['linux']
    else:
        print(f"No existe")
        return None
    
    #ruta
    base_path = Path(__file__).parent.parent #Obtiene la ruta del directorio donde está guardado este archivo, y agarra el padre que seria hasta tools(creo)
    bin_path = base_path / "tools" / "tools_bin" / config['folder'] / tool / config['bin_name']
    
    os.chmod(bin_path, 0o777)
    
    #Si no existe el archivo
    if not bin_path.exists():
        print(f"No se encontro en: {bin_path}")
        return None
    
    #Esto es para verificar algun error (gracias chat por)
    try:
        print(f"Ejecutando desde: {bin_path}")
        resultado = subprocess.run([str(bin_path), "--version"], capture_output = True, text = True)
        print(resultado.stdout.strip(), "\n")
        return resultado
    
    except Exception as e:
        print(f"Error: {e}")
        return None