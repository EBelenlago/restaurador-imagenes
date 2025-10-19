const form = document.getElementById("form-restaurar");
const fileInput = document.getElementById("file");
const preview = document.getElementById("preview");
const resultado = document.getElementById("resultado");
const estado = document.getElementById("estado");
const download = document.getElementById("download");

// URL de tu API FastAPI
const API_URL = "http://127.0.0.1:8000/restaurar";

// Vista previa de la imagen original
fileInput.addEventListener("change", () => {
  const file = fileInput.files?.[0];
  if (!file) return;
  const url = URL.createObjectURL(file);
  preview.src = url;
  resultado.src = "";
  download.style.display = "none";
  estado.textContent = "";
});

// Enviar al backend y mostrar resultado
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const file = fileInput.files?.[0];
  if (!file) {
    estado.textContent = "Seleccioná una imagen primero.";
    return;
  }

  estado.textContent = "Procesando...";
  const fd = new FormData();
  fd.append("file", file, file.name);

  try {
    const resp = await fetch(API_URL, { method: "POST", body: fd });
    if (!resp.ok) throw new Error(`Error ${resp.status}`);

    // La API devuelve la imagen como binario
    const blob = await resp.blob();
    const url = URL.createObjectURL(blob);

    resultado.src = url;
    download.href = url;
    download.style.display = "inline-block";
    estado.textContent = "Listo ✅";
  } catch (err) {
    console.error(err);
    estado.textContent = "Ocurrió un error procesando la imagen.";
  }
});
