
import os
import hashlib
import json
from datetime import datetime

VIDEO_DIR = "videos"
BLOCKCHAIN_FILE = "blockchain.json"

# Asegurarse de que exista la carpeta y archivo
os.makedirs(VIDEO_DIR, exist_ok=True)
if not os.path.exists(BLOCKCHAIN_FILE):
    with open(BLOCKCHAIN_FILE, "w") as f:
        json.dump([], f)

def calcular_hash(ruta):
    sha = hashlib.sha256()
    with open(ruta, "rb") as f:
        while chunk := f.read(4096):
            sha.update(chunk)
    return sha.hexdigest()

# Cargar blockchain actual
with open(BLOCKCHAIN_FILE, "r") as f:
    blockchain = json.load(f)

archivos_registrados = {bloque["nombre_archivo"] for bloque in blockchain}

for archivo in os.listdir(VIDEO_DIR):
    ruta = os.path.join(VIDEO_DIR, archivo)
    if os.path.isfile(ruta) and archivo not in archivos_registrados:
        hash_video = calcular_hash(ruta)
        hash_anterior = blockchain[-1]["hash_bloque"] if blockchain else "0"
        bloque_datos = f"{archivo}{hash_video}{datetime.now()}{hash_anterior}"
        hash_bloque = hashlib.sha256(bloque_datos.encode()).hexdigest()

        nuevo_bloque = {
            "indice": len(blockchain),
            "nombre_archivo": archivo,
            "hash_video": hash_video,
            "hash_bloque": hash_bloque,
            "hash_anterior": hash_anterior,
            "timestamp": datetime.now().isoformat()
        }

        blockchain.append(nuevo_bloque)
        print(f"✅ Registrado: {archivo} - Hash: {hash_video[:10]}...")

# Guardar actualización
with open(BLOCKCHAIN_FILE, "w") as f:
    json.dump(blockchain, f, indent=4)
