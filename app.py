import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="Reporte PVD 2026")

# ---------------------------
# DATA
# ---------------------------
RAW = [...]  # 👈 pega aquí tu JSON completo (sin cambiar nada)

df = pd.DataFrame(RAW)

MESES = ["ENERO","FEBRERO","MARZO","ABRIL","MAYO","JUNIO","JULIO","AGOSTO","SETIEMBRE","OCTUBRE","NOVIEMBRE","DICIEMBRE"]

# ---------------------------
# HELPERS
# ---------------------------
def fmt(n):
    if pd.isna(n): return "0"
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
            'bgcolor': "#1e293b"
        }
    ))
    fig.update_layout(height=250, margin=dict(l=10,r=10,t=40,b=10))
    return fig

# ---------------------------
# FILTROS
# ---------------------------
col1, col2 = st.columns(2)

with col1:
    gasto_filter = st.selectbox("Tipo de Gasto", ["TODO", "INVERSIÓN", "GASTO CORRIENTE"])

with col2:
    ff_filter = st.selectbox("Fuente", ["TODO", "RO", "ROOC"])

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
    "TOTAL_PROG": filtered["TOTAL_PROG."].sum()
}

st.title("📊 REPORTE PVD — 2026")
st.caption("Provías Descentralizado · Ejecución")

kpi_cols = st.columns(6)

for col, (k, v) in zip(kpi_cols, totals.items()):
    col.metric(k, fmt(v), fmt_full(v))

# ---------------------------
# DONUTS
# ---------------------------
col1, col2 = st.columns(2)

# Fuente
pim_by_ff = filtered.groupby("FF")["PIM"].sum()

fig_ff = go.Figure(data=[go.Pie(
    labels=pim_by_ff.index,
    values=pim_by_ff.values,
    hole=0.6
)])
fig_ff.update_layout(title="Fuente de Financiamiento")

col1.plotly_chart(fig_ff, use_container_width=True)

# Tipo gasto
pim_by_gasto = filtered.groupby("GASTO")["PIM"].sum()

fig_gasto = go.Figure(data=[go.Pie(
    labels=pim_by_gasto.index,
    values=pim_by_gasto.values,
    hole=0.6
)])
fig_gasto.update_layout(title="Tipo de Gasto")

col2.plotly_chart(fig_gasto, use_container_width=True)

# ---------------------------
# GAUGES
# ---------------------------
col1, col2, col3 = st.columns(3)

col1.plotly_chart(gauge(totals["DEVENGADO"], totals["PIM"], "Devengado", "#10b981"))
col2.plotly_chart(gauge(totals["CERTIFICADO"], totals["PIM"], "Certificado", "#06b6d4"))
col3.plotly_chart(gauge(totals["COMPROMISO"], totals["PIM"], "Compromiso", "#f59e0b"))

# ---------------------------
# BAR CHART
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
    title="Programación vs Ejecución 2026",
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

st.subheader("Ejecución por Línea")
st.dataframe(grouped.sort_values("PIM", ascending=False), use_container_width=True)
