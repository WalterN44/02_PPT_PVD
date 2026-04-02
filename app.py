import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Dashboard PVD 2026")

# Carga de datos
@st.cache_data
def load_data():
    # Buscamos el archivo llamado data.csv
    df = pd.read_csv("data.csv")
    df.columns = df.columns.str.strip() # Limpia espacios en los nombres
    return df

try:
    df = load_data()

    st.title("📊 Control Presupuestal PVD 2026")

    # --- FILTROS ---
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        fuente = st.multiselect("Fuente de Financiamiento (FF):", options=df['FF'].unique(), default=df['FF'].unique())
    with col_f2:
        tipo_gasto = st.radio("Tipo de Gasto:", options=df['GASTO'].unique(), horizontal=True)

    # Filtrar Data
    df_filtrada = df[(df['FF'].isin(fuente)) & (df['GASTO'] == tipo_gasto)]

    # --- KPIs ---
    pim = df_filtrada['PIM'].sum()
    dev = df_filtrada['DEVENGADO'].sum()
    cert = df_filtrada['CERTIFICADO'].sum()
    comp = df_filtrada['COMPROMISO'].sum()

    k1, k2, k3 = st.columns(3)
    k1.metric("Ejecución (Devengado/PIM)", f"{(dev/pim)*100:.2f}%" if pim > 0 else "0%")
    k2.metric("Certificación (Certif./PIM)", f"{(cert/pim)*100:.2f}%" if pim > 0 else "0%")
    k3.metric("Compromiso (Compro./PIM)", f"{(comp/pim)*100:.2f}%" if pim > 0 else "0%")

    # --- GRÁFICO DE BARRAS MENSUAL ---
    meses = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SETIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
    # Buscamos las columnas que empiezan con PROG.
    prog_cols = [f"PROG. {m}" for m in meses]
    valores_mes = [df_filtrada[c].sum() for c in prog_cols]

    df_barras = pd.DataFrame({"Mes": meses, "Presupuesto Programado": valores_mes})
    
    fig = px.bar(df_barras, x="Mes", y="Presupuesto Programado", 
                 title=f"Programación Mensual - {tipo_gasto}",
                 color_discrete_sequence=["#00CC96"])
    
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Error al cargar datos: {e}")
    st.info("Asegúrate de que el archivo de Excel se llame 'data.csv' en GitHub.")
