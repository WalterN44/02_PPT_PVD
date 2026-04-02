import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide", page_title="Reporte PVD 2026")

# Estilo CSS para replicar la imagen oscura y profesional
st.markdown("""
    <style>
    .main { background-color: #0f172a; }
    [data-testid="stMetricValue"] { color: #3b82f6 !important; font-weight: 800; font-size: 22px; }
    .card { background-color: #1e293b; padding: 20px; border-radius: 10px; border: 1px solid #334155; margin-bottom: 10px; }
    h1, h2, h3 { color: white !important; font-family: 'Inter', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_and_clean_data():
    try:
        # 1. Carga con detección de errores
        df = pd.read_csv("data.csv", encoding='latin-1', sep=None, engine='python', on_bad_lines='skip')
        
        # 2. Limpieza total de nombres de columnas
        df.columns = [str(c).strip().upper() for c in df.columns]
        
        # 3. Identificación de columnas clave (Flexible)
        col_map = {
            'PIM': next((c for c in df.columns if 'PIM' in c), None),
            'DEV': next((c for c in df.columns if 'DEV' in c), None),
            'CERT': next((c for c in df.columns if 'CERT' in c), None),
            'COMP': next((c for c in df.columns if 'COMP' in c), None),
            'PIA': next((c for c in df.columns if 'PIA' in c), None),
            'FF': next((c for c in df.columns if 'FF' in c), None),
            'GASTO': next((c for c in df.columns if 'GASTO' in c), None),
            'NAT': next((c for c in df.columns if 'NATU' in c), None)
        }

        # 4. Forzar conversión a NÚMEROS (Esto quita el TypeError)
        cols_to_fix = [col_map['PIM'], col_map['DEV'], col_map['CERT'], col_map['COMP'], col_map['PIA']]
        for col in cols_to_fix:
            if col:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '').str.replace('S/', '').strip(), errors='coerce').fillna(0)
        
        return df, col_map
    except Exception as e:
        st.error(f"Error cargando CSV: {e}")
        return pd.DataFrame(), {}

def fmt_millions(n):
    return f"{n/1e6:.2f} MM"

# --- LÓGICA DE INTERFAZ ---
df, cols = load_and_clean_data()

if not df.empty:
    st.markdown("<h1 style='margin-bottom:0;'>REPORTE PVD — 2026</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748b; margin-top:0;'>Provías Descentralizado - Ejecución de Inversiones y Gasto Corriente</p>", unsafe_allow_html=True)

    # 1. FILTROS (Estilo botones superiores)
    c_f1, c_f2 = st.columns([1, 1])
    with c_f1:
        tipo_gasto = st.radio("TIPO DE GASTO:", ["TODO"] + list(df[cols['GASTO']].unique()), horizontal=True)
    with c_f2:
        fuente = st.radio("FUENTE:", ["TODO"] + list(df[cols['FF']].unique()), horizontal=True)

    # Aplicar filtros
    dff = df.copy()
    if tipo_gasto != "TODO": dff = dff[dff[cols['GASTO']] == tipo_gasto]
    if fuente != "TODO": dff = dff[dff[cols['FF']] == fuente]

    # 2. TARJETAS SUPERIORES (KPIs)
    t1, t2, t3, t4 = st.columns(4)
    with t1: st.metric("PIA", fmt_millions(dff[cols['PIA']].sum()))
    with t2: st.metric("PIM", fmt_millions(dff[cols['PIM']].sum()))
    with t3: st.metric("CERTIFICADO", fmt_millions(dff[cols['CERT']].sum()))
    with t4: st.metric("COMPROMISO", fmt_millions(dff[cols['COMP']].sum()))

    st.markdown("---")

    # 3. GRÁFICOS CIRCULARES (Donuts)
    g1, g2, g3, g4 = st.columns(4)
    
    total_pim = dff[cols['PIM']].sum()
    
    with g1:
        # Fuente de Financiamiento
        fig_ff = px.pie(dff, values=cols['PIM'], names=cols['FF'], hole=0.7, 
                        color_discrete_sequence=['#3b82f6', '#f59e0b'])
        fig_ff.update_layout(showlegend=False, height=250, margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)')
        st.markdown("<p style='text-align:center; font-size:12px; color:#94a3b8;'>FUENTE DE FINANCIAMIENTO</p>", unsafe_allow_html=True)
        st.plotly_chart(fig_ff, use_container_width=True)

    with g2:
        # Tipo de Gasto
        fig_g = px.pie(dff, values=cols['PIM'], names=cols['GASTO'], hole=0.7,
                       color_discrete_sequence=['#a855f7', '#06b6d4'])
        fig_g.update_layout(showlegend=False, height=250, margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)')
        st.markdown("<p style='text-align:center; font-size:12px; color:#94a3b8;'>TIPO DE GASTO</p>", unsafe_allow_html=True)
        st.plotly_chart(fig_g, use_container_width=True)

    with g3:
        # Avance Devengado (Semicírculo)
        avance = (dff[cols['DEV']].sum() / total_pim * 100) if total_pim > 0 else 0
        fig_dev = go.Figure(go.Indicator(
            mode="gauge+number", value=avance, number={'suffix': "%", 'font':{'color':'white'}},
            gauge={'bar': {'color': "#10b981"}, 'bgcolor': "#1e293b", 'axis': {'range': [0, 100]}}
        ))
        fig_dev.update_layout(height=250, margin=dict(t=50, b=0), paper_bgcolor='rgba(0,0,0,0)')
        st.markdown("<p style='text-align:center; font-size:12px; color:#94a3b8;'>DEVENGADO</p>", unsafe_allow_html=True)
        st.plotly_chart(fig_dev, use_container_width=True)

    with g4:
        # Avance Certificado
        avance_c = (dff[cols['CERT']].sum() / total_pim * 100) if total_pim > 0 else 0
        fig_cert = go.Figure(go.Indicator(
            mode="gauge+number", value=avance_c, number={'suffix': "%", 'font':{'color':'white'}},
            gauge={'bar': {'color': "#06b6d4"}, 'bgcolor': "#1e293b", 'axis': {'range': [0, 100]}}
        ))
        fig_cert.update_layout(height=250, margin=dict(t=50, b=0), paper_bgcolor='rgba(0,0,0,0)')
        st.markdown("<p style='text-align:center; font-size:12px; color:#94a3b8;'>CERTIFICADO</p>", unsafe_allow_html=True)
        st.plotly_chart(fig_cert, use_container_width=True)

    # 4. GRÁFICO DE BARRAS MENSUAL (Simulado con los datos disponibles)
    st.markdown("### PROGRAMACIÓN Y EJECUCIÓN MENSUAL 2026")
    # Buscamos columnas que empiecen por 'PROG_' o 'DEV_'
    meses_cols = [c for c in dff.columns if 'PROG_' in c or 'DEV_' in c]
    if meses_cols:
        df_meses = dff[meses_cols].sum().reset_index()
        df_meses.columns = ['MES', 'MONTO']
        fig_bar = px.bar(df_meses, x='MES', y='MONTO', color_discrete_sequence=['#3b82f6'])
        fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
        st.plotly_chart(fig_bar, use_container_width=True)

else:
    st.error("Por favor, asegúrate de que 'data.csv' esté en la carpeta y tenga las columnas correctas.")
