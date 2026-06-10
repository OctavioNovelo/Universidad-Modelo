import http.server
import socketserver
import json
import os
from pathlib import Path
import utils.parser as parser
from utils.system_info import obtener_sistema_operativo, obtener_carpeta_os

PORT = 8080
DIRECTORY = "frontend/pages/HERA_Dashboard/dashboard/dashboard"

class HeraAPIHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        if self.path.startswith('/api/'):
            self.handle_api()
        else:
            super().do_GET()

    def handle_api(self):
        # Obtener el SO para saber qué carpeta de resultados usar
        os_name = obtener_sistema_operativo()
        os_folder = obtener_carpeta_os(os_name)
        
        response_data = {}
        status_code = 200

        if self.path == '/api/stats':
            response_data = parser.obtener_estadisticas_dashboard(os_folder)
        elif self.path == '/api/vulnerabilities':
            stats = parser.obtener_estadisticas_dashboard(os_folder)
            response_data = stats.get("vulnerabilities", [])
        elif self.path == '/api/devices':
            datos = parser.obtener_datos_completos(os_folder)
            # Agrupar por IP para mostrar en la tabla de escaneo
            devices_map = {}
            for d in datos:
                ip = d['IP']
                if ip not in devices_map:
                    devices_map[ip] = {
                        "ip": ip,
                        "ports": [],
                        "services": [],
                        "status": d.get("HostStatus", "online")
                    }
                if d['Puerto'] not in devices_map[ip]["ports"]:
                    devices_map[ip]["ports"].append(d['Puerto'])
                    devices_map[ip]["services"].append(d['Servicio'])
            
            response_data = list(devices_map.values())
        else:
            status_code = 404
            response_data = {"error": "Endpoint no encontrado"}

        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode('utf-8'))

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with socketserver.TCPServer(("", PORT), HeraAPIHandler) as httpd:
        print(f"Servidor HERA Dashboard activo en http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor detenido.")
            httpd.server_close()
