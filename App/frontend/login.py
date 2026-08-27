"""
Pantalla de login y registro. Al iniciar sesión correctamente, guarda al
usuario completo en session_state para que el resto de la app (home,
lección, perfil) lo use sin volver a consultar la base de datos a cada rato.
"""

import streamlit as st

from database.usuarios import crear_usuario, verificar_login


def mostrar_login():
    """Dibuja la pantalla de login/registro con dos pestañas."""

    st.title("Aprendiendo LSM 🤟")
    st.caption("Practica el abecedario en Lengua de Señas Mexicana")

    tab_login, tab_registro = st.tabs(["Iniciar sesión", "Crear cuenta"])

    # ------------------------- Iniciar sesión -------------------------
    with tab_login:
        with st.form("form_login"):
            nombreUsuario = st.text_input("Nombre de usuario", key="login_usuario")
            contrasena = st.text_input("Contraseña", type="password", key="login_contrasena")
            enviar = st.form_submit_button("Entrar", use_container_width=True)

        if enviar:
            if not nombreUsuario or not contrasena:
                st.error("Completa usuario y contraseña.")
            else:
                usuario = verificar_login(nombreUsuario, contrasena)
                if usuario is None:
                    st.error("Usuario o contraseña incorrectos.")
                else:
                    st.session_state["usuario"] = dict(usuario)
                    st.session_state["usuario_id"] = usuario["id"]
                    st.session_state["pagina_actual"] = "home"
                    st.rerun()

    # ------------------------- Crear cuenta -------------------------
    with tab_registro:
        with st.form("form_registro"):
            nombre = st.text_input("Nombre")
            apellidoP = st.text_input("Apellido paterno")
            apellidoM = st.text_input("Apellido materno (opcional)")
            nombreUsuario_nuevo = st.text_input("Nombre de usuario", key="registro_usuario")
            edad = st.number_input("Edad", min_value=5, max_value=100, step=1, value=18)
            contrasena_nueva = st.text_input("Contraseña", type="password", key="registro_contrasena")
            crear = st.form_submit_button("Crear cuenta", use_container_width=True)

        if crear:
            if not nombre or not apellidoP or not nombreUsuario_nuevo or not contrasena_nueva:
                st.error("Completa al menos nombre, apellido paterno, usuario y contraseña.")
            else:
                ok, mensaje = crear_usuario(
                    nombre, apellidoP, apellidoM, nombreUsuario_nuevo, edad, contrasena_nueva
                )
                if ok:
                    st.success(f"{mensaje} Ya puedes iniciar sesión en la otra pestaña.")
                else:
                    st.error(mensaje)