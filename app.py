import streamlit as st
import numpy as np
import pandas as pd
import math

st.title("Generador de muestras aleatorias representativas")

# Paso 1: Ingreso del tamaño de población
N = st.number_input("Tamaño total de la población", min_value=1, step=1)

if N:
    # Paso 2: Parámetros fijos
    Z = 1.96  # 95% de confianza
    e = 0.05  # margen de error
    p = 0.5   # proporción esperada (máxima variabilidad)

    # Paso 3: Cálculo del tamaño de la muestra con corrección para población finita
    n_0 = (Z**2 * p * (1 - p)) / (e**2)
    n = round((N * n_0) / (n_0 + N - 1))

    st.markdown(f"### Tamaño muestral requerido: `{n}` casos")

    if n > N:
        st.error("La muestra calculada es mayor que la población. Revisa los parámetros.")
    else:
        # Paso 4: Generar la muestra
        rng = np.random.default_rng()
        muestra = rng.choice(np.arange(1, N + 1), size=n, replace=False)
        muestra.sort()

        df_muestra = pd.DataFrame(muestra, columns=["Caso seleccionado"])

        # Mostrar muestra
        st.dataframe(df_muestra)

        # Descargar como CSV
        csv = df_muestra.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar muestra en CSV",
            data=csv,
            file_name="muestra_aleatoria.csv",
            mime="text/csv"
        )
