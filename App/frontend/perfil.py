"""
Pantalla de perfil: muestra los datos del usuario (racha, XP) y su
progreso detallado por letra, usando la información de la base de datos.
"""

import streamlit as st
import pandas as pd

from database.progreso import obtener_progreso_usuario


def mostrar_perfil():
    """Dibuja la pantalla completa de perfil del usuario."""

    usuario = st.session_state.get("usuario")
    usuario_id = st.session_state.get("usuario_id")

    if usuario_id is None:
        st.warning("Inicia sesión para ver tu perfil.")
        return

    # --- Encabezado con datos del usuario ---
    nombre_completo = f"{usuario['nombre']} {usuario['apellidoP']}" if usuario else "Usuario"
    st.subheader(nombre_completo)
    st.caption(f"@{usuario['nombreUsuario']}" if usuario else "")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Racha actual", f"{usuario['racha_actual']} 🔥" if usuario else "0 🔥")
    with col2:
        st.metric("Racha máxima", f"{usuario['racha_maxima']} 🏆" if usuario else "0 🏆")
    with col3:
        st.metric("XP total", f"{usuario['puntos_xp']} ⭐" if usuario else "0 ⭐")

    st.divider()

    # --- Progreso por letra ---
    st.markdown("### Progreso por letra")

    progreso = obtener_progreso_usuario(usuario_id)

    if not progreso:
        st.info("Todavía no has practicado ninguna letra. ¡Empieza una lección!")
        return

    tabla = pd.DataFrame(progreso)
    tabla = tabla.rename(columns={
        "letra": "Letra",
        "veces_practicadas": "Veces practicada",
        "veces_correctas": "Aciertos",
        "porcentaje_acierto": "% de acierto",
    })

    st.dataframe(tabla, hide_index=True, width="stretch")

    # --- Gráfica simple de porcentaje de acierto por letra ---
    st.markdown("### Porcentaje de acierto por letra")
    grafica = pd.DataFrame(progreso).set_index("letra")["porcentaje_acierto"]
    st.bar_chart(grafica)