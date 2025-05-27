import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Generador de muestras - Departamento de Estadísticas", layout="centered")

st.title("📊 Generador de muestras aleatorias representativas")

# Texto institucional
st.markdown(
    "Esta herramienta fue desarrollada por el **Departamento de Estadísticas** para facilitar la generación de muestras aleatorias representativas. "
    "El tamaño de la muestra se calcula automáticamente utilizando un **95% de nivel de confianza** y un **5% de margen de error**, "
    "criterios metodológicos ampliamente aceptados y consistentes con los utilizados en muestras previas del organismo. "
    "El cálculo asume una proporción esperada de máxima variabilidad (p = 0.5).",
    unsafe_allow_html=True
)

st.markdown("---")
st.subheader("1. Ingresar el tamaño de la población")

N = st.number_input("Tamaño total de la población", min_value=1, step=1)

if N:
    st.markdown("---")
    st.subheader("2. Generar muestra")

    if st.button("Generar muestra"):
        # Parámetros fijos
        Z = 1.96
        e = 0.05
        p = 0.5

        # Cálculo muestral con corrección por población finita
        n_0 = (Z**2 * p * (1 - p)) / (e**2)
        n = round((N * n_0) / (n_0 + N - 1))

        if n > N:
            st.error("El tamaño calculado de la muestra es mayor que la población.")
        else:
            st.success(f"Se generaron correctamente {n} casos únicos.")

            rng = np.random.default_rng()
            muestra = rng.choice(np.arange(1, N + 1), size=n, replace=False)
            muestra.sort()

            df_muestra = pd.DataFrame(
                muestra,
                columns=["Caso seleccionado"],
                index=np.arange(1, len(muestra) + 1)
            )

            st.markdown("---")
            st.subheader("3. Descargar o copiar la muestra")

            # Ver primeros 10 casos
            if st.checkbox("Ver los primeros 10 casos generados"):
                st.dataframe(df_muestra.head(10), use_container_width=True)

            # Descargar solo la muestra
            csv = df_muestra.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descargar muestra en CSV",
                data=csv,
                file_name="muestra_aleatoria.csv",
                mime="text/csv"
            )

            # Copiar listado
            muestra_txt = ", ".join(str(i) for i in muestra)
            st.text_area("Copiar al portapapeles", muestra_txt, height=100)

            # Crear columna con todo el universo y (x) marcando la muestra
            todos = pd.DataFrame({
                "Columna para Excel": [f"{i} (x)" if i in muestra else str(i) for i in range(1, N + 1)]
            })

            # Descargar columna con marcados
            csv_todos = todos.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descargar columna para Excel con marcados (x)",
                data=csv_todos,
                file_name="muestra_con_marcados.csv",
                mime="text/csv"
            )
