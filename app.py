import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Generador de muestras - Departamento de Estadísticas", layout="centered")

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
            st.success(f"Se generaron correctamente {n} casos únicos.")

    muestra = st.session_state.get("muestra_generada")

    if muestra is not None:
        df_muestra = pd.DataFrame(
            muestra,
            columns=["Caso seleccionado"],
            index=np.arange(1, len(muestra) + 1)
        )

        st.markdown("---")
        st.subheader("3. Descargar o copiar la muestra")

        if st.checkbox("Ver los primeros 10 casos generados"):
            st.dataframe(df_muestra.head(10), use_container_width=True)

        csv = df_muestra.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar muestra",
            data=csv,
            file_name="muestra.csv",
            mime="text/csv"
        )

        todos = pd.DataFrame({
            "Población con marca": [
                f"{i} muestra" if i in muestra else str(i)
                for i in range(1, N + 1)
            ]
        })

        csv_todos = todos.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar población con muestra marcada",
            data=csv_todos,
            file_name="poblacion_con_muestra.csv",
            mime="text/csv"
        )

        st.markdown("---")
        st.subheader("Casos de la muestra")
        muestra_txt = ", ".join(str(i) for i in muestra)
        st.text_area("Casos de la muestra", muestra_txt, height=100)
