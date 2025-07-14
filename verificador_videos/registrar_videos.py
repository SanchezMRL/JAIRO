import os
import hashlib
import json
from datetime import datetime

VIDEO_DIR = "videos"
BLOCKCHAIN_FILE = "blockchain.json"

# Asegura que existan la carpeta y el archivo
os.makedirs(VIDEO_DIR, exist_ok=True)
if not os.path.exists(BLOCKCHAIN_FILE):
    with open(BLOCKCHAIN_FILE, "w") as f:
        json.dump([], f)

# Función para calcular hash SHA-256 de un archivo
def calcular_hash(ruta):
    sha = hashlib.sha256()
    with open(ruta, "rb") as f:
        while chunk := f.read(4096):
            sha.update(chunk)
    return sha.hexdigest()

# Cargar blockchain actual
with open(BLOCKCHAIN_FILE, "r") as f:
    try:
        blockchain = json.load(f)
    except json.JSONDecodeError:
        print("⚠️ El archivo blockchain.json está dañado. Se reiniciará.")
        blockchain = []

archivos_registrados = {bloque["nombre_archivo"] for bloque in blockchain}

nuevos_registrados = 0

# Procesar videos nuevos
for archivo in sorted(os.listdir(VIDEO_DIR)):
    ruta = os.path.join(VIDEO_DIR, archivo)
    if os.path.isfile(ruta) and archivo not in archivos_registrados:
        try:
            hash_video = calcular_hash(ruta)
            hash_anterior = blockchain[-1]["hash_bloque"] if blockchain else "0"
            datos_bloque = f"{archivo}{hash_video}{datetime.now()}{hash_anterior}"
            hash_bloque = hashlib.sha256(datos_bloque.encode()).hexdigest()

            bloque = {
                "indice": len(blockchain),
                "nombre_archivo": archivo,
                "hash_video": hash_video,
                "hash_bloque": hash_bloque,
                "hash_anterior": hash_anterior,
                "timestamp": datetime.now().isoformat()
            }

            blockchain.append(bloque)
            nuevos_registrados += 1
            print(f"✅ Registrado: {archivo} - Hash: {hash_video[:10]}...")

        except Exception as e:
            print(f"❌ Error con el archivo {archivo}: {e}")

# Guardar blockchain actualizada
with open(BLOCKCHAIN_FILE, "w") as f:
    json.dump(blockchain, f, indent=4)

if nuevos_registrados == 0:
    print("📭 No hay videos nuevos para registrar.")
else:
    print(f"📝 {nuevos_registrados} video(s) registrado(s) correctamente.")
