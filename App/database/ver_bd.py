"""
Script utilitario para revisar rápidamente el contenido de la base de datos
desde la consola, sin necesidad de instalar un visor externo.

Cómo se usa (parado en la raíz del proyecto, con el venv activado):
    python App/ver_bd.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from database.conexion import obtener_conexion


def mostrar_tabla(cursor, nombre_tabla):
    print(f"\n{'=' * 50}")
    print(f"Tabla: {nombre_tabla}")
    print("=" * 50)

    cursor.execute(f"SELECT * FROM {nombre_tabla}")
    filas = cursor.fetchall()

    if not filas:
        print("(vacía)")
        return

    columnas = filas[0].keys()
    print(" | ".join(columnas))

    for fila in filas:
        print(" | ".join(str(fila[col]) for col in columnas))


def main():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    for tabla in ["usuario", "letras", "intentos", "progreso"]:
        mostrar_tabla(cursor, tabla)

    conexion.close()


if __name__ == "__main__":
    main()