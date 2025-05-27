import streamlit as st
import numpy as np
import pandas as pd
import math

st.set_page_config(page_title="Generador de muestras - Departamento de Estadísticas", layout="centered")

st.title("📊 Generador de muestras aleatorias representativas")

# 🔹 Aclaración institucional
st.markdown(
    "El tamaño de la muestra se calcula automáticamente en base a un **95% de nivel de confianza** "
    "y un **5% de margen de error**, bajo el supuesto de máxima variabilidad (p = 0.5).",
    unsafe_allow_html=True
)

# Paso 1: Ingreso del tamaño de población
N = st.number_input("Tamaño total de la población", min_value=1, step=1)

if N:
    # Parámetros fijos
    Z = 1.96  # 95% de confianza
    e = 0.05  # margen de error
    p = 0.5   # proporción esperada

    # Cálculo del tamaño de la muestra con corrección para población finita
    n_0 = (Z**2 * p * (1 - p)) / (e**2)
    n = round((N * n_0) / (n_0 + N - 1))

    st.markdown(f"### Tamaño muestral requerido: <span style='color:green;font-weight:bold'>{n}</span> casos", unsafe_allow_html=True)

    if n > N:
        st.error("⚠️ La muestra calculada es mayor que la población.")
    else:
        # Generar la muestra
        rng = np.random.default_rng()
        muestra = rng.choice(np.arange(1, N + 1), size=n, replace=False)
        muestra.sort()

        df_muestra = pd.DataFrame(
            muestra,
            columns=["Caso seleccionado"],
            index=np.arange(1, len(muestra) + 1)
        )

        # Confirmación
        st.success(f"🎉 Se generaron correctamente {n} casos únicos.")

        # Mostrar muestra parcial
        if st.checkbox("Ver los primeros 10 casos generados"):
            st.dataframe(df_muestra.head(10), use_container_width=True)

        # Descargar CSV
        csv = df_muestra.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar muestra en CSV",
            data=csv,
            file_name="muestra_aleatoria.csv",
            mime="text/csv"
        )
