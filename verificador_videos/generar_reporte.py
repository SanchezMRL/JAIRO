
import os
import hashlib
import json

VIDEO_DIR = "videos"
BLOCKCHAIN_FILE = "blockchain.json"
REPORTE_FILE = "reporte.html"

def calcular_hash(ruta):
    sha = hashlib.sha256()
    with open(ruta, "rb") as f:
        while chunk := f.read(4096):
            sha.update(chunk)
    return sha.hexdigest()

# Cargar blockchain
if not os.path.exists(BLOCKCHAIN_FILE):
    print("❌ No existe blockchain.json")
    exit()

with open(BLOCKCHAIN_FILE, "r") as f:
    blockchain = json.load(f)

# Generar HTML
html = """
<!DOCTYPE html>
<html lang='es'>
<head>
    <meta charset='UTF-8'>
    <title>Reporte de Integridad de Videos</title>
    <style>
        body { font-family: Arial; background: #f4f4f4; margin: 20px; }
        h1 { color: #2c3e50; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 8px 12px; border: 1px solid #ccc; text-align: left; }
        th { background: #3498db; color: white; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        .ok { background-color: #d4edda; }
        .alterado { background-color: #f8d7da; }
        .faltante { background-color: #fff3cd; }
    </style>
</head>
<body>
    <h1>📋 Reporte de Integridad de Videos</h1>
    <table>
        <tr>
            <th>#</th>
            <th>Archivo</th>
            <th>Estado</th>
            <th>Hash Registrado</th>
            <th>Hash Actual</th>
            <th>Fecha Registro</th>
        </tr>
"""

for bloque in blockchain:
    archivo = bloque["nombre_archivo"]
    ruta = os.path.join(VIDEO_DIR, archivo)
    hash_actual = None
    estado = "FALTANTE"
    clase = "faltante"

    if os.path.exists(ruta):
        hash_actual = calcular_hash(ruta)
        if hash_actual == bloque["hash_video"]:
            estado = "OK"
            clase = "ok"
        else:
            estado = "ALTERADO"
            clase = "alterado"

    html += f"""
        <tr class="{clase}">
            <td>{bloque["indice"]}</td>
            <td>{archivo}</td>
            <td><strong>{estado}</strong></td>
            <td>{bloque["hash_video"][:20]}...</td>
            <td>{hash_actual[:20] + "..." if hash_actual else "-"}</td>
            <td>{bloque["timestamp"]}</td>
        </tr>
    """

html += """
    </table>
</body>
</html>
"""

# Guardar archivo HTML
with open(REPORTE_FILE, "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ Reporte generado: {REPORTE_FILE}")
