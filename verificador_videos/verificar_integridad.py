import os
import hashlib
import json

VIDEO_DIR = "videos"
BLOCKCHAIN_FILE = "blockchain.json"
VERIFICACION_FILE = "verificacion.json"

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

verificaciones = []

for bloque in blockchain:
    archivo = bloque["nombre_archivo"]
    ruta = os.path.join(VIDEO_DIR, archivo)
    estado = "FALTANTE"
    hash_actual = None

    if os.path.exists(ruta):
        hash_actual = calcular_hash(ruta)
        if hash_actual == bloque["hash_video"]:
            estado = "OK"
        else:
            estado = "ALTERADO"

    verificaciones.append({
        "archivo": archivo,
        "estado": estado,
        "hash_registrado": bloque["hash_video"],
        "hash_actual": hash_actual if hash_actual else "-"
    })

with open(VERIFICACION_FILE, "w", encoding="utf-8") as f:
    json.dump(verificaciones, f, indent=2)

print("✅ Verificación completada. Resultado guardado en verificacion.json")

