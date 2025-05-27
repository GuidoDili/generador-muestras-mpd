import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Generador de muestras - Departamento de Estadísticas", layout="centered")

# ✅ Logo institucional centrado
st.markdown(
    "<div style='text-align: center;'>"
    "<img src='https://raw.githubusercontent.com/GuidoDili/generador-muestras-mpd/main/logo_mpd.png' width='250'>"
    "</div>",
    unsafe_allow_html=True
)

st.title("📊 Generador de muestras aleatorias representativas")

st.markdown(
    "Esta herramienta fue desarrollada por el **Departamento de Estadísticas** para facilitar la generación de muestras aleatorias representativas. "
    "El tamaño de la muestra se calcula automáticamente utilizando un **95% de nivel de confianza** y un **5% de margen de error**, "
    "criterios metodológicos sólidos y alineados con los empleados en diseños muestrales previos. "
    "El cálculo asume una proporción esperada de máxima variabilidad (p = 0.5).",
    unsafe_allow_html=True
)

st.markdown("---")
st.subheader("1. Ingresar el tamaño de la población")

N = st.number_input("Tamaño total de la población", min_value=1, step=1)

# ✅ Reiniciar la muestra si cambia la población
if "poblacion_anterior" not in st.session_state:
    st.session_state["poblacion_anterior"] = N
elif st.session_state["poblacion_anterior"] != N:
    st.session_state["poblacion_anterior"] = N
    st.session_state["muestra_generada"] = None

if "muestra_generada" not in st.session_state:
    st.session_state["muestra_generada"] = None

if N:
    st.markdown("---")
    st.subheader("2. Generar muestra")

    if st.button("Generar muestra"):
        Z = 1.96
        e = 0.05
        p = 0.5

        n_0 = (Z**2 * p * (1 - p)) / (e**2)
        n = round((N * n_0) / (n_0 + N - 1))

        if n > N:
            st.error("El tamaño calculado de la muestra es mayor que la población.")
        else:
            rng = np.random.default_rng()
            muestra = rng.choice(np.arange(1, N + 1), size=n, replace=False)
            muestra.sort()
            st.session_state["muestra_generada"] = muestra

    muestra = st.session_state.get("muestra_generada")

    if muestra is not None:
        df_muestra = pd.DataFrame(
            muestra,
            columns=["Caso seleccionado"],
            index=np.arange(1, len(muestra) + 1)
        )

        # ✅ Tamaño muestral destacado y centrado
        st.markdown(
            f"<div style='text-align:center; font-size:26px;'>Tamaño muestral requerido: "
            f"<span style='color:green; font-weight:bold;'>{len(muestra)} casos</span></div>",
            unsafe_allow_html=True
        )

        st.markdown("---")
        st.subheader("3. Descargar la muestra o el listado completo")

        # Botón: descargar muestra
        csv = df_muestra.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar muestra",
            data=csv,
            file_name="muestra.csv",
            mime="text/csv"
        )

        # Botón: descargar población completa con "muestra" marcado
        todos = pd.DataFrame({
            "Listado con muestra": [
                f"{i} muestra" if i in muestra else str(i)
                for i in range(1, N + 1)
            ]
        })

        csv_todos = todos.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar listado completo con muestra marcada",
            data=csv_todos,
            file_name="listado_completo_con_muestra.csv",
            mime="text/csv"
        )

        st.markdown("---")
        st.subheader("Casos de la muestra")

        muestra_txt = ", ".join(str(i) for i in muestra)
        st.text_area("", muestra_txt, height=100)
