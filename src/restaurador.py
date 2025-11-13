import cv2
import numpy as np
import torch # Se mantiene solo para la detección de GPU/CPU, ya que no se usa para procesamiento de imágenes.


class Restaurador:
    def __init__(self):
        """Inicializa recursos pesados."""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"🖥️ Usando dispositivo: {self.device} (Solo para info, el modelo de IA avanzado no se usará)")
        self.gfpgan = None
        print("✅ Restaurador de imágenes inicializado (Funcionalidad avanzada deshabilitada).")

    # ---------------- FILTROS BASE ----------------

    def reducir_ruido(self, img_actual: np.ndarray):
        """Reduce ruido de color."""
        return cv2.fastNlMeansDenoisingColored(img_actual, None, 10, 10, 7, 21)

    def mejorar_contraste(self, img_actual: np.ndarray):
        """Mejora el contraste usando CLAHE."""
        lab = cv2.cvtColor(img_actual, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
        l2 = clahe.apply(l)
        lab = cv2.merge((l2, a, b))
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    def corregir_color(self, img_actual: np.ndarray):
        """Corrige dominantes de color (requiere opencv-contrib)."""
        try:
            wb = cv2.xphoto.createSimpleWB()
            return wb.balanceWhite(img_actual)
        except AttributeError:
            # Devuelve la imagen sin cambios si no está instalada la versión contrib
            return img_actual

    def enfocar_suave(self, img_actual: np.ndarray, amount=1.2):
        """Enfoque suave tipo unsharp masking."""
        blurred = cv2.GaussianBlur(img_actual, (0, 0), 3)
        return cv2.addWeighted(img_actual, 1 + amount, blurred, -amount, 0)

    def reparar_manchas(self, img_actual: np.ndarray):
        """Detecta y repara zonas desgastadas (claras/oscuras)."""
        gray = cv2.cvtColor(img_actual, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.medianBlur(gray, 5)

        mask_bright = cv2.adaptiveThreshold(
            gray_blur, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 35, -10
        )

        mask_dark = cv2.adaptiveThreshold(
            gray_blur, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV, 35, -10
        )

        mask = cv2.bitwise_or(mask_bright, mask_dark)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=2)

        return cv2.inpaint(img_actual, mask, 3, cv2.INPAINT_TELEA)

    def contiene_rostros(self, img: np.ndarray):
        """Función obsoleta, siempre devuelve False."""
        return False

    def comparar_lado_a_lado(self, original, restaurada):
        """Concatena imágenes horizontalmente para comparar."""
        return np.hstack((original, restaurada))

    # ---------------- RESTAURACIÓN COMPLETA ----------------

    def restaurar_completo(self, ruta_entrada: str, ruta_salida: str = "data/data-output/restaurada.jpeg"):
        """Cadena de restauración optimizada con filtros base."""
        img_original = cv2.imread(ruta_entrada)
        if img_original is None:
            raise ValueError(f"No se pudo cargar la imagen en {ruta_entrada}")

        print("🔧 Iniciando proceso de restauración (Filtros base)...")

        paso1 = self.reparar_manchas(img_original)
        paso2 = self.reducir_ruido(paso1)
        paso3 = self.corregir_color(paso2)
        paso4 = self.mejorar_contraste(paso3)
        resultado = self.enfocar_suave(paso4)

        print("ℹ️ Restauración finalizada. Funcionalidad avanzada fue deshabilitada.")

        ok = cv2.imwrite(ruta_salida, resultado)
        if ok:
            print(f"✅ Imagen final guardada en: {ruta_salida}")
        else:
            print(f"❌ No se pudo guardar en: {ruta_salida}")

        return resultado
    
    # --- Restauración personalizada (imagen en memoria) ---

    def restaurar_custom(self, img_original, aplicar_ruido=True, aplicar_contraste=True,
                             aplicar_manchas=True, aplicar_enfoque=True,
                             intensidad_enfoque=1.2):

        img = img_original.copy()

        if aplicar_manchas:
            img = self.reparar_manchas(img)
        if aplicar_ruido:
            img = self.reducir_ruido(img)
        if aplicar_contraste:
            img = self.mejorar_contraste(img)
        if aplicar_enfoque:
            img = self.enfocar_suave(img, amount=intensidad_enfoque)
        
        return img


# ---------------- BLOQUE DE PRUEBA(solo para probar el codigo) ----------------
if __name__ == "__main__":
    print("🚀 Probando restauración automática...")

    r = Restaurador()
    try:
        salida = "data/data-output/restaurada_plaza.jpg"
        restaurada = r.restaurar_completo("data/data-raw/plaza.jpg", salida)

        if cv2.imread(salida) is not None:
            print(f"🖼️ Imagen restaurada correctamente en {salida}")
        else:
            print("⚠️ No se pudo verificar la imagen restaurada.")

    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")