"""
Punto de entrada de la aplicación Streamlit.

Corre con:
    streamlit run app.py

Se encarga de:
- Inicializar la base de datos (crear tablas si no existen)
- Cargar los estilos CSS opcionales
- Decidir qué pantalla mostrar según st.session_state["pagina_actual"]
"""

import os
import streamlit as st

import config
from database.conexion import inicializar_bd
from frontend.login import mostrar_login
from frontend.home import mostrar_home
from frontend.leccion import mostrar_leccion
from frontend.perfil import mostrar_perfil


st.set_page_config(
    page_title="GESTUM",
    page_icon="🤟",
    layout="centered",
)


@st.cache_resource
def preparar_base_de_datos():
    """
    Se asegura de correr inicializar_bd() una sola vez por sesión del servidor
    (no en cada rerun de Streamlit), ya que crear las tablas es idempotente
    pero no hace falta repetirlo a cada clic.
    """
    inicializar_bd()
    return True


def cargar_estilos():
    """Inyecta el CSS opcional si el archivo existe."""
    ruta_css = os.path.join(config.CARPETA_BASE, "recursos", "estilos.css")
    if os.path.exists(ruta_css):
        with open(ruta_css, encoding="utf-8") as archivo:
            st.markdown(f"<style>{archivo.read()}</style>", unsafe_allow_html=True)


def mostrar_barra_lateral():
    """Dibuja la navegación lateral para un usuario ya autenticado."""
    usuario = st.session_state.get("usuario")

    with st.sidebar:
        st.markdown(f"### 👋 {usuario['nombre']}" if usuario else "### 👋")

        if st.button("🏠 Inicio", use_container_width=True):
            st.session_state["pagina_actual"] = "home"
            st.rerun()

        if st.button("👤 Mi perfil", use_container_width=True):
            st.session_state["pagina_actual"] = "perfil"
            st.rerun()

        st.divider()

        if st.button("Cerrar sesión", use_container_width=True):
            for clave in ("usuario", "usuario_id", "pagina_actual"):
                st.session_state.pop(clave, None)
            st.rerun()


def main():
    preparar_base_de_datos()
    cargar_estilos()

    usuario_id = st.session_state.get("usuario_id")

    # Si no hay sesión iniciada, siempre se muestra el login,
    # sin importar qué diga pagina_actual (por ejemplo, tras cerrar sesión).
    if usuario_id is None:
        st.session_state["pagina_actual"] = "login"
        mostrar_login()
        return

    mostrar_barra_lateral()

    pagina = st.session_state.get("pagina_actual", "home")

    if pagina == "leccion":
        mostrar_leccion()
    elif pagina == "perfil":
        mostrar_perfil()
    else:
        mostrar_home()


if __name__ == "__main__":
    main()