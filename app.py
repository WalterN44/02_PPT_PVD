import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide", page_title="Reporte PVD 2026")

# Estilo para modo oscuro y métricas
st.markdown("""
    <style>
    .main { background-color: #0f172a; }
    div[data-testid="stMetricValue"] { color: #ffffff !important; font-size: 28px !important; font-weight: 800; }
    div[data-testid="stMetricLabel"] { color: #94a3b8 !important; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        # Cargamos con detección automática de separador
        df = pd.read_csv("data.csv", encoding='latin-1', sep=None, engine='python')
        
        # LIMPIEZA RADICAL DE COLUMNAS: Quitamos espacios y pasamos a mayúsculas
        df.columns = [str(c).strip().upper() for c in df.columns]
        
        # LIMPIEZA DE DATOS: Quitamos espacios en todas las celdas de texto
        for col in df.select_dtypes(['object']).columns:
            df[col] = df[col].astype(str).str.strip()
            
        return df
    except Exception as e:
        st.error(f"Error crítico al leer el archivo: {e}")
        return pd.DataFrame()

def create_gauge(title, value, total, color):
    percentage = (value / total * 100) if total > 0 else 0
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = percentage,
        number = {'suffix': "%", 'font': {'color': "white", 'size': 26}},
        title = {'text': title, 'font': {'color': color, 'size': 16, 'weight': "bold"}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#334155"},
            'bar': {'color': color},
            'bgcolor': "#1e293b",
            'borderwidth': 2,
            'bordercolor': "#334155",
            'steps': [{'range': [0, 100], 'color': '#0f172a'}]
        }
    ))
    fig.update_layout(height=180, margin=dict(l=25, r=25, t=40, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig

# --- EJECUCIÓN ---
df = load_data()

if not df.empty:
    # Título según tu boceto
    st.markdown("<h1 style='text-align: center; color: white;'>REPORTE PVD - 2026</h1>", unsafe_allow_html=True)
    
    # 1. IDENTIFICACIÓN FLEXIBLE DE COLUMNAS
    # Esto evita el KeyError: Busca la columna que contenga la palabra clave
    col_gasto = next((c for c in df.columns if "GASTO" in c), None)
    col_ff = next((c for c in df.columns if "FF" in c or "FUENTE" in c), None)
    col_pim = next((c for c in df.columns if "PIM" in c), None)
    col_dev = next((c for c in df.columns if "DEV" in c), None)
    col_cert = next((c for c in df.columns if "CERT" in c), None)
    col_comp = next((c for c in df.columns if "COMP" in c), None)

    if not col_gasto or not col_ff:
        st.error(f"No encontré las columnas necesarias. Columnas detectadas: {list(df.columns)}")
        st.stop()

    # 2. FILTROS (BOTONES Y SELECTORES)
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        fuente_opciones = ["TODO"] + sorted(df[col_ff].unique().tolist())
        fuente = st.selectbox("FUENTE DE FINANCIAMIENTO (FF):", fuente_opciones)
    with col_f2:
        gasto_opciones = ["TODO"] + sorted(df[col_gasto].unique().tolist())
        tipo_gasto = st.radio("TIPO DE GASTO PIM:", gasto_opciones, horizontal=True)

    # Filtrado lógico
    dff = df.copy()
    if fuente != "TODO":
        dff = dff[dff[col_ff] == fuente]
    if tipo_gasto != "TODO":
        dff = dff[dff[col_gasto] == tipo_gasto]

    # Totales numéricos (asegurando que sean números)
    total_pim = pd.to_numeric(dff[col_pim], errors='coerce').sum()
    total_dev = pd.to_numeric(dff[col_dev], errors='coerce').sum()
    total_cert = pd.to_numeric(dff[col_cert], errors='coerce').sum()
    total_comp = pd.to_numeric(dff[col_comp], errors='coerce').sum()

    # 3. VISUALIZACIÓN: VELOCÍMETROS (Según tu boceto)
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.plotly_chart(create_gauge("DEVENGADO", total_dev, total_pim, "#10b981"), use_container_width=True)
    with c2:
        st.plotly_chart(create_gauge("CERTIFICADO", total_cert, total_pim, "#3b82f6"), use_container_width=True)
    with c3:
        st.plotly_chart(create_gauge("COMPROMISO", total_comp, total_pim, "#f59e0b"), use_container_width=True)

    # Resumen de PIM
    st.markdown(f"""
        <div style="background-color: #1e293b; padding: 20px; border-radius: 10px; border: 1px solid #334155; text-align: center;">
            <h2 style="margin:0; color: #94a3b8; font-size: 16px;">PRESUPUESTO TOTAL (PIM)</h2>
            <h1 style="margin:0; color: #ffffff; font-size: 42px;">S/ {total_pim:,.2f}</h1>
        </div>
    """, unsafe_allow_html=True)

    # 4. TABLA DE DETALLE (Línea de Intervención)
    st.markdown("### EJECUCIÓN POR LÍNEA DE INTERVENCIÓN")
    col_nat = next((c for c in df.columns if "NATU" in c), df.columns[1])
    
    tabla = dff.groupby(col_nat).agg({
        col_pim: 'sum',
        col_dev: 'sum'
    }).reset_index()
    
    tabla['% AVANCE'] = (tabla[col_dev] / tabla[col_pim] * 100).fillna(0)
    
    # Formato final para mostrar
    tabla_show = tabla.copy()
    tabla_show[col_pim] = tabla_show[col_pim].map("S/ {:,.2f}".format)
    tabla_show[col_dev] = tabla_show[col_dev].map("S/ {:,.2f}".format)
    tabla_show['% AVANCE'] = tabla_show['% AVANCE'].map("{:.1f}%".format)

    st.table(tabla_show)

else:
    st.info("Esperando archivo 'data.csv' en la carpeta del proyecto...")
