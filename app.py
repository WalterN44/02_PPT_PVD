import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuración de página
st.set_page_config(layout="wide", page_title="Reporte PVD 2026")

# Cargar Data
@st.cache_data
def load_data():
    df = pd.read_csv("tu_archivo.csv") # Reemplazar con el nombre de tu archivo
    return df

df = load_data()

# --- SIDEBAR / FILTROS ---
st.sidebar.header("Filtros de Control")
ff_selected = st.sidebar.multiselect("Fuente de Financiamiento (FF)", options=df['FF'].unique(), default=df['FF'].unique())
gasto_selected = st.sidebar.radio("Tipo de Gasto", options=df['GASTO'].unique())

df_filtered = df[(df['FF'].isin(ff_selected)) & (df['GASTO'] == gasto_selected)]

# --- KPIs CALCULADOS ---
pim_total = df_filtered['PIM'].sum()
dev_total = df_filtered['DEVENGADO'].sum()
cert_total = df_filtered['CERTIFICADO'].sum()
comp_total = df_filtered['COMPROMISO'].sum()

# Evitar división por cero
ejecucion = (dev_total / pim_total) * 100 if pim_total > 0 else 0
certificacion = (cert_total / pim_total) * 100 if pim_total > 0 else 0
compromiso = (comp_total / pim_total) * 100 if pim_total > 0 else 0

# --- LAYOUT DASHBOARD ---
st.title(f"📊 Dashboard de Ejecución Presupuestal 2026: {gasto_selected}")

col1, col2, col3, col4 = st.columns(4)
col1.metric("PIM Total", f"S/ {pim_total:,.2f}")
col2.metric("Ejecución (Dev/PIM)", f"{ejecucion:.1f}%", delta=f"{ejecucion-100:.1f}%")
col3.metric("Certificación", f"{certificacion:.1f}%")
col4.metric("Compromiso", f"{compromiso:.1f}%")

st.divider()

# --- GRÁFICO DE BARRAS MENSUAL ---
meses = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SETIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
prog_cols = [f"PROG. {m}" for m in meses]
dev_cols = [f"DEV. {m}" for m in meses if f"DEV. {m}" in df.columns]

# Sumatoria por meses para el gráfico
data_mensual = pd.DataFrame({
    'Mes': meses,
    'Programado': [df_filtered[f"PROG. {m}"].sum() for m in meses],
    'Devengado': [df_filtered[f"DEV. {m}"].sum() if f"DEV. {m}" in df.columns else 0 for m in meses]
})

fig_barras = px.bar(data_mensual, x='Mes', y=['Programado', 'Devengado'], 
             title="Programación vs Ejecución Mensual",
             barmode='group', color_discrete_sequence=['#1E293B', '#00E5FF'])

# --- GRÁFICO DE PRESUPUESTO POR NATURALEZA ---
fig_pie = px.pie(df_filtered, values='PIM', names='NATURALEZA', 
                 title="Distribución Presupuesto (PIM) por Naturaleza",
                 hole=0.4)

c1, c2 = st.columns([2, 1])
c1.plotly_chart(fig_barras, use_container_width=True)
c2.plotly_chart(fig_pie, use_container_width=True)