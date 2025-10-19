import os

# Entradas
entrada = "data/data-raw/imagenprueba.jpeg"
salida = "data/data-output"

print("Ruta entrada relativa:", entrada)
print("Ruta entrada absoluta:", os.path.abspath(entrada))
print("¿Existe entrada?", os.path.exists(entrada))

print("\nRuta salida relativa:", salida)
print("Ruta salida absoluta:", os.path.abspath(salida))
print("¿Existe salida?", os.path.exists(salida))

