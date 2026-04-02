import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(layout="wide", page_title="REPORTE PUD 2026")

# --- FUNCIÓN DE CARGA Y LIMPIEZA ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data.csv", sep=None, engine='python', encoding='utf-8')
    except:
        df = pd.read_csv("data.csv", sep=None, engine='python', encoding='latin-1')
    
    df.columns = df.columns.str.strip().str.upper()
    
    # Limpieza de montos
    cols_money = [c for c in df.columns if any(x in c for x in ['PIM', 'CERT', 'COMP', 'DEV', 'ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO', 'JULIO', 'AGOSTO', 'SETIEMBRE', 'OCTUBRE', 'NOVIEMBRE', 'DICIEMBRE'])]
    for col in cols_money:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace('S/', '').replace(',', ''), errors='coerce').fillna(0)
    return df

try:
    df = load_data()
    
    st.title("📋 REPORTE PUD - 2026")
    st.markdown("---")

    # --- SECCIÓN DE BOTONES (FILTROS) ---
    c_btn1, c_btn2 = st.columns(2)
    
    with c_btn1:
        st.subheader("FUENTE FINANCIAMIENTO")
        # Opción "TOTAL" agregada a los botones
        ff_options = ["TOTAL"] + list(df['FF'].unique())
        ff_sel = st.radio("Seleccione FF:", ff_options, horizontal=True)

    with c_btn2:
        st.subheader("TIPO DE GASTO PIM")
        gasto_options = ["TODO"] + list(df['GASTO'].unique())
        gasto_sel = st.radio("Seleccione Gasto:", gasto_options, horizontal=True)

    # Filtrado lógico
    df_f = df.copy()
    if ff_sel != "TOTAL":
        df_f = df_f[df_f['FF'] == ff_sel]
    if gasto_sel != "TODO":
        df_f = df_f[df_f['GASTO'] == gasto_sel]

    # --- CÁLCULOS ---
    total_pim = df_f['PIM'].sum()
    total_cert = df_f['CERTIFICADO'].sum()
    total_comp = df_f['COMPROMISO'].sum()
    total_dev = df_f['DEVENGADO'].sum()

    # --- FILA 1: DONA Y TABLA DE PIM ---
    col_left, col_right = st.columns([1, 2])

    with col_left:
        # Gráfico de Dona por FF (como en tu dibujo)
        fig_donut = px.pie(df_f, values='PIM', names='FF', hole=0.6, title="PIM por Fuente")
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_right:
        # Tabla resumen PIM (Todo, Inversión, Gasto Corriente)
        resumen_pim = df.groupby('GASTO')['PIM'].sum().reset_index()
        total_gen = resumen_pim['PIM'].sum()
        st.write("### RESUMEN PIM")
        st.table(pd.DataFrame({
            "CONCEPTO": ["TODO", "INVERSIÓN", "GASTO CORRIENTE"],
            "MONTO S/": [f"S/ {total_gen:,.2d}", 
                         f"S/ {df[df['GASTO'].str.contains('INVER', na=False)]['PIM'].sum():,.2f}",
                         f"S/ {df[df['GASTO'].str.contains('CORRIENTE', na=False)]['PIM'].sum():,.2f}"]
        }))

    # --- FILA 2: VELOCÍMETROS (GAUGES) ---
    st.markdown("### INDICADORES DE AVANCE")
    g1, g2, g3 = st.columns(3)

    def crear_gauge(titulo, actual, total, color):
        porc = (actual/total*100) if total > 0 else 0
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = porc,
            title = {'text': f"{titulo}<br><span style='font-size:0.8em;color:gray'>S/ {actual:,.0f}</span>"},
            gauge = {'axis': {'range': [None, 100]}, 'bar': {'color': color}}
        ))
        fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
        return fig

    g1.plotly_chart(crear_gauge("DEVENGADO", total_dev, total_pim, "green"), use_container_width=True)
    g2.plotly_chart(crear_gauge("CERTIFICADO", total_cert, total_pim, "blue"), use_container_width=True)
    g3.plotly_chart(crear_gauge("COMPROMISO", total_comp, total_pim, "orange"), use_container_width=True)

    # --- FILA 3: PROGRAMACIÓN VS EJECUCIÓN (BARRAS) ---
    st.markdown("### PROGRAMACIÓN Y EJECUCIÓN 2026")
    meses = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SETIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]
    
    data_meses = []
    for m in meses:
        prog = df_f[m].sum()
        # Asumiendo que tienes columnas de devengado mensual llamadas DEV_ENERO, etc.
        ejec = df_f[f"DEV_{m}"].sum() if f"DEV_{m}" in df_f.columns else 0
        data_meses.append({"Mes": m, "Tipo": "Programación", "Monto": prog})
        data_meses.append({"Mes": m, "Tipo": "Devengado", "Monto": ejec})

    df_barras = pd.DataFrame(data_meses)
    fig_barras = px.bar(df_barras, x="Mes", y="Monto", color="Tipo", barmode="group", text_auto='.2s')
    st.plotly_chart(fig_barras, use_container_width=True)

    # --- FILA 4: TABLA DETALLADA ---
    st.markdown("### EJECUCIÓN POR LÍNEA DE INTERVENCIÓN")
    # Filtramos por naturaleza según tu dibujo
    tabla_final = df_f[['GASTO', 'NOMBRES', 'PIM', 'CERTIFICADO', 'COMPROMISO', 'DEVENGADO']]
    st.dataframe(tabla_final.style.format({"PIM": "{:,.2f}", "CERTIFICADO": "{:,.2f}", "COMPROMISO": "{:,.2f}", "DEVENGADO": "{:,.2f}"}), use_container_width=True)

except Exception as e:
    st.error(f"Error al procesar: {e}")
    st.info("Asegúrate de que tu CSV tenga las columnas: FF, GASTO, PIM, CERTIFICADO, COMPROMISO, DEVENGADO y los Meses.")
