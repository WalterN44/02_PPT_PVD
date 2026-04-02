import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de página
st.set_page_config(layout="wide", page_title="Reporte PVD 2026")

@st.cache_data
def load_data():
    # Intentamos leer con coma, si falla probamos con punto y coma
    try:
        df = pd.read_csv("data.csv", sep=None, engine='python', encoding='utf-8')
    except:
        df = pd.read_csv("data.csv", sep=',', encoding='latin-1')
    
    # ESTO ES LO MÁS IMPORTANTE: Limpia espacios en blanco en los nombres de las columnas
    df.columns = df.columns.str.strip()
    return df

try:
    df = load_data()

    st.title("📊 Dashboard de Ejecución Presupuestal 2026")

    # --- FILTROS ---
    # Usamos .get() o verificamos si la columna existe para evitar el error que te salió
    if 'FF' in df.columns and 'GASTO' in df.columns:
        col1, col2 = st.columns(2)
        with col1:
            ff_options = df['FF'].unique()
            ff_selected = st.multiselect("Fuente de Financiamiento (FF):", options=ff_options, default=ff_options)
        with col2:
            gasto_options = df['GASTO'].unique()
            gasto_selected = st.radio("Tipo de Gasto:", options=gasto_options, horizontal=True)

        # Filtrado
        df_filtered = df[(df['FF'].isin(ff_selected)) & (df['GASTO'] == gasto_selected)]

        # --- KPIs ---
        # Aseguramos que los nombres coincidan con tu Excel
        pim = df_filtered['PIM'].sum()
        dev = df_filtered['DEVENGADO'].sum()
        cert = df_filtered['CERTIFICADO'].sum()
        comp = df_filtered['COMPROMISO'].sum()

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("PIM Total", f"S/ {pim:,.2f}")
        k2.metric("Devengado/PIM", f"{(dev/pim)*100:.1f}%" if pim > 0 else "0%")
        k3.metric("Certificado/PIM", f"{(cert/pim)*100:.1f}%" if pim > 0 else "0%")
        k4.metric("Compromiso/PIM", f"{(comp/pim)*100:.1f}%" if pim > 0 else "0%")

        # --- GRÁFICO ---
        meses = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SETIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
        prog_cols = [f"PROG. {m}" for m in meses]
        
        # Verificar cuáles de estas columnas existen realmente en el CSV
        prog_cols_present = [c for c in prog_cols if c in df_filtered.columns]
        
        if prog_cols_present:
            valores_mes = [df_filtered[c].sum() for c in prog_cols_present]
            df_grafico = pd.DataFrame({"Mes": [c.replace("PROG. ", "") for c in prog_cols_present], "Monto": valores_mes})
            
            fig = px.bar(df_grafico, x="Mes", y="Monto", title="Programación por Mes", color_discrete_sequence=['#0083B8'])
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.error(f"No encontré las columnas 'FF' o 'GASTO'. Columnas detectadas: {list(df.columns)}")

except Exception as e:
    st.error(f"Ocurrió un error: {e}")
