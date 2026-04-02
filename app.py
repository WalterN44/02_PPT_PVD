import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(layout="wide", page_title="Dashboard PVD 2026", page_icon="📊")

@st.cache_data
def load_data():
    try:
        # El motor 'python' y sep=None detectan si usas (,) o (;) automáticamente
        df = pd.read_csv("data.csv", sep=None, engine='python', encoding='utf-8')
    except:
        # Si el anterior falla por las tildes, usa este formato
        df = pd.read_csv("data.csv", sep=None, engine='python', encoding='latin-1')
    
    # LIMPIEZA: Quitamos espacios vacíos al inicio o final de los nombres de columnas
    df.columns = df.columns.str.strip()
    
    # Convertimos las columnas de dinero a números (por si hay celdas vacías o con texto)
    cols_dinero = ['PIM', 'DEVENGADO', 'CERTIFICADO', 'COMPROMISO']
    for col in cols_dinero:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
    return df

# 2. EJECUCIÓN PRINCIPAL
try:
    df = load_data()

    st.title("📊 Control de Ejecución Presupuestal - PVD 2026")
    st.markdown("---")

    # 3. FILTROS EN LA PARTE SUPERIOR
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        fuentes = sorted(df['FF'].unique())
        ff_sel = st.multiselect("Seleccione Fuente de Financiamiento (FF):", fuentes, default=fuentes)
    
    with col_f2:
        gastos = sorted(df['GASTO'].unique())
        gasto_sel = st.radio("Seleccione Tipo de Gasto:", gastos, horizontal=True)

    # Aplicamos los filtros
    df_f = df[(df['FF'].isin(ff_sel)) & (df['GASTO'] == gasto_sel)]

    # 4. KPIs (INDICADORES CLAVE)
    pim = df_f['PIM'].sum()
    dev = df_f['DEVENGADO'].sum()
    cert = df_f['CERTIFICADO'].sum()

    k1, k2, k3 = st.columns(3)
    
    # Formato de moneda peruana (S/)
    k1.metric("Presupuesto (PIM)", f"S/ {pim:,.2f}")
    
    # Cálculo de porcentajes de avance
    porcentaje_dev = (dev / pim * 100) if pim > 0 else 0
    porcentaje_cert = (cert / pim * 100) if pim > 0 else 0
    
    k2.metric("Avance Devengado", f"{porcentaje_dev:.1f}%", delta=f"S/ {dev:,.0f}")
    k3.metric("Avance Certificado", f"{porcentaje_cert:.1f}%", delta=f"S/ {cert:,.0f}")

    st.markdown("### Programación Mensual de Gastos")

    # 5. GRÁFICO DE BARRAS POR MES
    meses = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", 
             "JULIO", "AGOSTO", "SETIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
    
    # Identificamos las columnas que empiezan con "PROG."
    prog_cols = [f"PROG. {m}" for m in meses if f"PROG. {m}" in df.columns]
    
    if prog_cols:
        # Sumamos los valores de cada mes y los limpiamos
        valores_mensuales = []
        for col in prog_cols:
            valor = pd.to_numeric(df_f[col], errors='coerce').sum()
            valores_mensuales.append(valor)
            
        nombres_meses = [c.replace("PROG. ", "") for c in prog_cols]
        
        df_grafico = pd.DataFrame({"Mes": nombres_meses, "Monto": valores_mensuales})
        
        fig = px.bar(df_grafico, x="Mes", y="Monto", 
                     text_auto='.2s', 
                     color_discrete_sequence=['#0083B8'],
                     template="plotly_white")
        
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No se encontraron columnas de programación mensual (PROG. ENERO, etc.)")

except Exception as e:
    st.error(f"⚠️ Error de lectura: {e}")
    st.info("Asegúrate de que las columnas en tu Excel se llamen exactamente: FF, GASTO, PIM, DEVENGADO, CERTIFICADO.")
