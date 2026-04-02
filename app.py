import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de página
st.set_page_config(layout="wide", page_title="Reporte PVD 2026")

@st.cache_data
def load_data():
    # Esta configuración detecta automáticamente si usas coma (,) o punto y coma (;)
    try:
        df = pd.read_csv("data.csv", sep=None, engine='python', encoding='utf-8')
    except Exception:
        # Si falla por caracteres especiales (tildes), intenta con este formato:
        df = pd.read_csv("data.csv", sep=None, engine='python', encoding='latin-1')
    
    # Limpieza de espacios en los nombres de las columnas
    df.columns = df.columns.str.strip()
    return df

try:
    df = load_data()

    st.title("📊 Dashboard de Ejecución Presupuestal 2026")

    # --- FILTROS ---
    # Verificamos que las columnas existan
    columnas = list(df.columns)
    
    if 'FF' in columnas and 'GASTO' in columnas:
        col1, col2 = st.columns(2)
        with col1:
            fuentes = df['FF'].unique()
            ff_sel = st.multiselect("Fuente de Financiamiento (FF):", options=fuentes, default=fuentes)
        with col2:
            gastos = df['GASTO'].unique()
            gasto_sel = st.radio("Tipo de Gasto:", options=gastos, horizontal=True)

        # Aplicar filtros
        df_f = df[(df['FF'].isin(ff_sel)) & (df['GASTO'] == gasto_sel)]

        # --- KPIs ---
        # Usamos nombres exactos de tu archivo
        pim = df_f['PIM'].sum()
        dev = df_f['DEVENGADO'].sum()
        cert = df_f['CERTIFICADO'].sum()
        comp = df_f['COMPROMISO'].sum()

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("PIM Total", f"S/ {pim:,.2f}")
        m2.metric("Devengado/PIM", f"{(dev/pim)*100:.1f}%" if pim > 0 else "0%")
        m3.metric("Certificado/PIM", f"{(cert/pim)*100:.1f}%" if pim > 0 else "0%")
        m4.metric("Compromiso/PIM", f"{(comp/pim)*100:.1f}%" if pim > 0 else "0%")

        st.divider()

        # --- GRÁFICO DE BARRAS ---
        meses = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SETIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
        # Creamos la lista de columnas de programación que sí existen en el archivo
        prog_cols = [f"PROG. {m}" for m in meses if f"PROG. {m}" in columnas]

        if prog_cols:
            valores = [df_f[c].sum() for c in prog_cols]
            nombres_meses = [c.replace("PROG. ", "") for c in prog_cols]
            
            df_barras = pd.DataFrame({"Mes": nombres_meses, "Monto": valores})
            fig = px.bar(df_barras, x="Mes", y="Monto", title=f"Programación Mensual: {gasto_sel}", 
                         color_discrete_sequence=['#00D4FF'], text_auto='.2s')
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"Revisa los títulos de tu Excel. Columnas encontradas: {columnas}")

except Exception as e:
    st.error(f"Error crítico: {e}")
