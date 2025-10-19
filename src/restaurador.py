import cv2
import numpy as np

class Restaurador:
    def __init__(self):
        """
        Inicializa el restaurador sin cargar imagen.
        La imagen se carga con el método cargar_imagen().
        """
        self.img = None

    def cargar_imagen(self, ruta_imagen: str = "data/data-raw/imagenprueba.jpeg"):
        """
        Carga la imagen desde la ruta especificada.
        Por defecto usa data/data-raw/imagenprueba.jpeg
        """
        self.img = cv2.imread(ruta_imagen)

        if self.img is None:
            raise ValueError(f"No se pudo cargar la imagen en {ruta_imagen}. Revisa la ruta.")

    def reducir_ruido(self):
        """
        Reduce el ruido de la imagen con Non-Local Means Denoising
        """
        if self.img is None:
            raise ValueError("Primero cargá una imagen con cargar_imagen()")
        return cv2.fastNlMeansDenoisingColored(self.img, None, 10, 10, 7, 21)

    def mejorar_contraste(self):
        """
        Mejora el contraste usando CLAHE (Adaptive Histogram Equalization)
        """
        if self.img is None:
            raise ValueError("Primero cargá una imagen con cargar_imagen()")
        lab = cv2.cvtColor(self.img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)

        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l2 = clahe.apply(l)

        lab = cv2.merge((l2, a, b))
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    def enfocar(self):
        """
        Aplica un filtro de nitidez (sharpening) seguro
        """
        if self.img is None:
            raise ValueError("Primero cargá una imagen con cargar_imagen()")
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]], dtype=np.float32)
        return cv2.filter2D(self.img, -1, kernel)

    def reparar_manchas(self, ruta_mascara: str):
        """
        Rellena rayas o manchas usando inpainting.
        La máscara debe estar en blanco (zonas a reparar) y negro (zonas intactas).
        """
        if self.img is None:
            raise ValueError("Primero cargá una imagen con cargar_imagen()")

        mascara = cv2.imread(ruta_mascara, 0)  # escala de grises
        if mascara is None:
            raise ValueError(f"No se pudo cargar la máscara en {ruta_mascara}. Revisa la ruta.")

        return cv2.inpaint(self.img, mascara, 3, cv2.INPAINT_TELEA)

    def restaurar_completo(self, ruta_salida: str = "data/data-output/restaurada.jpeg"):
        """
        Aplica reducción de ruido, mejora de contraste y enfoque en cadena
        de manera más suave para no perder detalles.
        """
        if self.img is None:
            raise ValueError("Primero cargá una imagen con cargar_imagen()")

        # 1. Reducir ruido (más suave)
        paso1 = cv2.fastNlMeansDenoisingColored(self.img, None, 3, 3, 7, 21)

        # 2. Mejorar contraste (CLAHE con clipLimit más bajo)
        lab = cv2.cvtColor(paso1, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l2 = clahe.apply(l)
        lab = cv2.merge((l2, a, b))
        paso2 = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

        # 3. Enfocar (kernel de sharpen seguro)
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]], dtype=np.float32)
        paso3 = cv2.filter2D(paso2, -1, kernel)

        # Guardar resultado final
        ok = cv2.imwrite(ruta_salida, paso3)
        if ok:
            print(f"✅ Imagen final guardada en: {ruta_salida}")
        else:
            print(f"❌ No se pudo guardar en: {ruta_salida}")
        return paso3
