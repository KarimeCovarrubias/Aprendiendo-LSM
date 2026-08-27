"""
Configuración centralizada del proyecto: rutas de archivos y constantes
que se usan en varios módulos. Si algo se mueve de carpeta o cambia de
valor, se ajusta aquí en un solo lugar.
"""

import os

# Carpeta raíz de la app (donde vive este archivo: App/)
CARPETA_BASE = os.path.dirname(os.path.abspath(__file__))

# ------------------------- Rutas de datos -------------------------

RUTA_BD = os.path.join(CARPETA_BASE, "datos", "usuarios.db")
RUTA_DATASET = os.path.join(CARPETA_BASE, "datos", "dataset_letras.csv")
RUTA_MODELO = os.path.join(CARPETA_BASE, "modelo", "modelo_entrenado.pkl")
CARPETA_IMAGENES_LETRAS = os.path.join(CARPETA_BASE, "recursos", "imagenes_letras")

# ------------------------- Parámetros de la app -------------------------

XP_POR_INTENTO_CORRECTO = 10
MUESTRAS_POR_RAFAGA = 60          # usado en recolectar_datos.py
RETARDO_ENTRE_MUESTRAS = 0.03     # segundos, usado en recolectar_datos.py

# Letras disponibles para practicar (se va ampliando conforme grabes más datos)
LETRAS_DISPONIBLES = ["A", "B", "C", "D", "E"]

# Umbral mínimo de confianza del modelo para aceptar una predicción
# (útil si más adelante cambias a un modelo que entregue probabilidades)
UMBRAL_CONFIANZA = 0.6