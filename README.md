# restaurador-imagenes con filtros
##Restaurador de Imágenes  — Proyecto Final

Aplicación para restauración automática de imágenes mediante IA y FastAPI.
 Este proyecto permite subir una imagen dañada, restaurarla usando modelos de procesamiento visual y devolver la versión reparada en segundos 🚀

Descripción del proyecto
El Restaurador de Imágenes es una API desarrollada con FastAPI que permite subir imágenes deterioradas y restaurarlas automáticamente.
 El proceso se realiza con una clase llamada Restaurador, encargada de aplicar el modelo de reconstrucción visual.
 El proyecto está diseñado para ser ligero, modular y fácilmente integrable con aplicaciones web o móviles.

 Características principales

 Procesamiento de imágenes en tiempo real.

 Restauración automática mediante modelo preentrenado.

  API REST moderna con FastAPI y soporte CORS.

  Manejo de archivos temporales seguro.


  Preparado para desplegar en Render, Railway, o Docker.



restaurador-imagenes/ vista general

│
├── api.py                      # API principal con FastAPI
├── check_all.py                # Verifica rutas de entrada/salida
├── requirements.txt            # Dependencias del proyecto
├── README.md                   # Documentación principal
├── .gitignore                  # Ignora archivos temporales en Git
│
├── data/                       # Carpeta para imágenes de entrada/salida
│
├── frontend/                   # Interfaz web del usuario
│   ├── index.html              # Página principal
│   ├── styles.css              # Estilos visuales
│   └── script.js               # Lógica JS para enviar imágenes al backend
│
├── src/
│   ├── __init__.py
│   └── restaurador.py          # Clase principal de restauración
│
└── test/
    ├── __init__.py
    └── test_restaurador.py     # Pruebas del módulo restaurador


Estructura del repositorio

El proyecto está organizado de manera modular para separar claramente la lógica del backend (procesamiento de imágenes), el frontend (interfaz visual) y los recursos de datos.

frontend: 
Contiene todos los archivos relacionados con la interfaz visual del usuario.
 Esta parte permite al usuario subir imágenes, ver el resultado restaurado y manejar la interacción con la API.
index.html: Es la página principal del proyecto. Contiene la estructura HTML donde el usuario puede seleccionar una imagen desde su dispositivo y visualizar el resultado restaurado.
styles.css: Archivo de estilos que define la apariencia visual de la interfaz: colores, tamaños, bordes, tipografía y disposición de los elementos. Se encarga de que el sitio sea limpio y agradable.
script.js: Archivo JavaScript que conecta el frontend con el backend (API). Toma la imagen seleccionada por el usuario, la envía al servidor mediante una solicitud POST /restaurar, y luego muestra la imagen restaurada en pantalla sin necesidad de recargar la página.
Esta carpeta implementa la experiencia de usuario (UI) para interactuar de manera sencilla con el servicio de restauración.

src:
Aquí se encuentra el núcleo lógico del proyecto — el procesamiento y restauración de imágenes.

restaurador.py: Es la clase principal del sistema. Contiene la lógica que permite restaurar imágenes: carga de modelo, preprocesamiento, restauración y guardado del resultado final. La clase se inicializa una sola vez para optimizar recursos.
init.py: Indica que la carpeta src es un paquete de Python. Esto permite importar el módulo restaurador desde otros archivos (por ejemplo, desde api.py).
motor del proyecto, donde realmente ocurre el proceso de restauración visual.

Data:
Contiene las imágenes que se usan como entrada y salida del sistema.
data-raw: Se almacenan las imágenes originales (por ejemplo, las dañadas o con baja calidad).
data-output:  Aquí se guardan las imágenes resultantes luego de ser restauradas por el sistema.
almacena los datos brutos y los resultados finales del proceso de restauración.

test: Contiene los archivos de pruebas automáticas para verificar que el sistema funcione correctamente.
test-restaurador.py: Permite probar que el módulo restaurador.py funciona correctamente: carga, ejecución y salida de imágenes restauradas.

init.py: Permite que la carpeta sea reconocida como paquete y las pruebas puedan ser ejecutadas con frameworks como pytest.

se garantiza la calidad del código mediante pruebas de funcionamiento

Archivos principales en la raíz
Archivo
Descripción
api.py
Es el servidor principal del proyecto, desarrollado con FastAPI. Define los endpoints de la API (por ejemplo / y /restaurar). Se encarga de recibir imágenes del frontend, procesarlas usando la clase Restaurador y devolver el resultado restaurado.
check_all.py
Es un script auxiliar que verifica que las rutas de entrada y salida existen correctamente y que los archivos necesarios estén en su lugar antes de ejecutar la API. Muy útil para depuración.
requirements.txt
Lista de dependencias necesarias para ejecutar el proyecto. Permite instalar todas las librerías con un solo comando (pip install -r requirements.txt).
README.md
Archivo de documentación principal, Explica la descripción del proyecto, instalación, uso, estructura, y autores, etc.
.gitignore
Indica a Git qué archivos o carpetas no deben subirse al repositorio (entornos virtuales, archivos temporales o imágenes generadas).





Tecnologías y librerías usadas
Python (backend).


Librerías de imagen (ej.: Pillow / OpenCV — si se usan en el proyecto).


Frameworks web ligeros (por ejemplo Flask/FastAPI si están presentes).


Frontend: HTML/CSS/JS (carpeta frontend).


Instalación y ejecución
1️⃣ Clonar el repositorio
git clone https://github.com/tu-usuario/restaurador_imagenes.git
cd restaurador_imagenes

2️⃣ Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Mac/Linux
venv\Scripts\activate     # En Windows

3️⃣ Instalar dependencias
instalar las librerías manualmente
pip install fastapi uvicorn pillow opencv-python starlette

4️⃣ Ejecutar el servidor
uvicorn api:app --reload

Una vez iniciado, abrí en el navegador:
http://127.0.0.1:8000


🧠 Uso de la API
POST /restaurar
Permite subir una imagen y devuelve la versión restaurada.
Ejemplo en cURL:
curl -X POST "http://127.0.0.1:8000/restaurar" \
-F "file=@imagenprueba.jpeg" \
-o salida.jpeg

Respuesta:
Código 200 OK → Devuelve la imagen restaurada (image/jpeg).


Código 503 → Modelo no inicializado.


Código 500 → Error interno durante el proceso.


 Ejemplo de flujo interno
El usuario envía una imagen (UploadFile).


Se guarda temporalmente en disco (tempfile.NamedTemporaryFile).


Se llama al método GLOBAL_RESTAURADOR.restaurar_completo().


El sistema genera un archivo restaurado en data/data-output/.


FastAPI devuelve la imagen procesada como respuesta.



🧠 Dependencias utilizadas
Librería
Descripción
FastAPI
Framework para construir APIs rápidas y asincrónicas
Uvicorn
Servidor ASGI ligero para ejecutar la API
Starlette
Base de FastAPI (manejo de middleware, respuestas y concurrencia)
Pillow
Procesamiento de imágenes
OpenCV
Operaciones de mejora y filtrado de imágenes
(Opcional) torch / tensorflow
Modelos de restauración o redes neuronales


 Posibles mejoras futuras 
Añadir una interfaz web con Streamlit o React.


Incluir un modelo de restauración con aprendizaje profundo (p. ej., ESRGAN).


Guardar el historial de imágenes procesadas.


Implementar autenticación de usuario.


Agregar soporte para restaurar videos o fotos antiguas en lote.


