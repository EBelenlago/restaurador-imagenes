const form = document.getElementById("form-restaurar");
const fileInput = document.getElementById("file");
const preview = document.getElementById("preview");
const resultado = document.getElementById("resultado");
const estado = document.getElementById("estado");
const download = document.getElementById("download");
const modoSelect = document.getElementById("modo");
const filtrosPanel = document.querySelector(".filtros");

const API_URL = "http://127.0.0.1:8000/restaurar";

// Vista previa de imagen
fileInput.addEventListener("change", () => {
  const file = fileInput.files?.[0];
  if (!file) return;
  const url = URL.createObjectURL(file);
  preview.src = url;
  resultado.src = "";
  download.style.display = "none";
  estado.textContent = "";
});

// Mostrar u ocultar filtros según el modo
modoSelect.addEventListener("change", () => {
  filtrosPanel.style.display = modoSelect.value === "avanzado" ? "block" : "none";
});

// Se actualiza valor de cada slider en tiempo real
document.querySelectorAll(".filtro input[type='range']").forEach((slider) => {
  const labelValor = document.createElement("span");
  labelValor.textContent = slider.value;
  labelValor.style.marginLeft = "0.5rem";
  labelValor.style.color = "#9ad0f5";
  slider.parentNode.appendChild(labelValor);

  slider.addEventListener("input", () => {
    labelValor.textContent = slider.value;
  });
});

// Enviamos imagen + filtros al backend
form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const file = fileInput.files?.[0];
  if (!file) {
    estado.textContent = "Seleccioná una imagen primero.";
    return;
  }

  estado.textContent = "Procesando...";
  resultado.src = "";
  download.style.display = "none";

  const fd = new FormData();
  fd.append("file", file, file.name);

  // Solo se aplican filtros si está en modo avanzado
  if (modoSelect.value === "avanzado") {
    const filtros = document.querySelectorAll(".filtro input[type='range']");
    filtros.forEach((f) => fd.append(f.name, f.value));
  }

  try {
    const resp = await fetch(API_URL, { method: "POST", body: fd });
    if (!resp.ok) throw new Error(`Error ${resp.status}`);

    const blob = await resp.blob();
    const url = URL.createObjectURL(blob);

    resultado.src = url;
    download.href = url;
    download.style.display = "inline-block";
    estado.textContent = "✅ Imagen restaurada con éxito.";
  } catch (err) {
    console.error(err);
    estado.textContent = "❌ Ocurrió un error procesando la imagen.";
  }
});

