// Test simple para verificar la función formatearFecha
const cms2Data = {
  "noticias": [
    {
      "fecha": "Julio 02, 2025",
      "texto": "Prueba de texto",
      "imagen": "test.jpg"
    }
  ]
};

function formatearFecha(fechaTexto) {
  try {
    const partes = fechaTexto.split(' ');
    if (partes.length >= 3) {
      const mes = partes[0];
      const ano = partes[2].replace(',', '');
      return `${mes} ${ano}`;
    }
    return fechaTexto;
  } catch (error) {
    return fechaTexto;
  }
}

console.log("Test formatearFecha:");
console.log("Input: 'Julio 02, 2025'");
console.log("Output:", formatearFecha("Julio 02, 2025"));
console.log("Expected: 'Julio 2025'");

console.log("\nTotal noticias disponibles:", cms2Data.noticias.length);
