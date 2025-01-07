# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 13:14:53 2025

@author: jperezr
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Estilo de fondo
page_bg_img = """
<style>
[data-testid="stAppViewContainer"]{
background:
radial-gradient(black 15%, transparent 16%) 0 0,
radial-gradient(black 15%, transparent 16%) 8px 8px,
radial-gradient(rgba(255,255,255,.1) 15%, transparent 20%) 0 1px,
radial-gradient(rgba(255,255,255,.1) 15%, transparent 20%) 8px 9px;
background-color:#282828;
background-size:16px 16px;
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

# Tasa de rendimiento anual y mensual
tasa_rendimiento_anual = 0.05
tasa_rendimiento_mensual = tasa_rendimiento_anual / 12

# Función para calcular el fondo total con los aportes y rendimiento durante la actividad y la inactividad
def calcular_fondo_con_inactividad(meses_actividad, meses_inactividad, aporte_mensual):
    fondo = 0
    for mes in range(meses_actividad):
        fondo += aporte_mensual
        fondo *= (1 + tasa_rendimiento_mensual)
    for mes in range(meses_inactividad):
        fondo += aporte_mensual
        fondo *= (1 + tasa_rendimiento_mensual)
    return fondo

# Función para calcular el fondo sin aportes durante la inactividad
def calcular_fondo_sin_aporte_inactividad(meses_actividad, meses_inactividad, aporte_mensual):
    fondo = 0
    for mes in range(meses_actividad):
        fondo += aporte_mensual
        fondo *= (1 + tasa_rendimiento_mensual)
    for mes in range(meses_inactividad):
        fondo *= (1 + tasa_rendimiento_mensual)
    return fondo

# Sidebar: Ayuda
st.sidebar.title("Ayuda")
st.sidebar.write("""
Esta aplicación permite simular cómo se acumula el fondo de pensión considerando:
- Aportes mensuales realizados durante la actividad laboral.
- Impacto de los meses de inactividad en el fondo acumulado, con o sin aportes.

### Explicación:
1. **Con Aportes Durante Inactividad**:
   El fondo sigue creciendo durante la inactividad debido a los aportes mensuales y el rendimiento compuesto.

2. **Sin Aportes Durante Inactividad**:
   El fondo solo crece por el rendimiento compuesto, sin contribuciones adicionales durante los meses de inactividad.

### Importancia de Mantenerse Activo:
- Al estar activo el mayor tiempo posible, el trabajador no solo asegura sus aportes mensuales al AFORE, sino que también permite que estos aportes sean administrados en inversiones que generan rendimientos adicionales.
- Durante los meses de inactividad, no se realizan nuevos aportes al AFORE, lo que limita el crecimiento del fondo a los rendimientos generados por el saldo acumulado hasta ese momento.

### Diferencias:
- Se muestra el dinero no percibido cuando no se realizan aportes durante la inactividad.
- También puedes observar cuánto varía el fondo entre escenarios de inactividad de m y n meses.

¡Asegúrate de mantener aportes constantes y reducir los periodos de inactividad para maximizar tu fondo acumulado!

### Desarrollado por:
- Javier Horacio Pérez Ricárdez    
""")

# Inputs de usuario
st.title("Simulación de Aportes y Rendimiento de Pensión")
aporte_mensual = st.number_input("Introduce el aporte mensual en MXN:", min_value=1, value=1000)
meses_actividad = st.number_input("Introduce los meses de actividad laboral:", min_value=1, value=240)
meses_inactividad_1 = st.number_input("Introduce los meses de inactividad laboral (comparativa 1):", min_value=1, value=30)
meses_inactividad_2 = st.number_input("Introduce los meses de inactividad laboral (comparativa 2):", min_value=1, value=60)

# Cálculos
fondo_con_inactividad_1 = calcular_fondo_con_inactividad(meses_actividad, meses_inactividad_1, aporte_mensual)
fondo_con_inactividad_2 = calcular_fondo_con_inactividad(meses_actividad, meses_inactividad_2, aporte_mensual)
fondo_sin_inactividad_1 = calcular_fondo_sin_aporte_inactividad(meses_actividad, meses_inactividad_1, aporte_mensual)
fondo_sin_inactividad_2 = calcular_fondo_sin_aporte_inactividad(meses_actividad, meses_inactividad_2, aporte_mensual)

# Diferencias
diferencia_con_aporte = fondo_con_inactividad_2 - fondo_con_inactividad_1
diferencia_sin_aporte = fondo_sin_inactividad_2 - fondo_sin_inactividad_1
dinero_no_percibido_1 = fondo_con_inactividad_1 - fondo_sin_inactividad_1
dinero_no_percibido_2 = fondo_con_inactividad_2 - fondo_sin_inactividad_2

# Resultados
st.write(f"1.- Con una tasa de rendimiento anual de 5.0%, tu fondo total al final de los {meses_actividad + meses_inactividad_1} meses será:")
st.write(f"Con Aportes Durante Inactividad ({meses_inactividad_1} meses): ${fondo_con_inactividad_1:,.2f} MXN.")
st.write(f"Sin Aportes Durante Inactividad ({meses_inactividad_1} meses): ${fondo_sin_inactividad_1:,.2f} MXN.")
st.write(f"Diferencia (dinero no percibido) por no aportar durante {meses_inactividad_1} meses de inactividad: ${dinero_no_percibido_1:,.2f} MXN.")

st.write(f"2.- Con una tasa de rendimiento anual de 5.0%, tu fondo total al final de los {meses_actividad + meses_inactividad_2} meses será:")
st.write(f"Con Aportes Durante Inactividad ({meses_inactividad_2} meses): ${fondo_con_inactividad_2:,.2f} MXN.")
st.write(f"Sin Aportes Durante Inactividad ({meses_inactividad_2} meses): ${fondo_sin_inactividad_2:,.2f} MXN.")
st.write(f"Diferencia (dinero no percibido) por no aportar durante {meses_inactividad_2} meses de inactividad: ${dinero_no_percibido_2:,.2f} MXN.")

# Resumen de diferencias totales
st.write(f"Diferencia total entre fondos con aportes para {meses_inactividad_1} y {meses_inactividad_2} meses de inactividad: ${diferencia_con_aporte:,.2f} MXN.")
st.write(f"Diferencia total entre fondos sin aportes para {meses_inactividad_1} y {meses_inactividad_2} meses de inactividad: ${diferencia_sin_aporte:,.2f} MXN.")

# Gráficos
labels = [
    f'Con Aportes ({meses_inactividad_1} meses)',
    f'Sin Aportes ({meses_inactividad_1} meses)',
    f'Con Aportes ({meses_inactividad_2} meses)',
    f'Sin Aportes ({meses_inactividad_2} meses)'
]
fondos = [fondo_con_inactividad_1, fondo_sin_inactividad_1, fondo_con_inactividad_2, fondo_sin_inactividad_2]

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(labels, fondos, color=['blue', 'green', 'orange', 'red'], alpha=0.7)
ax.set_ylabel('Fondo Acumulado en MXN')
ax.set_title('Comparación de Fondos Acumulados con y sin Aportes Durante Inactividad')
plt.xticks(rotation=90)
st.pyplot(fig)
