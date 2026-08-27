"""
Pantalla de lección: muestra la letra objetivo, la cámara en vivo con
feedback de correcto/incorrecto, y guarda cada intento en la base de datos.
"""

import os
import streamlit as st

import config
from database.progreso import registrar_intento
from database.usuarios import actualizar_racha_y_xp
from componentes.camara import mostrar_camara


def mostrar_leccion():
    """Dibuja la pantalla completa de práctica de una letra."""

    # --- Estado de la lección (persiste entre reruns de Streamlit) ---
    if "letra_objetivo" not in st.session_state:
        st.session_state["letra_objetivo"] = config.LETRAS_DISPONIBLES[0]
    if "indice_letra" not in st.session_state:
        st.session_state["indice_letra"] = 0
    if "ultimo_resultado" not in st.session_state:
        st.session_state["ultimo_resultado"] = None

    letra_objetivo = st.session_state["letra_objetivo"]
    usuario_id = st.session_state.get("usuario_id")

    # --- Encabezado: progreso dentro de la lección + racha ---
    total_letras = len(config.LETRAS_DISPONIBLES)
    avance = (st.session_state["indice_letra"] + 1) / total_letras
    st.progress(avance)

    col1, col2 = st.columns([1, 3])
    with col1:
        racha = st.session_state.get("racha_actual", 0)
        st.metric("Racha", f"{racha} 🔥")

    # --- Imagen de referencia de la letra ---
    ruta_imagen = os.path.join(config.CARPETA_IMAGENES_LETRAS, f"{letra_objetivo}.png")
    if os.path.exists(ruta_imagen):
        st.image(ruta_imagen, width=120)
    else:
        st.info(f"Falta la imagen de referencia para la letra '{letra_objetivo}'.")

    st.subheader(f"Letra {letra_objetivo}")

    # --- Bloque de cámara con feedback en vivo ---
    mostrar_camara(letra_objetivo)

    # --- Registrar el intento más reciente detectado por la cámara ---
    if st.session_state["ultimo_resultado"] is not None and usuario_id is not None:
        registrar_intento(usuario_id, letra_objetivo, st.session_state["ultimo_resultado"])
        st.session_state["ultimo_resultado"] = None  # evita registrar el mismo intento dos veces

    # --- Botones de navegación ---
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Repetir"):
            st.rerun()

    with col2:
        if st.button("Siguiente →"):
            if usuario_id is not None:
                actualizar_racha_y_xp(usuario_id, xp_ganado=config.XP_POR_INTENTO_CORRECTO)

            siguiente_indice = st.session_state["indice_letra"] + 1
            if siguiente_indice < total_letras:
                st.session_state["indice_letra"] = siguiente_indice
                st.session_state["letra_objetivo"] = config.LETRAS_DISPONIBLES[siguiente_indice]
                st.rerun()
            else:
                st.success("¡Completaste todas las letras disponibles!")