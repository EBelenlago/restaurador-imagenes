import os
import cv2
from src.restaurador import Restaurador
# Carpeta de salida absoluta
output_dir = os.path.abspath("data/data-output")
os.makedirs(output_dir, exist_ok=True)
print("Salida absoluta:", output_dir)

# Crear el objeto restaurador
rest = Restaurador()
rest.cargar_imagen("data/data-raw/imagenprueba.jpeg")

# Guardar imágenes con ruta absoluta
ruido = rest.reducir_ruido()
print("Guardar ruido ->", cv2.imwrite(os.path.join(output_dir, "ruido.jpeg"), ruido))

contraste = rest.mejorar_contraste()
print("Guardar contraste ->", cv2.imwrite(os.path.join(output_dir, "contraste.jpeg"), contraste))

nitidez = rest.enfocar()
print("Guardar nitidez ->", cv2.imwrite(os.path.join(output_dir, "nitidez.jpeg"), nitidez))

# Restauración completa en un solo paso
final = rest.restaurar_completo()
print("Imagen restaurada guardada en data/data-output/restaurada.jpeg")

# Restauración completa en un solo paso
final = rest.restaurar_completo("data/data-output/restaurada.jpeg")

