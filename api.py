import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from restaurador import Restaurador

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # en dev, abierto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carpeta de salida
OUTPUT_DIR = "data/data-output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"mensaje": "API Restaurador de Imágenes funcionando 🚀"}

@app.post("/restaurar")
async def restaurar_imagen(file: UploadFile = File(...)):
    """
    Recibe una imagen subida por el usuario, la restaura y devuelve el archivo final.
    """
    # Guardar la imagen temporalmente
    ruta_temp = os.path.join(OUTPUT_DIR, file.filename)
    with open(ruta_temp, "wb") as f:
        f.write(await file.read())

    # Procesar la imagen con tu clase Restaurador
    rest = Restaurador()
    rest.cargar_imagen(ruta_temp)
    salida = os.path.join(OUTPUT_DIR, "restaurada.jpeg")
    rest.restaurar_completo(salida)

    return FileResponse(salida, media_type="image/jpeg", filename="restaurada.jpeg")

