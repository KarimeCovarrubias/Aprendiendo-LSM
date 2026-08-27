"""
Pantalla principal (home): muestra un resumen del usuario (racha, XP) y
la cuadrícula de letras disponibles para practicar, cada una como tarjeta
con su porcentaje de acierto si ya se practicó antes.
"""

import streamlit as st

import config
from database.progreso import obtener_progreso_usuario
from componentes.tarjeta_letra import mostrar_tarjeta_letra

UMBRAL_COMPLETADA = 80  # % de acierto a partir del cual se marca la letra como "completada"


def _ir_a_leccion(letra):
    """Prepara el estado para abrir la lección de una letra específica y navega ahí."""
    indice = config.LETRAS_DISPONIBLES.index(letra)
    st.session_state["letra_objetivo"] = letra
    st.session_state["indice_letra"] = indice
    st.session_state["pagina_actual"] = "leccion"
    st.rerun()


def mostrar_home():
    """Dibuja la pantalla principal con el resumen del usuario y las letras."""

    usuario = st.session_state.get("usuario")
    usuario_id = st.session_state.get("usuario_id")

    if usuario_id is None:
        st.warning("Inicia sesión para ver tu progreso.")
        return

    # --- Encabezado ---
    col_titulo, col_logout = st.columns([4, 1])
    with col_titulo:
        st.subheader(f"Hola, {usuario['nombre']} 👋" if usuario else "Hola 👋")
    with col_logout:
        if st.button("Salir"):
            for clave in ("usuario", "usuario_id", "pagina_actual"):
                st.session_state.pop(clave, None)
            st.rerun()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Racha", f"{usuario['racha_actual']} 🔥" if usuario else "0 🔥")
    with col2:
        st.metric("XP", f"{usuario['puntos_xp']} ⭐" if usuario else "0 ⭐")

    st.divider()

    # --- Cuadrícula de letras ---
    st.markdown("### Elige una letra para practicar")

    progreso = obtener_progreso_usuario(usuario_id)
    progreso_por_letra = {fila["letra"]: fila for fila in progreso}

    columnas = st.columns(4)

    for i, letra in enumerate(config.LETRAS_DISPONIBLES):
        datos_letra = progreso_por_letra.get(letra)
        porcentaje = datos_letra["porcentaje_acierto"] if datos_letra else None
        estado = "completada" if (porcentaje is not None and porcentaje >= UMBRAL_COMPLETADA) else "disponible"

        with columnas[i % 4]:
            mostrar_tarjeta_letra(letra, estado=estado, porcentaje_acierto=porcentaje, on_click=_ir_a_leccion)

    st.divider()

    if st.button("Ver mi perfil completo"):
        st.session_state["pagina_actual"] = "perfil"
        st.rerun()