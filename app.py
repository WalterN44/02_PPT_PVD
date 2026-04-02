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
    
    # Limpieza segura de nombres de columnas
    df.columns = [str(c).strip().upper() for c in df.columns]
    
    # Función de limpieza de dinero ultra-resistente
    def clean_num(x):
        if isinstance(x, str):
            # Quitamos todo lo que no sea número, punto o signo menos
            x = x.replace('S/', '').replace('$', '').replace(',', '').strip()
        try:
            return float(x)
        except:
            return 0.0

    # Columnas que deben ser numéricas
    target_cols = [c for c in df.columns if any(k in c for k in ['PIM', 'CERT', 'COMP', 'DEV', 'ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO', 'JULIO', 'AGOSTO', 'SETIEMBRE', 'OCTUBRE', 'NOVIEMBRE', 'DICIEMBRE'])]
    
    for col in target_cols:
        df[col] = df[col].apply(clean_num)
        
    return df

try:
    df = load_data()
    
    # Buscadores flexibles para evitar errores de nombres
    c_ff = next((c for c in df.columns if 'FF' in c or 'FUENTE' in c), None)
    c_gasto = next((c for c in df.columns if 'GASTO' in c or 'TIPO' in c), None)
    c_pim = next((c for c in df.columns if 'PIM' in c), None)
    c_cert = next((c for c in df.columns if 'CERT' in c), None)
    c_comp = next((c for c in df.columns if 'COMP' in c), None)
    c_dev = next((c for c in df.columns if 'DEV' in c), None)

    st.title("📋 REPORTE PUD - 2026")
    st.markdown("---")

    # Filtros estilo botones
    c_btn1, c_btn2 = st.columns(2)
    with c_btn1:
        ff_list = ["TOTAL"] + sorted(list(df[c_ff].unique())) if c_ff else ["TOTAL"]
        ff_sel = st.radio("FUENTE FINANCIAMIENTO:", ff_list, horizontal=True)
    with c_btn2:
        gasto_list = ["TODO"] + sorted(list(df[c_gasto].unique())) if c_gasto else ["TODO"]
        gasto_sel = st.radio("TIPO DE GASTO:", gasto_list, horizontal=True)

    # Filtrado
    df_f = df.copy()
    if ff_sel != "TOTAL": df_f = df_f[df_f[c_ff] == ff_sel]
    if gasto_sel != "TODO": df_f = df_f[df_f[c_gasto] == gasto_sel]

    # KPIs
    t_pim = df_f[c_pim].sum() if c_pim else 0
    t_cert = df_f[c_cert].sum() if c_cert else 0
    t_comp = df_f[c_comp].sum() if c_comp else 0
    t_dev = df_f[c_dev].sum() if c_dev else 0

    # Velocímetros
    st.subheader("AVANCE DE EJECUCIÓN")
    g1, g2, g3 = st.columns(3)

    def draw_gauge(label, val, base, color):
        p = (val/base*100) if base > 0 else 0
        fig = go.Figure(go.Indicator(
            mode = "gauge+number", value = p,
            number = {'suffix': "%", 'font': {'size': 35}},
            title = {'text': f"<b>{label}</b><br><span style='font-size:0.7em'>S/ {val:,.2f}</span>"},
            gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': color}}
        ))
        fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
        return fig

    g1.plotly_chart(draw_gauge("DEVENGADO", t_dev, t_pim, "#2ecc71"), use_container_width=True)
    g2.plotly_chart(draw_gauge("CERTIFICADO", t_cert, t_pim, "#3498db"), use_container_width=True)
    g3.plotly_chart(draw_gauge("COMPROMISO", t_comp, t_pim, "#e67e22"), use_container_width=True)

    # Gráfico de Barras Mensual
    st.subheader("COMPORTAMIENTO MENSUAL")
    meses = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SETIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
    
    chart_data = []
    for m in meses:
        p_val = df_f[m].sum() if m in df_f.columns else 0
        d_val = df_f[f"DEV_{m}"].sum() if f"DEV_{m}" in df_f.columns else 0
        chart_data.append({"Mes": m, "Tipo": "Programación", "Monto": p_val})
        chart_data.append({"Mes": m, "Tipo": "Devengado", "Monto": d_val})

    if chart_data:
        fig_b = px.bar(pd.DataFrame(chart_data), x="Mes", y="Monto", color="Tipo", barmode="group", text_auto='.2s')
        st.plotly_chart(fig_b, use_container_width=True)

except Exception as e:
    st.error(f"Error al procesar los datos: {e}")
