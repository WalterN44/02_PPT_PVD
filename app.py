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
    
    # 1. Limpiar nombres de columnas
    df.columns = df.columns.str.strip().str.upper()

    # 2. FUNCIÓN PARA LIMPIAR DINERO: Quita S/, comas y espacios
    def clean_currency(value):
        if isinstance(value, str):
            value = value.replace('S/', '').replace('$', '').replace(',', '').strip()
            # Si el Excel usa coma para decimales, la cambiamos por punto
            if len(value) > 3 and value[-3] == ',':
                value = value.replace('.', '').replace(',', '.')
        return pd.to_numeric(value, errors='coerce')

    # Aplicamos la limpieza a todas las columnas que deberían ser números
    for col in df.columns:
        if any(x in col for x in ['PIM', 'DEV', 'CERT', 'COMP', 'PROG', 'TOTAL', 'SALDO']):
            df[col] = df[col].apply(clean_currency).fillna(0)
            
    return df

try:
    df = load_data()
    st.title("📊 Control de Ejecución Presupuestal - PVD 2026")

    # Buscador de columnas clave
    col_ff = next((c for c in df.columns if 'FF' in c or 'FUENTE' in c), None)
    col_gasto = next((c for c in df.columns if 'GASTO' in c or 'TIPO' in c), None)
    col_pim = next((c for c in df.columns if 'PIM' in c), None)
    col_dev = next((c for c in df.columns if 'DEV' in c or 'DEVENGADO' in c), None)

    if col_ff and col_gasto:
        c1, c2 = st.columns(2)
        with c1:
            ff_sel = st.multiselect("Fuente de Financiamiento:", sorted(df[col_ff].unique()), default=df[col_ff].unique())
        with c2:
            gasto_sel = st.radio("Tipo de Gasto:", sorted(df[col_gasto].unique()), horizontal=True)

        # Filtrar datos
        df_f = df[(df[col_ff].isin(ff_sel)) & (df[col_gasto] == gasto_sel)].copy()

        # KPIs con formato moneda
        pim_val = df_f[col_pim].sum() if col_pim else 0
        dev_val = df_f[col_dev].sum() if col_dev else 0

        k1, k2 = st.columns(2)
        k1.metric("Presupuesto Total (PIM)", f"S/ {pim_val:,.2f}")
        k2.metric("Avance Devengado (%)", f"{(dev_val/pim_val*100):.1f}%" if pim_val > 0 else "0%")

        # GRÁFICO MENSUAL
        # Buscamos columnas que empiecen con PROG o tengan nombres de meses
        meses_lista = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SETIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
        prog_cols = []
        for m in meses_lista:
            encontrada = next((c for c in df.columns if m in c and ('PROG' in c or '_' in c)), None)
            if encontrada: prog_cols.append(encontrada)

        if prog_cols:
            sumas = [df_f[c].sum() for c in prog_cols]
            nombres_eje = [c.replace("PROG.", "").replace("_", "").strip() for c in prog_cols]
            
            df_barras = pd.DataFrame({"Mes": nombres_eje, "Monto": sumas})
            fig = px.bar(df_barras, x="Mes", y="Monto", title="Programación Mensual", 
                         text_auto='.2s', color_discrete_sequence=['#3399FF'])
            st.plotly_chart(fig, use_container_width=True)
            
    else:
        st.error("No se encontraron las columnas FF o GASTO. Revisa tu Excel.")

except Exception as e:
    st.error(f"Error detectado: {e}")
