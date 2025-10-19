import cv2
import numpy as np

class Restaurador:
    def __init__(self):
        """
        Inicializa el restaurador. Solo carga modelos o recursos pesados aquí.
        """
        pass

    def reducir_ruido(self, img_actual: np.ndarray):
        """
        Reduce el ruido de la imagen con Non-Local Means Denoising
        """
        return cv2.fastNlMeansDenoisingColored(img_actual, None, 10, 10, 7, 21)

    def mejorar_contraste(self, img_actual: np.ndarray):
        """
        Mejora el contraste usando CLAHE (Adaptive Histogram Equalization)
        """
        lab = cv2.cvtColor(img_actual, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)

        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l2 = clahe.apply(l)

        lab = cv2.merge((l2, a, b))
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    def enfocar(self, img_actual: np.ndarray):
        """
        Aplica un filtro de nitidez (sharpening) seguro
        """

        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]], dtype=np.float32)
        return cv2.filter2D(img_actual, -1, kernel)

    def reparar_manchas(self, img_actual: np.ndarray, ruta_mascara: str):
        """
        Rellena rayas o manchas usando inpainting.
        """

        mascara = cv2.imread(ruta_mascara, 0)  # escala de grises
        if mascara is None:
            raise ValueError(f"No se pudo cargar la máscara en {ruta_mascara}. Revisa la ruta.")

        return cv2.inpaint(img_actual, mascara, 3, cv2.INPAINT_TELEA)


    def restaurar_completo(self, ruta_entrada: str, ruta_salida: str = "data/data-output/restaurada.jpeg"):
        """
        Carga la imagen, aplica la cadena de filtros y guarda el resultado.
        """
        
        img_original = cv2.imread(ruta_entrada)
        
        if img_original is None:
            raise ValueError(f"No se pudo cargar la imagen en {ruta_entrada}. Revisa la ruta.")

        #reducimos el ruido, el resultado se guarda en una variable local
        paso1 = cv2.fastNlMeansDenoisingColored(img_original, None, 3, 3, 7, 21)

        #mejoramos el contraste (CLAHE con clipLimit más bajo)
        lab = cv2.cvtColor(paso1, cv2.COLOR_BGR2LAB) 
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l2 = clahe.apply(l)
        lab = cv2.merge((l2, a, b))
        paso2 = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]], dtype=np.float32)
        paso3 = cv2.filter2D(paso2, -1, kernel)

        #guardamos resultado final usando la ruta de salida pasada como argumento

        ok = cv2.imwrite(ruta_salida, paso3) 
        
        if ok:
            print(f"Imagen final guardada en: {ruta_salida}")
        else:
            print(f"No se pudo guardar en: {ruta_salida}")
            
        return paso3 #se devuelve el resultado si es necesario