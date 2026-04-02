import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Reporte PVD 2026")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data.csv", sep=None, engine='python', encoding='utf-8')
    except:
        df = pd.read_csv("data.csv", sep=None, engine='python', encoding='latin-1')
    
    # Limpieza de nombres de columnas
    df.columns = df.columns.str.strip().str.upper()
    return df

try:
    df = load_data()
    st.title("📊 Control de Ejecución Presupuestal - PVD 2026")

    # --- BUSCADOR INTELIGENTE DE COLUMNAS ---
    # Esto busca las columnas aunque tengan otros nombres parecidos
    col_ff = next((c for c in df.columns if 'FF' in c or 'FUENTE' in c), None)
    col_gasto = next((c for c in df.columns if 'GASTO' in c or 'TIPO' in c), None)
    col_pim = next((c for c in df.columns if 'PIM' in c), None)
    col_dev = next((c for c in df.columns if 'DEV' in c), None)

    if col_ff and col_gasto:
        c1, c2 = st.columns(2)
        with c1:
            ff_sel = st.multiselect("Fuente de Financiamiento:", df[col_ff].unique(), default=df[col_ff].unique())
        with c2:
            gasto_sel = st.radio("Tipo de Gasto:", df[col_gasto].unique(), horizontal=True)

        # Filtrar
        df_f = df[(df[col_ff].isin(ff_sel)) & (df[col_gasto] == gasto_sel)].copy()

        # Asegurar que los montos sean números
        for c in [col_pim, col_dev]:
            if c: df_f[c] = pd.to_numeric(df_f[c], errors='coerce').fillna(0)

        # KPIs
        pim_val = df_f[col_pim].sum() if col_pim else 0
        dev_val = df_f[col_dev].sum() if col_dev else 0

        k1, k2 = st.columns(2)
        k1.metric("Presupuesto Total (PIM)", f"S/ {pim_val:,.2f}")
        k2.metric("Avance Devengado", f"{(dev_val/pim_val*100):.1f}%" if pim_val > 0 else "0%")

        # Gráfico Mensual
        prog_cols = [c for c in df.columns if 'PROG' in c]
        if prog_cols:
            sumas = [pd.to_numeric(df_f[c], errors='coerce').sum() for c in prog_cols]
            nombres = [c.replace("PROG.", "").strip() for c in prog_cols]
            fig = px.bar(x=nombres, y=sumas, title="Programación Mensual", labels={'x':'Mes', 'y':'S/'})
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.error(f"No encontré las columnas FF o GASTO. Columnas detectadas: {list(df.columns)}")

except Exception as e:
    st.error(f"Hubo un detalle: {e}")
