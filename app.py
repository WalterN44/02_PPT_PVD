import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# --- CONFIGURACIÓN VISUAL ---
st.set_page_config(layout="wide", page_title="Reporte PVD 2026")

# CSS para fondo oscuro y tarjetas (Replica tu imagen objetivo)
st.markdown("""
    <style>
    .main { background-color: #0f172a; }
    [data-testid="stMetricValue"] { color: #3b82f6 !important; font-weight: 800; font-size: 24px; }
    .stPlotlyChart { background-color: rgba(0,0,0,0); }
    h1, h2, h3, p { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        # Cargamos el CSV con encoding flexible
        df = pd.read_csv("data.csv", encoding='latin-1', sep=None, engine='python')
        
        # LIMPIEZA DE COLUMNAS (Forma correcta que no da error de 'strip')
        df.columns = df.columns.str.strip().str.upper()
        
        # LIMPIEZA DE DATOS NUMÉRICOS: Quitar S/, comas y espacios
        for col in df.columns:
            if any(x in str(col) for x in ['PIM', 'PIA', 'DEV', 'CERT', 'COMP']):
                df[col] = df[col].astype(str).str.replace(r'[S/,\s]', '', regex=True)
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Limpieza de columnas de texto
        for col in df.select_dtypes(['object']).columns:
            df[col] = df[col].astype(str).str.strip()
            
        return df
    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")
        return pd.DataFrame()

# --- CARGA DE DATOS ---
df = load_data()

if not df.empty:
    # Encabezado (Como en tu imagen objetivo)
    st.markdown("<h1>REPORTE PVD — 2026</h1>", unsafe_allow_html=True)
    st.caption("Provías Descentralizado - Ejecución de Inversiones y Gasto Corriente")

    # Identificación de columnas
    c_gasto = next((c for c in df.columns if 'GASTO' in c), None)
    c_ff = next((c for c in df.columns if 'FF' in c), None)
    c_pim = next((c for c in df.columns if 'PIM' in c), None)
    c_dev = next((c for c in df.columns if 'DEV' in c), None)
    c_cert = next((c for c in df.columns if 'CERT' in c), None)
    c_comp = next((c for c in df.columns if 'COMP' in c), None)
    c_pia = next((c for c in df.columns if 'PIA' in c), 'PIM')

    # 1. FILTROS SUPERIORES
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        tipo_gasto = st.radio("TIPO DE GASTO:", ["TODO"] + list(df[c_gasto].unique()), horizontal=True)
    with col_f2:
        fuente = st.radio("FUENTE:", ["TODO"] + list(df[c_ff].unique()), horizontal=True)

    # Filtrar datos
    dff = df.copy()
    if tipo_gasto != "TODO": dff = dff[dff[c_gasto] == tipo_gasto]
    if fuente != "TODO": dff = dff[dff[c_ff] == fuente]

    # 2. TARJETAS DE INDICADORES (KPIs)
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("PIA", f"{(dff[c_pia].sum()/1e6):.2f} MM")
    k2.metric("PIM", f"{(dff[c_pim].sum()/1e6):.2f} MM")
    k3.metric("CERTIFICADO", f"{(dff[c_cert].sum()/1e6):.2f} MM")
    k4.metric("COMPROMISO", f"{(dff[c_comp].sum()/1e6):.2f} MM")

    st.markdown("---")

    # 3. GRÁFICOS (Donuts y Semicírculos)
    g1, g2, g3, g4 = st.columns(4)
    
    with g1: # Fuente de Financiamiento
        fig1 = px.pie(dff, values=c_pim, names=c_ff, hole=0.7, color_discrete_sequence=['#3b82f6', '#f59e0b'])
        fig1.update_layout(showlegend=False, height=200, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor='rgba(0,0,0,0)')
        st.markdown("<p style='text-align:center; font-size:12px;'>FUENTE DE FINANCIAMIENTO</p>", unsafe_allow_html=True)
        st.plotly_chart(fig1, use_container_width=True)

    with g2: # Tipo de Gasto
        fig2 = px.pie(dff, values=c_pim, names=c_gasto, hole=0.7, color_discrete_sequence=['#a855f7', '#06b6d4'])
        fig2.update_layout(showlegend=False, height=200, margin=dict(t=0,b=0,l=0,r=0), paper_bgcolor='rgba(0,0,0,0)')
        st.markdown("<p style='text-align:center; font-size:12px;'>TIPO DE GASTO</p>", unsafe_allow_html=True)
        st.plotly_chart(fig2, use_container_width=True)

    with g3: # Devengado %
        perc = (dff[c_dev].sum() / dff[c_pim].sum() * 100) if dff[c_pim].sum() > 0 else 0
        fig3 = go.Figure(go.Indicator(
            mode="gauge+number", value=perc, number={'suffix': "%", 'font':{'size':20, 'color':'white'}},
            gauge={'bar':{'color':"#10b981"}, 'bgcolor':"#1e293b", 'axis':{'range':[0,100]}}
        ))
        fig3.update_layout(height=200, margin=dict(t=40,b=0,l=20,r=20), paper_bgcolor='rgba(0,0,0,0)')
        st.markdown("<p style='text-align:center; font-size:12px;'>% DEVENGADO</p>", unsafe_allow_html=True)
        st.plotly_chart(fig3, use_container_width=True)

    with g4: # Certificado %
        perc_c = (dff[c_cert].sum() / dff[c_pim].sum() * 100) if dff[c_pim].sum() > 0 else 0
        fig4 = go.Figure(go.Indicator(
            mode="gauge+number", value=perc_c, number={'suffix': "%", 'font':{'size':20, 'color':'white'}},
            gauge={'bar':{'color':"#06b6d4"}, 'bgcolor':"#1e293b", 'axis':{'range':[0,100]}}
        ))
        fig4.update_layout(height=200, margin=dict(t=40,b=0,l=20,r=20), paper_bgcolor='rgba(0,0,0,0)')
        st.markdown("<p style='text-align:center; font-size:12px;'>% CERTIFICADO</p>", unsafe_allow_html=True)
        st.plotly_chart(fig4, use_container_width=True)

    # 4. GRÁFICO DE BARRAS MENSUAL
    st.markdown("### PROGRAMACIÓN Y EJECUCIÓN MENSUAL 2026")
    # Intentar buscar columnas de meses
    meses_cols = [c for c in dff.columns if any(m in c for m in ['ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN'])]
    if meses_cols:
        df_meses = dff[meses_cols].sum().reset_index()
        df_meses.columns = ['MES', 'MONTO']
        fig_bar = px.bar(df_meses, x='MES', y='MONTO', color_discrete_sequence=['#3b82f6'])
        fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
        st.plotly_chart(fig_bar, use_container_width=True)

else:
    st.warning("No se pudo cargar el archivo 'data.csv'. Asegúrate de que esté en la misma carpeta.")
