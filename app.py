import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="Reporte PVD 2026")

# ---------------------------
# CARGA DE DATA (ROBUSTA)
# ---------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data.csv", encoding="utf-8")
    except:
        df = pd.read_csv("data.csv", encoding="latin-1")

    # 🔥 FIX ERROR strip
    df.columns = df.columns.str.strip()

    # limpiar strings
    for col in df.select_dtypes(include="object"):
        df[col] = df[col].astype(str).str.strip()

    # convertir numéricos
    for col in df.columns:
        if col not in ["GASTO", "NATURALEZA", "FF"]:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df

df = load_data()

MESES = ["ENERO","FEBRERO","MARZO","ABRIL","MAYO","JUNIO","JULIO","AGOSTO","SETIEMBRE","OCTUBRE","NOVIEMBRE","DICIEMBRE"]

# ---------------------------
# FORMATOS
# ---------------------------
def fmt(n):
    if abs(n) >= 1e9: return f"{n/1e9:.2f} MM"
    if abs(n) >= 1e6: return f"{n/1e6:.1f} M"
    if abs(n) >= 1e3: return f"{n/1e3:.1f} K"
    return f"{n:.0f}"

def fmt_full(n):
    return f"S/ {int(n):,}".replace(",", ".")

def gauge(value, total, title, color):
    pct = 0 if total == 0 else value / total

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=pct * 100,
        number={'suffix': "%"},
        title={'text': title},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': color},
        }
    ))
    fig.update_layout(height=220, margin=dict(l=10,r=10,t=40,b=10))
    return fig

# ---------------------------
# HEADER
# ---------------------------
st.markdown("## 📊 REPORTE PVD — 2026")
st.caption("Provías Descentralizado · Ejecución de Inversiones y Gasto Corriente")

# ---------------------------
# FILTROS
# ---------------------------
col1, col2 = st.columns(2)

with col1:
    gasto_filter = st.radio("Tipo de Gasto", ["TODO", "INVERSIÓN", "GASTO CORRIENTE"], horizontal=True)

with col2:
    ff_filter = st.radio("Fuente", ["TODO", "RO", "ROOC"], horizontal=True)

filtered = df.copy()

if gasto_filter == "INVERSIÓN":
    filtered = filtered[filtered["GASTO"] == "Inversión"]
elif gasto_filter == "GASTO CORRIENTE":
    filtered = filtered[filtered["GASTO"] == "Gasto corriente"]

if ff_filter != "TODO":
    filtered = filtered[filtered["FF"] == ff_filter]

# ---------------------------
# KPIs
# ---------------------------
totals = {
    "PIA": filtered["PIA"].sum(),
    "PIM": filtered["PIM"].sum(),
    "CERTIFICADO": filtered["CERTIFICADO"].sum(),
    "COMPROMISO": filtered["COMPROMISO"].sum(),
    "DEVENGADO": filtered["DEVENGADO"].sum(),
    "PROGRAMADO": filtered["TOTAL_PROG."].sum()
}

cols = st.columns(6)

for col, (k, v) in zip(cols, totals.items()):
    col.metric(k, fmt(v), fmt_full(v))

# ---------------------------
# DONUTS
# ---------------------------
col1, col2 = st.columns(2)

pim_ff = filtered.groupby("FF")["PIM"].sum()

fig1 = go.Figure(data=[go.Pie(
    labels=pim_ff.index,
    values=pim_ff.values,
    hole=0.65
)])
fig1.update_layout(title="Fuente de Financiamiento")

col1.plotly_chart(fig1, use_container_width=True)

pim_gasto = filtered.groupby("GASTO")["PIM"].sum()

fig2 = go.Figure(data=[go.Pie(
    labels=pim_gasto.index,
    values=pim_gasto.values,
    hole=0.65
)])
fig2.update_layout(title="Tipo de Gasto")

col2.plotly_chart(fig2, use_container_width=True)

# ---------------------------
# GAUGES
# ---------------------------
g1, g2, g3 = st.columns(3)

g1.plotly_chart(gauge(totals["DEVENGADO"], totals["PIM"], "Devengado", "#10b981"))
g2.plotly_chart(gauge(totals["CERTIFICADO"], totals["PIM"], "Certificado", "#06b6d4"))
g3.plotly_chart(gauge(totals["COMPROMISO"], totals["PIM"], "Compromiso", "#f59e0b"))

# ---------------------------
# BARRAS MENSUALES
# ---------------------------
prog = []
dev = []

for m in MESES:
    prog.append(filtered[f"PROG._{m}"].sum())
    dev.append(filtered.get(f"DEV._{m}", 0).sum())

fig_bar = go.Figure()

fig_bar.add_bar(x=MESES, y=prog, name="Programado")
fig_bar.add_bar(x=MESES, y=dev, name="Devengado")

fig_bar.update_layout(
    title="Programación y Ejecución Mensual 2026",
    barmode='group'
)

st.plotly_chart(fig_bar, use_container_width=True)

# ---------------------------
# TABLA
# ---------------------------
grouped = filtered.groupby(["NATURALEZA","GASTO"]).agg({
    "PIM":"sum",
    "CERTIFICADO":"sum",
    "COMPROMISO":"sum",
    "DEVENGADO":"sum"
}).reset_index()

grouped["% EJEC"] = np.where(
    grouped["PIM"] > 0,
    grouped["DEVENGADO"] / grouped["PIM"] * 100,
    0
)

st.subheader("Ejecución por Línea de Intervención")
st.dataframe(
    grouped.sort_values("PIM", ascending=False),
    use_container_width=True
)

# ---------------------------
# FOOTER
# ---------------------------
st.caption("Provías Descentralizado — MTC · Dashboard generado con Streamlit")
