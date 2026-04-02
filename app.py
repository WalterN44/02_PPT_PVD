import React, { useState, useMemo } from "react";

// --- DATOS PROPORCIONADOS (RAW) ---
const RAW = [{"GASTO":"Gasto corriente","NATURALEZA":"Emergencias en VD","FF":"RO","PIA":200000,"PIM":218344,"CERTIFICADO":218343.63,"COMPROMISO":178303.63,"DEVENGADO":178303.63,"PROG._ENERO":0,"DEV._ENERO":36000,"PROG._FEBRERO":26000,"DEV._FEBRERO":57979.6,"PROG._MARZO":26000,"DEV._MARZO":28400,"PROG._ABRIL":0,"PROG._MAYO":0,"PROG._JUNIO":8135.93,"PROG._JULIO":5000,"PROG._AGOSTO":5000,"PROG._SETIEMBRE":5000,"PROG._OCTUBRE":0,"PROG._NOVIEMBRE":0,"PROG._DICIEMBRE":52189.37,"TOTAL_PROG.":230493,"SALDO_PROG.":-12149},/*... resto de datos ...*/];

const MESES = ["ENERO","FEBRERO","MARZO","ABRIL","MAYO","JUNIO","JULIO","AGOSTO","SETIEMBRE","OCTUBRE","NOVIEMBRE","DICIEMBRE"];
const MESES_SHORT = ["ENE","FEB","MAR","ABR","MAY","JUN","JUL","AGO","SET","OCT","NOV","DIC"];

// --- UTILIDADES ---
const fmt = (n) => {
  if (n == null || isNaN(n)) return "0";
  const abs = Math.abs(n);
  if (abs >= 1e6) return (n/1e6).toFixed(1) + " M";
  if (abs >= 1e3) return (n/1e3).toFixed(1) + " K";
  return n.toFixed(0);
};

const fmtFull = (n) => "S/ " + Math.round(n || 0).toLocaleString("es-PE");

// --- COMPONENTE: VELOCÍMETRO (GAUGE) ---
function Gauge({ value, total, label, color }) {
  const size = 160;
  const radius = 65;
  const cx = 80;
  const cy = 85;
  const percentage = total > 0 ? Math.min(value / total, 1) : 0;
  const circumference = Math.PI * radius;
  const dashOffset = circumference * (1 - percentage);

  return (
    <div style={{ textAlign: "center", background: "#1e293b", padding: "15px", borderRadius: "12px", border: "1px solid #334155" }}>
      <svg width={size} height={size * 0.65}>
        <path d={`M ${cx - radius} ${cy} A ${radius} ${radius} 0 0 1 ${cx + radius} ${cy}`} fill="none" stroke="#0f172a" strokeWidth="12" strokeLinecap="round"/>
        <path d={`M ${cx - radius} ${cy} A ${radius} ${radius} 0 0 1 ${cx + radius} ${cy}`} fill="none" stroke={color} strokeWidth="12" strokeLinecap="round"
          strokeDasharray={circumference} strokeDashoffset={dashOffset} style={{ transition: "all 0.8s ease-out" }}/>
        <text x={cx} y={cy - 15} textAnchor="middle" fill="#f8fafc" fontSize="20" fontWeight="800">{(percentage * 100).toFixed(1)}%</text>
        <text x={cx} y={cy + 5} textAnchor="middle" fill="#94a3b8" fontSize="10" fontWeight="600">{fmt(value)}</text>
      </svg>
      <div style={{ fontSize: "11px", fontWeight: "700", color: color, textTransform: "uppercase", letterSpacing: "1px" }}>{label}</div>
    </div>
  );
}

