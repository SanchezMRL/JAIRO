// Variable global para contar pruebas
let contadorPruebas = 0;

// Función para generar un hash (simplificado)
async function generarHash(file) {
    return new Promise((resolve) => {
        setTimeout(() => {
            const hash = "hash_" + Math.random().toString(36).substring(2, 15);
            resolve(hash);
        }, 1000);
    });
}

// Función principal
async function verificarVideo() {
    const fileInput = document.getElementById('videoFile');
    const resultadoDiv = document.getElementById('resultado');
    const hashDiv = document.getElementById('hashGenerado');

    if (!fileInput.files[0]) {
        resultadoDiv.textContent = "⚠️ Por favor, sube un video.";
        return;
    }

    const file = fileInput.files[0];
    resultadoDiv.textContent = "Procesando...";
    
    // 1. Generar hash del video (simulado)
    const hash = await generarHash(file);
    hashDiv.textContent = `Hash generado: ${hash}`;

    // 2. Lógica para que cada 4ta prueba sea AUTÉNTICO
    contadorPruebas++;
    let esAutentico;
    const hashesRegistrados = ["hash_abc123"]; // Hash válido de ejemplo

    if (contadorPruebas % 4 === 0) {
        // Fuerza resultado AUTÉNTICO cada 4ta prueba
        esAutentico = true;
        hashDiv.textContent = `Hash generado: hash_abc123`; // Mostrar hash "válido"
    } else {
        // Verificación normal (aleatoria)
        esAutentico = hashesRegistrados.includes(hash);
    }

    // 3. Mostrar resultado
    resultadoDiv.innerHTML = esAutentico 
        ? "✅ <span style='color:green;'>VIDEO AUTÉNTICO</span>" 
        : "❌ <span style='color:red;'>VIDEO ALTERADO</span>";
}
