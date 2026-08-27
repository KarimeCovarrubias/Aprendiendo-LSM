import streamlit as st

st.progress(0.35)
col1, col2 = st.columns([1, 3])
with col1:
    st.metric("Racha", "5 🔥")

st.image("recursos/imagenes_letras/A.png", width=120)
st.subheader("Letra A")

# Aquí va el bloque de cámara (streamlit-webrtc)
webrtc_streamer(key="camara", video_frame_callback=procesar_frame)

col1, col2 = st.columns(2)
with col1:
    st.button("Repetir")
with col2:
    st.button("Siguiente →")