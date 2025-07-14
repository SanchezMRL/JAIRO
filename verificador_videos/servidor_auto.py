import http.server
import socketserver
import threading
import subprocess
import time
import os
import json
from urllib.parse import urlparse

PUERTO = 8000
CARPETA = os.path.dirname(os.path.abspath(__file__))

def verificar_periodicamente():
    while True:
        try:
            subprocess.run(["python", "verificar_integridad.py"], cwd=CARPETA)
        except Exception as e:
            print(f"Error al verificar: {e}")
        time.sleep(10)

class MiHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        ruta = urlparse(self.path).path
        if ruta == "/registrar":
            try:
                subprocess.run(["python", "registrar_videos.py"], cwd=CARPETA)
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"estado": "ok", "mensaje": "Videos registrados correctamente."}).encode())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f"Error: {e}".encode())

        elif ruta == "/verificar":
            try:
                subprocess.run(["python", "verificar_integridad.py"], cwd=CARPETA)
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"estado": "ok", "mensaje": "Verificación completa."}).encode())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f"Error: {e}".encode())

        else:
            super().do_GET()

    def log_message(self, format, *args):
        return  # Silencia logs

verificacion_thread = threading.Thread(target=verificar_periodicamente, daemon=True)
verificacion_thread.start()

os.chdir(CARPETA)
with socketserver.TCPServer(("", PUERTO), MiHandler) as httpd:
    print(f"🌐 Servidor corriendo en http://localhost:{PUERTO}")
    httpd.serve_forever()
