import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(layout="wide", page_title="REPORTE PUD 2026")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data.csv", sep=None, engine='python', encoding='utf-8')
    except:
        df = pd.read_csv("data.csv", sep=None, engine='python', encoding='latin-1')
    
    # Limpieza: quitamos espacios y pasamos todo a mayúsculas para no fallar
    df.columns = df.columns.str.strip().str.upper()
    
    # Limpieza de montos: quitamos S/ y comas para poder sumar
    cols_money = [c for c in df.columns if any(x in c for x in ['PIM', 'CERT', 'COMP', 'DEV', 'ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO', 'JULIO', 'AGOSTO', 'SETIEMBRE', 'OCTUBRE', 'NOVIEMBRE', 'DICIEMBRE'])]
    for col in cols_money:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace('S/', '').replace(',', '').strip(), errors='coerce').fillna(0)
    return df

try:
    df = load_data()
    
    # --- BUSCADOR FLEXIBLE DE COLUMNAS ---
    # Esto evita el error que te salió ('GASTO')
    c_ff = next((c for c in df.columns if 'FF' in c or 'FUENTE' in c), None)
    c_gasto = next((c for c in df.columns if 'GASTO' in c or 'TIPO' in c), None)
    c_pim = next((c for c in df.columns if 'PIM' in c), None)
    c_cert = next((c for c in df.columns if 'CERT' in c), None)
    c_comp = next((c for c in df.columns if 'COMP' in c), None)
    c_dev = next((c for c in df.columns if 'DEV' in c), None)

    st.title("📋 REPORTE PUD - 2026")
    st.markdown("---")

    # --- SECCIÓN DE BOTONES ---
    c_btn1, c_btn2 = st.columns(2)
    
    with c_btn1:
        st.subheader("FUENTE FINANCIAMIENTO")
        ff_list = ["TOTAL"] + list(df[c_ff].unique()) if c_ff else ["TOTAL"]
        ff_sel = st.radio("Seleccione FF:", ff_list, horizontal=True)

    with c_btn2:
        st.subheader("TIPO DE GASTO PIM")
        gasto_list = ["TODO"] + list(df[c_gasto].unique()) if c_gasto else ["TODO"]
        gasto_sel = st.radio("Seleccione Gasto:", gasto_list, horizontal=True)

    # Filtrado dinámico
    df_f = df.copy()
    if ff_sel != "TOTAL": df_f = df_f[df_f[c_ff] == ff_sel]
    if gasto_sel != "TODO": df_f = df_f[df_f[c_gasto] == gasto_sel]

    # --- CÁLCULOS SEGUROS ---
    total_pim = df_f[c_pim].sum() if c_pim else 0
    total_cert = df_f[c_cert].sum() if c_cert else 0
    total_comp = df_f[c_comp].sum() if c_comp else 0
    total_dev = df_f[c_dev].sum() if c_dev else 0

    # --- INDICADORES (GAUGES / VELOCÍMETROS) ---
    st.markdown("### INDICADORES DE AVANCE")
    g1, g2, g3 = st.columns(3)

    def crear_gauge(titulo, actual, total, color):
        porc = (actual/total*100) if total > 0 else 0
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = porc,
            number = {'suffix': "%", 'font': {'size': 40}},
            title = {'text': f"<b>{titulo}</b><br><span style='font-size:0.8em;color:gray'>S/ {actual:,.0f}</span>"},
            gauge = {'axis': {'range': [None, 100]}, 'bar': {'color': color}}
        ))
        fig.update_layout(height=280, margin=dict(l=30, r=30, t=50, b=20))
        return fig

    g1.plotly_chart(crear_gauge("DEVENGADO", total_dev, total_pim, "#2ecc71"), use_container_width=True)
    g2.plotly_chart(crear_gauge("CERTIFICADO", total_cert, total_pim, "#3498db"), use_container_width=True)
    g3.plotly_chart(crear_gauge("COMPROMISO", total_comp, total_pim, "#e67e22"), use_container_width=True)

    # --- GRÁFICO DE BARRAS MENSUAL ---
    st.markdown("### PROGRAMACIÓN Y EJECUCIÓN MENSUAL")
    meses = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SETIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
    
    data_grafico = []
    for m in meses:
        prog_val = df_f[m].sum() if m in df_f.columns else 0
        dev_mes_col = f"DEV_{m}"
        dev_mes_val = df_f[dev_mes_col].sum() if dev_mes_col in df_f.columns else 0
        data_grafico.append({"Mes": m, "Tipo": "Programación", "Monto": prog_val})
        data_grafico.append({"Mes": m, "Tipo": "Devengado", "Monto": dev_mes_val})

    if data_grafico:
        fig_bar = px.bar(pd.DataFrame(data_grafico), x="Mes", y="Monto", color="Tipo", barmode="group", text_auto='.2s')
        st.plotly_chart(fig_bar, use_container_width=True)

except Exception as e:
    st.error(f"Error crítico: {e}")
    st.info("Revisa que tu Excel tenga columnas con los nombres: FF, GASTO, PIM, CERTIFICADO, COMPROMISO, DEVENGADO.")
