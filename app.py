import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuración de página
st.set_page_config(layout="wide", page_title="Reporte PVD 2026")

# Estilo CSS para modo oscuro y tarjetas
st.markdown("""
    <style>
    .main { background-color: #0f172a; }
    .stMetric { background-color: #1e293b; padding: 15px; border-radius: 10px; border: 1px solid #334155; }
    div[data-testid="stMetricValue"] { color: white; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        # Carga y limpieza inicial
        df = pd.read_csv("data.csv", encoding='utf-8', sep=None, engine='python')
        # Limpiar espacios en nombres de columnas
        df.columns = [c.strip().upper() for c in df.columns]
        # Limpiar espacios en los datos de texto para evitar errores de filtrado
        for col in df.select_dtypes(['object']).columns:
            df[col] = df[col].astype(str).str.strip()
        return df
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return pd.DataFrame()

def create_gauge(title, value, total, color):
    percentage = (value / total * 100) if total > 0 else 0
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = percentage,
        number = {'suffix': "%", 'font': {'color': "white", 'size': 24}},
        title = {'text': title, 'font': {'color': color, 'size': 16, 'weight': "bold"}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#334155"},
            'bar': {'color': color},
            'bgcolor': "#0f172a",
            'borderwidth': 2,
            'bordercolor': "#334155",
            'steps': [{'range': [0, 100], 'color': '#1e293b'}],
        }
    ))
    fig.update_layout(height=200, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig

# --- LÓGICA PRINCIPAL ---
df = load_data()

if not df.empty:
    st.title("📊 Reporte PVD - 2026")
    
    # 1. FILTROS (Basados en tus botones del boceto)
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        ff_list = ["TODO"] + sorted(df['FF'].unique().tolist())
        fuente = st.selectbox("FUENTE DE FINANCIAMIENTO (FF):", ff_list)
    with col_f2:
        gasto_list = ["TODO"] + sorted(df['GASTO'].unique().tolist())
        tipo_gasto = st.radio("TIPO DE GASTO:", gasto_list, horizontal=True)

    # Aplicar Filtros
    dff = df.copy()
    if fuente != "TODO":
        dff = dff[dff['FF'] == fuente]
    if tipo_gasto != "TODO":
        dff = dff[dff['GASTO'] == tipo_gasto]

    # Cálculos de Totales
    total_pim = dff['PIM'].sum()
    total_dev = dff['DEVENGADO'].sum()
    total_cert = dff['CERTIFICADO'].sum()
    total_comp = dff['COMPROMISO'].sum()

    # 2. INDICADORES (Velocímetros como en tu dibujo)
    st.markdown("---")
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.plotly_chart(create_gauge("DEVENGADO", total_dev, total_pim, "#10b981"), use_container_width=True)
    with c2:
        st.plotly_chart(create_gauge("CERTIFICADO", total_cert, total_pim, "#3b82f6"), use_container_width=True)
    with c3:
        st.plotly_chart(create_gauge("COMPROMISO", total_comp, total_pim, "#f59e0b"), use_container_width=True)
    with c4:
        st.metric("PRESUPUESTO PIM", f"S/ {total_pim:,.0f}")
        st.metric("SALDO PIM", f"S/ {(total_pim - total_dev):,.0f}")

    # 3. TABLA DE EJECUCIÓN (Línea de intervención)
    st.markdown("### EJECUCIÓN POR LÍNEA DE INTERVENCIÓN")
    # Agrupamos por Naturaleza para limpiar la vista
    tabla = dff.groupby('NATURALEZA').agg({
        'PIM': 'sum',
        'CERTIFICADO': 'sum',
        'COMPROMISO': 'sum',
        'DEVENGADO': 'sum'
    }).reset_index()
    
    tabla['% AVANCE'] = (tabla['DEVENGADO'] / tabla['PIM'] * 100).fillna(0).map("{:.1f}%".format)
    
    # Formatear números para la tabla
    for col in ['PIM', 'CERTIFICADO', 'COMPROMISO', 'DEVENGADO']:
        tabla[col] = tabla[col].map("S/ {:,.2f}".format)

    st.dataframe(tabla, use_container_width=True, hide_index=True)

else:
    st.warning("No se encontraron datos. Verifica que el archivo data.csv esté en la misma carpeta.")
