import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Reporte PVD 2026")

@st.cache_data
def load_data():
    # SOLUCIÓN DE FUERZA BRUTA: 
    # on_bad_lines='skip' ignora filas que rompan el formato
    # skipinitialspace=True quita espacios después de las comas
    try:
        df = pd.read_csv(
            "data.csv", 
            sep=None, 
            engine='python', 
            on_bad_lines='skip', 
            encoding='utf-8',
            skipinitialspace=True
        )
    except:
        df = pd.read_csv(
            "data.csv", 
            sep=None, 
            engine='python', 
            on_bad_lines='skip', 
            encoding='latin-1',
            skipinitialspace=True
        )
    
    # Limpieza extrema de nombres de columnas
    df.columns = df.columns.str.strip().str.replace('"', '').str.replace("'", "")
    return df

try:
    df = load_data()

    st.title("📊 Control Presupuestal PVD 2026")

    # Verificar si las columnas críticas existen (con manejo de errores)
    columnas_reales = list(df.columns)
    
    # Buscamos nombres que se parezcan a 'GASTO' y 'FF' por si tienen espacios ocultos
    col_gasto = next((c for c in columnas_reales if 'GASTO' in c.upper()), None)
    col_ff = next((c for c in columnas_reales if 'FF' in c.upper()), None)

    if col_gasto and col_ff:
        c1, c2 = st.columns(2)
        with c1:
            ff_sel = st.multiselect("Fuente de Financiamiento:", df[col_ff].unique(), default=df[col_ff].unique())
        with c2:
            gasto_sel = st.radio("Tipo de Gasto:", df[col_gasto].unique(), horizontal=True)

        # Filtrar
        df_f = df[(df[col_ff].isin(ff_sel)) & (df[col_gasto] == gasto_sel)]

        # KPIs (Asegurando que sean numéricos)
        for col in ['PIM', 'DEVENGADO', 'CERTIFICADO', 'COMPROMISO']:
            if col in df_f.columns:
                df_f[col] = pd.to_numeric(df_f[col], errors='coerce').fillna(0)

        pim = df_f['PIM'].sum()
        dev = df_f['DEVENGADO'].sum()
        cert = df_f['CERTIFICADO'].sum()
        
        k1, k2, k3 = st.columns(3)
        k1.metric("Presupuesto Actual (PIM)", f"S/ {pim:,.2f}")
        k2.metric("Ejecución (DEV/PIM)", f"{(dev/pim)*100:.1f}%" if pim > 0 else "0%")
        k3.metric("Certificación", f"{(cert/pim)*100:.1f}%" if pim > 0 else "0%")

        # Gráfico Mensual
        meses = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SETIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
        prog_cols = [c for c in columnas_reales if "PROG." in c.upper()]
        
        if prog_cols:
            # Solo tomamos los meses que están en el Excel
            sumas = [pd.to_numeric(df_f[c], errors='coerce').sum() for c in prog_cols]
            nombres = [c.replace("PROG. ", "").replace("PROG.", "") for c in prog_cols]
            
            df_barras = pd.DataFrame({"Mes": nombres, "Monto": sumas})
            fig = px.bar(df_barras, x="Mes", y="Monto", title="Avance Mensual", color_discrete_sequence=['#00CC96'])
            st.plotly_chart(fig, use_container_width=True)

    else:
        st.error(f"No encontré las columnas clave. Columnas detectadas: {columnas_reales}")

except Exception as e:
    st.error(f"Error detectado: {e}")