// --- COMPONENTE PRINCIPAL ---
export default function DashboardPVD() {
  const [gastoFilter, setGastoFilter] = useState("TODO");
  const [ffFilter, setFfFilter] = useState("TODO");

  // Filtrado de datos según los botones
  const filtered = useMemo(() => {
    return RAW.filter(r => {
      const matchGasto = gastoFilter === "TODO" || r.GASTO.toUpperCase() === gastoFilter;
      const matchFF = ffFilter === "TODO" || r.FF === ffFilter;
      return matchGasto && matchFF;
    });
  }, [gastoFilter, ffFilter]);

  // Cálculos de totales
  const totals = useMemo(() => {
    return filtered.reduce((acc, r) => ({
      pim: acc.pim + (r.PIM || 0),
      dev: acc.dev + (r.DEVENGADO || 0),
      cert: acc.cert + (r.CERTIFICADO || 0),
      comp: acc.comp + (r.COMPROMISO || 0),
      prog: acc.prog + (r.TOTAL_PROG || 0)
    }), { pim: 0, dev: 0, cert: 0, comp: 0, prog: 0 });
  }, [filtered]);

  const btnStyle = (active) => ({
    padding: "8px 20px", borderRadius: "8px", border: "none", cursor: "pointer",
    background: active ? "linear-gradient(135deg, #3b82f6, #1d4ed8)" : "#1e293b",
    color: active ? "#fff" : "#94a3b8", fontSize: "11px", fontWeight: "700",
    transition: "all 0.3s ease", boxShadow: active ? "0 4px 12px rgba(59, 130, 246, 0.4)" : "none"
  });

  return (
    <div style={{ backgroundColor: "#0f172a", minHeight: "100vh", padding: "24px", color: "#e2e8f0", fontFamily: "'Inter', sans-serif" }}>
      
      {/* HEADER */}
      <div style={{ borderBottom: "1px solid #1e293b", paddingBottom: "15px", marginBottom: "25px", display: "flex", justifyContent: "space-between", alignItems: "flex-end" }}>
        <div>
          <h1 style={{ margin: 0, fontSize: "24px", fontWeight: "900", color: "#fff", letterSpacing: "-0.5px" }}>REPORT PVD — 2026</h1>
          <p style={{ margin: 0, color: "#64748b", fontSize: "13px" }}>Provías Descentralizado - Control Presupuestal</p>
        </div>
        <div style={{ textAlign: "right", fontSize: "12px", color: "#475569" }}>MTC - PERÚ</div>
      </div>

      {/* FILTROS (BOTONES) */}
      <div style={{ display: "flex", gap: "30px", marginBottom: "30px", background: "#1e293b55", padding: "15px", borderRadius: "12px" }}>
        <div>
          <div style={{ fontSize: "10px", color: "#64748b", fontWeight: "800", marginBottom: "8px" }}>TIPO DE GASTO</div>
          <div style={{ display: "flex", gap: "8px" }}>
            {["TODO", "GASTO CORRIENTE", "INVERSIÓN"].map(g => (
              <button key={g} style={btnStyle(gastoFilter === g)} onClick={() => setGastoFilter(g)}>{g}</button>
            ))}
          </div>
        </div>
        <div>
          <div style={{ fontSize: "10px", color: "#64748b", fontWeight: "800", marginBottom: "8px" }}>FUENTE DE FINANCIAMIENTO</div>
          <div style={{ display: "flex", gap: "8px" }}>
            {["TODO", "RO", "ROOC"].map(f => (
              <button key={f} style={btnStyle(ffFilter === f)} onClick={() => setFfFilter(f)}>{f}</button>
            ))}
          </div>
        </div>
      </div>

      {/* INDICADORES (GAUGES) */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: "20px", marginBottom: "30px" }}>
        <Gauge label="Devengado" value={totals.dev} total={totals.pim} color="#10b981" />
        <Gauge label="Certificado" value={totals.cert} total={totals.pim} color="#3b82f6" />
        <Gauge label="Compromiso" value={totals.comp} total={totals.pim} color="#f59e0b" />
        <div style={{ background: "linear-gradient(135deg, #1e293b, #0f172a)", padding: "20px", borderRadius: "12px", border: "1px solid #334155", display: "flex", flexDirection: "column", justifyContent: "center" }}>
          <div style={{ fontSize: "11px", color: "#64748b", fontWeight: "700" }}>PRESUPUESTO PIM</div>
          <div style={{ fontSize: "24px", fontWeight: "900", color: "#fff", marginTop: "5px" }}>{fmtFull(totals.pim)}</div>
        </div>
      </div>

      {/* TABLA DE EJECUCIÓN */}
      <div style={{ background: "#1e293b", borderRadius: "16px", padding: "20px", border: "1px solid #334155" }}>
        <h2 style={{ fontSize: "14px", fontWeight: "800", marginBottom: "20px", color: "#94a3b8" }}>EJECUCIÓN POR LÍNEA DE INTERVENCIÓN</h2>
        <div style={{ overflowX: "auto" }}>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr style={{ textAlign: "left", borderBottom: "2px solid #334155" }}>
                <th style={{ padding: "12px", fontSize: "11px", color: "#64748b" }}>NATURALEZA</th>
                <th style={{ padding: "12px", fontSize: "11px", color: "#64748b", textAlign: "right" }}>PIM</th>
                <th style={{ padding: "12px", fontSize: "11px", color: "#64748b", textAlign: "right" }}>DEVENGADO</th>
                <th style={{ padding: "12px", fontSize: "11px", color: "#64748b", textAlign: "right" }}>% AVANCE</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((r, i) => {
                const avance = r.PIM > 0 ? (r.DEVENGADO / r.PIM * 100) : 0;
                return (
                  <tr key={i} style={{ borderBottom: "1px solid #334155", fontSize: "13px" }}>
                    <td style={{ padding: "12px", fontWeight: "600" }}>{r.NATURALEZA}</td>
                    <td style={{ padding: "12px", textAlign: "right" }}>{fmtFull(r.PIM)}</td>
                    <td style={{ padding: "12px", textAlign: "right", color: "#10b981", fontWeight: "700" }}>{fmtFull(r.DEVENGADO)}</td>
                    <td style={{ padding: "12px", textAlign: "right" }}>
                      <span style={{ padding: "4px 8px", borderRadius: "6px", background: avance > 80 ? "#064e3b" : "#451a03", color: avance > 80 ? "#34d399" : "#fbbf24", fontSize: "11px", fontWeight: "800" }}>
                        {avance.toFixed(1)}%
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
