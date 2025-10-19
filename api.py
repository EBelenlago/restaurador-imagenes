import sys
import os
import tempfile
from uuid import uuid4

from starlette.concurrency import run_in_threadpool 

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from restaurador import Restaurador


#inicializamos el Restaurador una sola vez, para evitar recargar modelos pesados en cada petición
GLOBAL_RESTAURADOR = None
try:
    GLOBAL_RESTAURADOR = Restaurador()
    print("Restaurador inicializado y listo para usar.")
except Exception as e:
    print(f"ERROR: No se pudo inicializar la clase Restaurador. {e}")
        

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


OUTPUT_DIR = "data/data-output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"mensaje": "API Restaurador de Imágenes funcionando 🚀"}


def _procesar_imagen_sync(temp_in_path: str, temp_out_path: str):
    """Función síncrona que contiene la lógica de Restaurador."""
    if not GLOBAL_RESTAURADOR:
        raise RuntimeError("El servicio de restauración no está disponible.")
    

    GLOBAL_RESTAURADOR.restaurar_completo(temp_in_path, temp_out_path) 
    
    return temp_out_path


@app.post("/restaurar")
async def restaurar_imagen(file: UploadFile = File(...)):
    if not GLOBAL_RESTAURADOR:
        raise HTTPException(status_code=503, detail="El servicio de restauración no está operativo. Revise la inicialización del modelo.")
        
    temp_in_path = ""
    temp_out_path = ""
    
    #generamos nombres de archivos únicos para entrada y salida
    unique_id = uuid4().hex
    temp_out_path = os.path.join(tempfile.gettempdir(), f"restaurada_{unique_id}.jpeg")

    try:
        #se crea un archivo temporal de entrada con esto aseguramos un nombre de archivo único para la imagen subida
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            temp_in_path = tmp.name
        
        #guardamos la imagen del usuario en el disco temporal
        with open(temp_in_path, "wb") as f:
            f.write(await file.read())

        #procesamos la imagen (CPU-bound), con run_in_threadpool previene el bloqueo del servidor
        salida_final = await run_in_threadpool(_procesar_imagen_sync, temp_in_path, temp_out_path)

        return FileResponse(
            salida_final, 
            media_type="image/jpeg", 
            filename=f"restaurada_{file.filename.split('.')[0]}.jpeg"
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error durante la restauración: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno al procesar la imagen: {e}")
        
    finally: #limpieza de archivos temporales
        if os.path.exists(temp_in_path):
            os.remove(temp_in_path)

        #no se elimina temp_out_path aquí, porque FastAPI lo necesita para enviar la imagen.


