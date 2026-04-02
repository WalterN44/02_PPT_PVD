import { useState, useMemo, useRef, useEffect } from "react";
 
const RAW = [{"GASTO":"Gasto corriente","NATURALEZA":"Emergencias en VD","FF":"RO","PIA":200000,"PIM":218344,"CERTIFICADO":218343.63,"COMPROMISO":178303.63,"DEVENGADO":178303.63,"PROG._ENERO":0,"DEV._ENERO":36000,"PROG._FEBRERO":26000,"DEV._FEBRERO":57979.6,"PROG._MARZO":26000,"DEV._MARZO":28400,"PROG._ABRIL":0,"PROG._MAYO":0,"PROG._JUNIO":8135.93,"PROG._JULIO":5000,"PROG._AGOSTO":5000,"PROG._SETIEMBRE":5000,"PROG._OCTUBRE":0,"PROG._NOVIEMBRE":0,"PROG._DICIEMBRE":52189.37,"TOTAL_PROG.":230493,"SALDO_PROG.":-12149},{"GASTO":"Gasto corriente","NATURALEZA":"Emergencias en VV","FF":"RO","PIA":6000000,"PIM":7698741,"CERTIFICADO":7626858.5,"COMPROMISO":7089895.22,"DEVENGADO":6991482.31,"PROG._ENERO":50000,"DEV._ENERO":1179000,"PROG._FEBRERO":589500,"DEV._FEBRERO":1107184.44,"PROG._MARZO":589500,"DEV._MARZO":1320201.09,"PROG._ABRIL":440000,"PROG._MAYO":50000,"PROG._JUNIO":30000,"PROG._JULIO":17410,"PROG._AGOSTO":15000,"PROG._SETIEMBRE":20000,"PROG._OCTUBRE":30000,"PROG._NOVIEMBRE":50000,"PROG._DICIEMBRE":1996382.06,"TOTAL_PROG.":8103935.78,"SALDO_PROG.":-405194.78},{"GASTO":"Gasto corriente","NATURALEZA":"Estructuras modulares","FF":"RO","PIA":0,"PIM":47080426,"CERTIFICADO":44927861.26,"COMPROMISO":1050552.3,"DEVENGADO":523562.41,"PROG._ENERO":0,"DEV._ENERO":0,"PROG._FEBRERO":0,"DEV._FEBRERO":0,"PROG._MARZO":0,"DEV._MARZO":0,"PROG._ABRIL":0,"PROG._MAYO":0,"PROG._JUNIO":0,"PROG._JULIO":6100,"PROG._AGOSTO":24000,"PROG._SETIEMBRE":53700,"PROG._OCTUBRE":351589.45,"PROG._NOVIEMBRE":331870.17,"PROG._DICIEMBRE":44807209.93,"TOTAL_PROG.":45276697.67,"SALDO_PROG.":1803728.33},{"GASTO":"Gasto corriente","NATURALEZA":"Locadores","FF":"RO","PIA":20000000,"PIM":28724517,"CERTIFICADO":28448422.67,"COMPROMISO":27061040.7,"DEVENGADO":24544987.6,"PROG._ENERO":1250100,"DEV._ENERO":1118666,"PROG._FEBRERO":2420419,"DEV._FEBRERO":1980759.57,"PROG._MARZO":3036348.33,"DEV._MARZO":3105009.26,"PROG._ABRIL":3246248.33,"PROG._MAYO":3828071.83,"PROG._JUNIO":4413648.33,"PROG._JULIO":3554600.01,"PROG._AGOSTO":3062200,"PROG._SETIEMBRE":3062400,"PROG._OCTUBRE":2872000,"PROG._NOVIEMBRE":2509330,"PROG._DICIEMBRE":2792313,"TOTAL_PROG.":26822985.74,"SALDO_PROG.":1901531.26},{"GASTO":"Gasto corriente","NATURALEZA":"Negociación Colectiva","FF":"RO","PIA":39700,"PIM":39700,"CERTIFICADO":0,"COMPROMISO":0,"DEVENGADO":0,"PROG._ENERO":0,"DEV._ENERO":0,"PROG._FEBRERO":0,"DEV._FEBRERO":0,"PROG._MARZO":0,"DEV._MARZO":0,"PROG._ABRIL":0,"PROG._MAYO":0,"PROG._JUNIO":0,"PROG._JULIO":0,"PROG._AGOSTO":0,"PROG._SETIEMBRE":0,"PROG._OCTUBRE":0,"PROG._NOVIEMBRE":0,"PROG._DICIEMBRE":39700,"TOTAL_PROG.":39700,"SALDO_PROG.":0},{"GASTO":"Gasto corriente","NATURALEZA":"Otros","FF":"RO","PIA":39173585,"PIM":22959257,"CERTIFICADO":22185204.36,"COMPROMISO":20179322.87,"DEVENGADO":16608447.39,"PROG._ENERO":794766.45,"DEV._ENERO":885814.04,"PROG._FEBRERO":1660467.67,"DEV._FEBRERO":1334184.32,"PROG._MARZO":893392.42,"DEV._MARZO":1970420.45,"PROG._ABRIL":3554715.59,"PROG._MAYO":3344921.2,"PROG._JUNIO":2106424.73,"PROG._JULIO":3060526.41,"PROG._AGOSTO":1722228.14,"PROG._SETIEMBRE":2863590.91,"PROG._OCTUBRE":2050280.89,"PROG._NOVIEMBRE":3323418.68,"PROG._DICIEMBRE":3623320.74,"TOTAL_PROG.":20052270.82,"SALDO_PROG.":2906986.18},{"GASTO":"Gasto corriente","NATURALEZA":"Planilla de Personal CAP","FF":"RO","PIA":23597485,"PIM":24573292,"CERTIFICADO":21992184.26,"COMPROMISO":21128431.38,"DEVENGADO":20467415.36,"PROG._ENERO":2469551,"DEV._ENERO":2466092.94,"PROG._FEBRERO":1294812.84,"DEV._FEBRERO":1296906.12,"PROG._MARZO":1287012.44,"DEV._MARZO":1287139.36,"PROG._ABRIL":2007780.48,"PROG._MAYO":1320200.75,"PROG._JUNIO":2528084.99,"PROG._JULIO":1328924.71,"PROG._AGOSTO":1335182.42,"PROG._SETIEMBRE":1341967.84,"PROG._OCTUBRE":1988714.34,"PROG._NOVIEMBRE":2540878.79,"PROG._DICIEMBRE":2181194.4,"TOTAL_PROG.":21396128.8,"SALDO_PROG.":3177163.2},{"GASTO":"Gasto corriente","NATURALEZA":"Planilla de Personal CAS","FF":"RO","PIA":13353231,"PIM":14139018,"CERTIFICADO":14139018,"COMPROMISO":14100786.75,"DEVENGADO":13547980.16,"PROG._ENERO":1177779,"DEV._ENERO":1214162.57,"PROG._FEBRERO":1215301.85,"DEV._FEBRERO":1194124.29,"PROG._MARZO":1137809.52,"DEV._MARZO":1168562.31,"PROG._ABRIL":1190922.89,"PROG._MAYO":1147538.13,"PROG._JUNIO":1114806.24,"PROG._JULIO":1205509.72,"PROG._AGOSTO":1139613,"PROG._SETIEMBRE":1125777.56,"PROG._OCTUBRE":1142381.25,"PROG._NOVIEMBRE":1188306.92,"PROG._DICIEMBRE":1239986.72,"TOTAL_PROG.":13928691.85,"SALDO_PROG.":210326.15},{"GASTO":"Gasto corriente","NATURALEZA":"Proregión I","FF":"RO","PIA":409586000,"PIM":409161591,"CERTIFICADO":409125766.33,"COMPROMISO":406310311.87,"DEVENGADO":399756129.42,"PROG._ENERO":13952105.04,"DEV._ENERO":20987435.53,"PROG._FEBRERO":19857412.85,"DEV._FEBRERO":41531135.87,"PROG._MARZO":24164516.93,"DEV._MARZO":17522182.09,"PROG._ABRIL":23998399.25,"PROG._MAYO":22501074.08,"PROG._JUNIO":24499344.71,"PROG._JULIO":45348759.6,"PROG._AGOSTO":38830173.31,"PROG._SETIEMBRE":46363934.8,"PROG._OCTUBRE":65781929.25,"PROG._NOVIEMBRE":38223456.92,"PROG._DICIEMBRE":62710572.27,"TOTAL_PROG.":458906340.29,"SALDO_PROG.":-49744749.29},{"GASTO":"Gasto corriente","NATURALEZA":"Proregión II","FF":"RO","PIA":0,"PIM":14367259,"CERTIFICADO":14178777,"COMPROMISO":0,"DEVENGADO":0,"PROG._ENERO":0,"DEV._ENERO":0,"PROG._FEBRERO":0,"DEV._FEBRERO":0,"PROG._MARZO":0,"DEV._MARZO":0,"PROG._ABRIL":0,"PROG._MAYO":0,"PROG._JUNIO":0,"PROG._JULIO":0,"PROG._AGOSTO":0,"PROG._SETIEMBRE":0,"PROG._OCTUBRE":0,"PROG._NOVIEMBRE":0,"PROG._DICIEMBRE":0,"TOTAL_PROG.":0,"SALDO_PROG.":14367259},{"GASTO":"Gasto corriente","NATURALEZA":"Puente modulares PLIA","FF":"RO","PIA":0,"PIM":36306746,"CERTIFICADO":31697763.03,"COMPROMISO":1190418.18,"DEVENGADO":759856.46,"PROG._ENERO":0,"DEV._ENERO":0,"PROG._FEBRERO":0,"DEV._FEBRERO":0,"PROG._MARZO":0,"DEV._MARZO":0,"PROG._ABRIL":0,"PROG._MAYO":0,"PROG._JUNIO":344400,"PROG._JULIO":7100,"PROG._AGOSTO":105500,"PROG._SETIEMBRE":351000,"PROG._OCTUBRE":406148.99,"PROG._NOVIEMBRE":306237.1,"PROG._DICIEMBRE":33494708.69,"TOTAL_PROG.":34228345.38,"SALDO_PROG.":2078400.62},{"GASTO":"Gasto corriente","NATURALEZA":"Reconstrucción con Cambios","FF":"RO","PIA":0,"PIM":11579,"CERTIFICADO":10178.17,"COMPROMISO":5230.75,"DEVENGADO":4557.94,"PROG._ENERO":3000,"DEV._ENERO":640,"PROG._FEBRERO":0,"DEV._FEBRERO":647.19,"PROG._MARZO":860,"DEV._MARZO":3018.17,"PROG._ABRIL":0,"PROG._MAYO":0,"PROG._JUNIO":0,"PROG._JULIO":0,"PROG._AGOSTO":752,"PROG._SETIEMBRE":0,"PROG._OCTUBRE":0,"PROG._NOVIEMBRE":10268,"PROG._DICIEMBRE":0,"TOTAL_PROG.":4557.94,"SALDO_PROG.":7021.06},{"GASTO":"Gasto corriente","NATURALEZA":"Sentencias judiciales","FF":"RO","PIA":0,"PIM":795774,"CERTIFICADO":795593.14,"COMPROMISO":669089.03,"DEVENGADO":669089.03,"PROG._ENERO":0,"DEV._ENERO":0,"PROG._FEBRERO":0,"DEV._FEBRERO":0,"PROG._MARZO":0,"DEV._MARZO":0,"PROG._ABRIL":0,"PROG._MAYO":0,"PROG._JUNIO":0,"PROG._JULIO":0,"PROG._AGOSTO":0,"PROG._SETIEMBRE":0,"PROG._OCTUBRE":0,"PROG._NOVIEMBRE":0,"PROG._DICIEMBRE":2534373,"TOTAL_PROG.":3203462.03,"SALDO_PROG.":-2407688.03},{"GASTO":"Gasto corriente","NATURALEZA":"Zonales","FF":"RO","PIA":0,"PIM":3632649,"CERTIFICADO":2989786.93,"COMPROMISO":2957323.23,"DEVENGADO":2663615.25,"PROG._ENERO":209238,"DEV._ENERO":15346.8,"PROG._FEBRERO":237316,"DEV._FEBRERO":263710.8,"PROG._MARZO":237316,"DEV._MARZO":338647.84,"PROG._ABRIL":274745.5,"PROG._MAYO":409798.04,"PROG._JUNIO":356155.48,"PROG._JULIO":394381.18,"PROG._AGOSTO":370160.08,"PROG._SETIEMBRE":404149.48,"PROG._OCTUBRE":347508.98,"PROG._NOVIEMBRE":296935.35,"PROG._DICIEMBRE":215749.09,"TOTAL_PROG.":2834446.35,"SALDO_PROG.":798202.65},{"GASTO":"Inversión","NATURALEZA":"Inversión PATS","FF":"RO","PIA":256816891,"PIM":171587749,"CERTIFICADO":158905906.5,"COMPROMISO":152263165.48,"DEVENGADO":147119884.29,"PROG._ENERO":391589.03,"DEV._ENERO":814880.51,"PROG._FEBRERO":2618261.71,"DEV._FEBRERO":367535.06,"PROG._MARZO":2583681.1,"DEV._MARZO":3690976.92,"PROG._ABRIL":6233095.49,"PROG._MAYO":8708124.62,"PROG._JUNIO":14843656.77,"PROG._JULIO":14656960.98,"PROG._AGOSTO":15998712.22,"PROG._SETIEMBRE":17162161.69,"PROG._OCTUBRE":21722686.52,"PROG._NOVIEMBRE":19654619.89,"PROG._DICIEMBRE":20132673.53,"TOTAL_PROG.":166669715.96,"SALDO_PROG.":4918033.04},{"GASTO":"Inversión","NATURALEZA":"Inversión Proregión 1","FF":"RO","PIA":30966313,"PIM":34036490,"CERTIFICADO":29570875.78,"COMPROMISO":28570099.67,"DEVENGADO":25066004.47,"PROG._ENERO":2851342.73,"DEV._ENERO":2419491.51,"PROG._FEBRERO":3725436.43,"DEV._FEBRERO":2942327.39,"PROG._MARZO":2590600.59,"DEV._MARZO":2150338.69,"PROG._ABRIL":1934782,"PROG._MAYO":1294840,"PROG._JUNIO":999143,"PROG._JULIO":1229690,"PROG._AGOSTO":944910,"PROG._SETIEMBRE":3285412.24,"PROG._OCTUBRE":1468968.33,"PROG._NOVIEMBRE":1516727.86,"PROG._DICIEMBRE":4138301.11,"TOTAL_PROG.":28890007.04,"SALDO_PROG.":5146482.96},{"GASTO":"Inversión","NATURALEZA":"Inversión Proregión 1","FF":"ROOC","PIA":194741714,"PIM":233548229,"CERTIFICADO":134987466.46,"COMPROMISO":123741779.54,"DEVENGADO":120835868.88,"PROG._ENERO":26073887.44,"DEV._ENERO":8806494.29,"PROG._FEBRERO":35273622.16,"DEV._FEBRERO":32324109.64,"PROG._MARZO":7031577.02,"DEV._MARZO":8801565.01,"PROG._ABRIL":10157210.06,"PROG._MAYO":4036096.56,"PROG._JUNIO":19487107.11,"PROG._JULIO":10735019.67,"PROG._AGOSTO":6416218.23,"PROG._SETIEMBRE":6447570.3,"PROG._OCTUBRE":8457815.93,"PROG._NOVIEMBRE":2104130.25,"PROG._DICIEMBRE":21228382.61,"TOTAL_PROG.":142059451.49,"SALDO_PROG.":91488777.51},{"GASTO":"Inversión","NATURALEZA":"Inversión Proregión 2","FF":"RO","PIA":6013053,"PIM":5813053,"CERTIFICADO":4475570.13,"COMPROMISO":4317888.3,"DEVENGADO":3211076.9,"PROG._ENERO":9000,"DEV._ENERO":9000,"PROG._FEBRERO":135000,"DEV._FEBRERO":47798.13,"PROG._MARZO":99000,"DEV._MARZO":34701.4,"PROG._ABRIL":263500,"PROG._MAYO":333500,"PROG._JUNIO":1006831.85,"PROG._JULIO":143767,"PROG._AGOSTO":590195.56,"PROG._SETIEMBRE":207267,"PROG._OCTUBRE":352767,"PROG._NOVIEMBRE":1471981.24,"PROG._DICIEMBRE":903681.95,"TOTAL_PROG.":4087397.05,"SALDO_PROG.":1725655.95},{"GASTO":"Inversión","NATURALEZA":"Inversión Proregión 2","FF":"ROOC","PIA":3105300,"PIM":3105300,"CERTIFICADO":0,"COMPROMISO":0,"DEVENGADO":0,"PROG._ENERO":0,"DEV._ENERO":0,"PROG._FEBRERO":0,"DEV._FEBRERO":0,"PROG._MARZO":0,"DEV._MARZO":0,"PROG._ABRIL":0,"PROG._MAYO":10000,"PROG._JUNIO":0,"PROG._JULIO":0,"PROG._AGOSTO":0,"PROG._SETIEMBRE":0,"PROG._OCTUBRE":0,"PROG._NOVIEMBRE":0,"PROG._DICIEMBRE":40000,"TOTAL_PROG.":40000,"SALDO_PROG.":3065300},{"GASTO":"Inversión","NATURALEZA":"OXI","FF":"RO","PIA":4244955,"PIM":358814,"CERTIFICADO":175368.42,"COMPROMISO":161768.85,"DEVENGADO":151666.37,"PROG._ENERO":0,"DEV._ENERO":0,"PROG._FEBRERO":0,"DEV._FEBRERO":0,"PROG._MARZO":0,"DEV._MARZO":0,"PROG._ABRIL":0,"PROG._MAYO":87390.1,"PROG._JUNIO":91872.42,"PROG._JULIO":20750,"PROG._AGOSTO":0,"PROG._SETIEMBRE":2800,"PROG._OCTUBRE":106667.15,"PROG._NOVIEMBRE":48717.52,"PROG._DICIEMBRE":57950,"TOTAL_PROG.":209616.37,"SALDO_PROG.":149197.63},{"GASTO":"Inversión","NATURALEZA":"Programática","FF":"RO","PIA":227873188,"PIM":304027103,"CERTIFICADO":301693429.37,"COMPROMISO":293244516.06,"DEVENGADO":281502762.95,"PROG._ENERO":9181658.45,"DEV._ENERO":16064267.78,"PROG._FEBRERO":13293015.83,"DEV._FEBRERO":15260511.01,"PROG._MARZO":20313679.47,"DEV._MARZO":22013352.97,"PROG._ABRIL":62192935.27,"PROG._MAYO":30799228,"PROG._JUNIO":33780323.48,"PROG._JULIO":14483802.61,"PROG._AGOSTO":33126839.74,"PROG._SETIEMBRE":18431349.57,"PROG._OCTUBRE":34825657.2,"PROG._NOVIEMBRE":28784356.02,"PROG._DICIEMBRE":46935982.64,"TOTAL_PROG.":328213074.28,"SALDO_PROG.":-24185971.28},{"GASTO":"Inversión","NATURALEZA":"Programática","FF":"ROOC","PIA":0,"PIM":0,"CERTIFICADO":0,"COMPROMISO":0,"DEVENGADO":0,"PROG._ENERO":0,"DEV._ENERO":0,"PROG._FEBRERO":0,"DEV._FEBRERO":0,"PROG._MARZO":0,"DEV._MARZO":0,"PROG._ABRIL":0,"PROG._MAYO":0,"PROG._JUNIO":0,"PROG._JULIO":0,"PROG._AGOSTO":0,"PROG._SETIEMBRE":0,"PROG._OCTUBRE":0,"PROG._NOVIEMBRE":0,"PROG._DICIEMBRE":0,"TOTAL_PROG.":0,"SALDO_PROG.":0},{"GASTO":"Inversión","NATURALEZA":"Puentes emergencia-IOARR","FF":"RO","PIA":0,"PIM":7901675,"CERTIFICADO":7093117.27,"COMPROMISO":7015785.87,"DEVENGADO":6690422.04,"PROG._ENERO":0,"DEV._ENERO":33495.88,"PROG._FEBRERO":38409.76,"DEV._FEBRERO":3384.11,"PROG._MARZO":220871.5,"DEV._MARZO":124323.19,"PROG._ABRIL":1438109.46,"PROG._MAYO":822504.63,"PROG._JUNIO":329383.37,"PROG._JULIO":674291.54,"PROG._AGOSTO":572062,"PROG._SETIEMBRE":682146,"PROG._OCTUBRE":800750.11,"PROG._NOVIEMBRE":2635750.11,"PROG._DICIEMBRE":4778645.68,"TOTAL_PROG.":9007578.42,"SALDO_PROG.":-1105903.42},{"GASTO":"Inversión","NATURALEZA":"Puentes modulares-IOARR","FF":"RO","PIA":9041109,"PIM":4092537,"CERTIFICADO":3839742.04,"COMPROMISO":3815266.58,"DEVENGADO":3408054.5,"PROG._ENERO":0,"DEV._ENERO":0,"PROG._FEBRERO":500000,"DEV._FEBRERO":0,"PROG._MARZO":312300,"DEV._MARZO":630992.57,"PROG._ABRIL":207000,"PROG._MAYO":601242,"PROG._JUNIO":300000,"PROG._JULIO":200000,"PROG._AGOSTO":288654,"PROG._SETIEMBRE":488630,"PROG._OCTUBRE":566252,"PROG._NOVIEMBRE":424101,"PROG._DICIEMBRE":481579,"TOTAL_PROG.":3889633.5,"SALDO_PROG.":202903.5},{"GASTO":"Inversión","NATURALEZA":"RCC","FF":"RO","PIA":0,"PIM":34338088,"CERTIFICADO":30021903.28,"COMPROMISO":28422141.06,"DEVENGADO":27063919.5,"PROG._ENERO":1355000,"DEV._ENERO":0,"PROG._FEBRERO":1276626.5,"DEV._FEBRERO":3041365.29,"PROG._MARZO":1185582.64,"DEV._MARZO":237346.58,"PROG._ABRIL":4338275.63,"PROG._MAYO":3101570.36,"PROG._JUNIO":5578391.82,"PROG._JULIO":3138387.73,"PROG._AGOSTO":4164130.97,"PROG._SETIEMBRE":3553431.89,"PROG._OCTUBRE":3234823.65,"PROG._NOVIEMBRE":2323761.41,"PROG._DICIEMBRE":1158000.75,"TOTAL_PROG.":28162895.49,"SALDO_PROG.":6175192.51},{"GASTO":"Inversión","NATURALEZA":"RCC","FF":"ROOC","PIA":0,"PIM":20133667,"CERTIFICADO":18301375.44,"COMPROMISO":15616575.72,"DEVENGADO":13683343.06,"PROG._ENERO":436000,"DEV._ENERO":0,"PROG._FEBRERO":1290000,"DEV._FEBRERO":1752925.26,"PROG._MARZO":3854500,"DEV._MARZO":1510350.85,"PROG._ABRIL":3808105,"PROG._MAYO":414139.65,"PROG._JUNIO":430339.78,"PROG._JULIO":1317969.3,"PROG._AGOSTO":978096.6,"PROG._SETIEMBRE":525903.92,"PROG._OCTUBRE":459573.96,"PROG._NOVIEMBRE":1184625,"PROG._DICIEMBRE":3412068.38,"TOTAL_PROG.":16718385.17,"SALDO_PROG.":3415281.83}];
 
const MESES = ["ENERO","FEBRERO","MARZO","ABRIL","MAYO","JUNIO","JULIO","AGOSTO","SETIEMBRE","OCTUBRE","NOVIEMBRE","DICIEMBRE"];
const MESES_SHORT = ["ENE","FEB","MAR","ABR","MAY","JUN","JUL","AGO","SET","OCT","NOV","DIC"];
 
const fmt = (n) => {
  if (n == null || isNaN(n)) return "0";
  const abs = Math.abs(n);
  if (abs >= 1e9) return (n/1e9).toFixed(2) + " MM";
  if (abs >= 1e6) return (n/1e6).toFixed(1) + " M";
  if (abs >= 1e3) return (n/1e3).toFixed(1) + " K";
  return n.toFixed(0);
};
 
const fmtFull = (n) => {
  if (n == null || isNaN(n)) return "S/ 0";
  return "S/ " + Math.round(n).toLocaleString("es-PE");
};
 
const pct = (part, total) => total === 0 ? 0 : (part / total * 100);
 
// Donut Chart SVG
function DonutChart({ data, size = 180, thickness = 28, colors, title }) {
  const total = data.reduce((s, d) => s + d.value, 0);
  let cumulative = 0;
  const radius = (size - thickness) / 2;
  const cx = size / 2, cy = size / 2;
 
  const arcs = data.map((d, i) => {
    const startAngle = (cumulative / total) * 2 * Math.PI - Math.PI / 2;
    cumulative += d.value;
    const endAngle = (cumulative / total) * 2 * Math.PI - Math.PI / 2;
    const largeArc = endAngle - startAngle > Math.PI ? 1 : 0;
    const x1 = cx + radius * Math.cos(startAngle);
    const y1 = cy + radius * Math.sin(startAngle);
    const x2 = cx + radius * Math.cos(endAngle);
    const y2 = cy + radius * Math.sin(endAngle);
    return { d: `M ${x1} ${y1} A ${radius} ${radius} 0 ${largeArc} 1 ${x2} ${y2}`, color: colors[i], label: d.label, value: d.value, pct: pct(d.value, total) };
  });
 
  return (
    <div style={{ textAlign: "center" }}>
      <div style={{ fontSize: 11, fontWeight: 700, color: "#94a3b8", textTransform: "uppercase", letterSpacing: 1.5, marginBottom: 8 }}>{title}</div>
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        <circle cx={cx} cy={cy} r={radius} fill="none" stroke="#1e293b" strokeWidth={thickness} />
        {arcs.map((a, i) => (
          <path key={i} d={a.d} fill="none" stroke={a.color} strokeWidth={thickness} strokeLinecap="butt" />
        ))}
        <text x={cx} y={cy - 8} textAnchor="middle" fill="#e2e8f0" fontSize="13" fontWeight="700">{fmtFull(total)}</text>
        <text x={cx} y={cy + 10} textAnchor="middle" fill="#64748b" fontSize="10">PIM TOTAL</text>
      </svg>
      <div style={{ display: "flex", justifyContent: "center", gap: 16, marginTop: 6 }}>
        {arcs.map((a, i) => (
          <div key={i} style={{ fontSize: 10, color: "#cbd5e1" }}>
            <span style={{ display: "inline-block", width: 10, height: 10, borderRadius: 2, background: a.color, marginRight: 4, verticalAlign: "middle" }} />
            {a.label}: {a.pct.toFixed(1)}%
          </div>
        ))}
      </div>
    </div>
  );
}
 
// Gauge (semicircle)
function Gauge({ value, total, label, color, size = 140 }) {
  const percentage = total === 0 ? 0 : Math.min(value / total, 1);
  const radius = (size - 20) / 2;
  const cx = size / 2, cy = size / 2 + 10;
  const startAngle = Math.PI;
  const endAngle = startAngle + Math.PI * percentage;
  const x1 = cx + radius * Math.cos(startAngle);
  const y1 = cy + radius * Math.sin(startAngle);
  const x2 = cx + radius * Math.cos(endAngle);
  const y2 = cy + radius * Math.sin(endAngle);
  const largeArc = percentage > 0.5 ? 1 : 0;
 
  return (
    <div style={{ textAlign: "center" }}>
      <svg width={size} height={size * 0.6} viewBox={`0 0 ${size} ${size * 0.65}`}>
        <path d={`M ${cx - radius} ${cy} A ${radius} ${radius} 0 0 1 ${cx + radius} ${cy}`} fill="none" stroke="#1e293b" strokeWidth={12} strokeLinecap="round" />
        {percentage > 0 && (
          <path d={`M ${x1} ${y1} A ${radius} ${radius} 0 ${largeArc} 1 ${x2} ${y2}`} fill="none" stroke={color} strokeWidth={12} strokeLinecap="round" />
        )}
        <text x={cx} y={cy - 12} textAnchor="middle" fill="#e2e8f0" fontSize="16" fontWeight="800">{(percentage * 100).toFixed(1)}%</text>
        <text x={cx} y={cy + 2} textAnchor="middle" fill="#64748b" fontSize="9">{fmt(value)}</text>
      </svg>
      <div style={{ fontSize: 10, fontWeight: 700, color, textTransform: "uppercase", letterSpacing: 1, marginTop: -4 }}>{label}</div>
    </div>
  );
}
 
// Bar chart
function BarChart({ progData, devData, maxVal, height = 260 }) {
  const barW = 28;
  const gap = 12;
  const groupW = barW * 2 + gap;
  const totalW = MESES_SHORT.length * groupW + (MESES_SHORT.length - 1) * 8;
  const chartH = height - 40;
 
  return (
    <div style={{ overflowX: "auto", paddingBottom: 4 }}>
      <svg width={Math.max(totalW + 60, 500)} height={height} viewBox={`0 0 ${Math.max(totalW + 60, 500)} ${height}`}>
        {[0, 0.25, 0.5, 0.75, 1].map((f, i) => (
          <g key={i}>
            <line x1={40} y1={chartH * (1 - f) + 10} x2={totalW + 50} y2={chartH * (1 - f) + 10} stroke="#1e293b" strokeWidth={1} />
            <text x={36} y={chartH * (1 - f) + 14} textAnchor="end" fill="#475569" fontSize="8">{fmt(maxVal * f)}</text>
          </g>
        ))}
        {MESES_SHORT.map((m, i) => {
          const x = 44 + i * (groupW + 8);
          const progH = maxVal > 0 ? (progData[i] / maxVal) * chartH : 0;
          const devH = maxVal > 0 ? (devData[i] / maxVal) * chartH : 0;
          return (
            <g key={i}>
              <rect x={x} y={chartH - progH + 10} width={barW} height={progH} rx={3} fill="#3b82f6" opacity={0.85} />
              <rect x={x + barW + 2} y={chartH - devH + 10} width={barW} height={devH} rx={3} fill="#f59e0b" opacity={0.9} />
              <text x={x + barW} y={chartH + 26} textAnchor="middle" fill="#94a3b8" fontSize="8" fontWeight="600">{m}</text>
            </g>
          );
        })}
      </svg>
      <div style={{ display: "flex", gap: 20, justifyContent: "center", marginTop: 4 }}>
        <span style={{ fontSize: 10, color: "#3b82f6" }}>■ Programación</span>
        <span style={{ fontSize: 10, color: "#f59e0b" }}>■ Devengado</span>
      </div>
    </div>
  );
}
 
export default function Dashboard() {
  const [gastoFilter, setGastoFilter] = useState("TODO");
  const [ffFilter, setFfFilter] = useState("TODO");
 
  const filtered = useMemo(() => {
    let d = RAW;
    if (gastoFilter === "INVERSIÓN") d = d.filter(r => r.GASTO === "Inversión");
    else if (gastoFilter === "GASTO CORRIENTE") d = d.filter(r => r.GASTO === "Gasto corriente");
    if (ffFilter === "RO") d = d.filter(r => r.FF === "RO");
    else if (ffFilter === "ROOC") d = d.filter(r => r.FF === "ROOC");
    return d;
  }, [gastoFilter, ffFilter]);
 
  const totals = useMemo(() => {
    const sum = (key) => filtered.reduce((s, r) => s + (r[key] || 0), 0);
    return { PIA: sum("PIA"), PIM: sum("PIM"), CERTIFICADO: sum("CERTIFICADO"), COMPROMISO: sum("COMPROMISO"), DEVENGADO: sum("DEVENGADO"), TOTAL_PROG: sum("TOTAL_PROG."), SALDO_PROG: sum("SALDO_PROG.") };
  }, [filtered]);
 
  const pimByGasto = useMemo(() => {
    const inv = filtered.filter(r => r.GASTO === "Inversión").reduce((s, r) => s + r.PIM, 0);
    const gc = filtered.filter(r => r.GASTO === "Gasto corriente").reduce((s, r) => s + r.PIM, 0);
    return { inv, gc };
  }, [filtered]);
 
  const pimByFF = useMemo(() => {
    const ro = filtered.filter(r => r.FF === "RO").reduce((s, r) => s + r.PIM, 0);
    const rooc = filtered.filter(r => r.FF === "ROOC").reduce((s, r) => s + r.PIM, 0);
    return { ro, rooc };
  }, [filtered]);
 
  const monthlyData = useMemo(() => {
    const prog = MESES.map((m) => filtered.reduce((s, r) => s + (r[`PROG._${m}`] || 0), 0));
    const dev = MESES.map((m) => {
      const key = `DEV._${m}`;
      return filtered.reduce((s, r) => s + (r[key] || 0), 0);
    });
    const maxVal = Math.max(...prog, ...dev) * 1.15;
    return { prog, dev, maxVal };
  }, [filtered]);
 
  // Table data grouped by naturaleza
  const tableData = useMemo(() => {
    const groups = {};
    filtered.forEach(r => {
      const key = r.NATURALEZA;
      if (!groups[key]) groups[key] = { NATURALEZA: key, GASTO: r.GASTO, PIM: 0, CERTIFICADO: 0, COMPROMISO: 0, DEVENGADO: 0 };
      groups[key].PIM += r.PIM;
      groups[key].CERTIFICADO += r.CERTIFICADO;
      groups[key].COMPROMISO += r.COMPROMISO;
      groups[key].DEVENGADO += r.DEVENGADO;
    });
    return Object.values(groups).sort((a, b) => b.PIM - a.PIM);
  }, [filtered]);
 
  const btnStyle = (active) => ({
    padding: "7px 18px",
    borderRadius: 6,
    border: "1px solid " + (active ? "#3b82f6" : "#334155"),
    background: active ? "linear-gradient(135deg, #1e40af, #3b82f6)" : "transparent",
    color: active ? "#fff" : "#94a3b8",
    fontSize: 11,
    fontWeight: 700,
    cursor: "pointer",
    letterSpacing: 0.8,
    transition: "all 0.2s",
    textTransform: "uppercase"
  });
 
  return (
    <div style={{ background: "linear-gradient(180deg, #0c1222 0%, #0f172a 100%)", minHeight: "100vh", color: "#e2e8f0", fontFamily: "'Segoe UI', 'Helvetica Neue', sans-serif", padding: "16px 20px" }}>
      {/* Header */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 20, borderBottom: "1px solid #1e293b", paddingBottom: 14 }}>
        <div>
          <h1 style={{ margin: 0, fontSize: 20, fontWeight: 800, background: "linear-gradient(90deg, #60a5fa, #a78bfa)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}>REPORTE PVD — 2026</h1>
          <div style={{ fontSize: 11, color: "#64748b", marginTop: 2 }}>Provías Descentralizado · Ejecución de Inversiones y Gasto Corriente</div>
        </div>
        <div style={{ fontSize: 10, color: "#475569", textAlign: "right" }}>
          <div>Ministerio de Transportes</div>
          <div>y Comunicaciones</div>
        </div>
      </div>
 
      {/* Filter buttons */}
      <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginBottom: 18, alignItems: "center" }}>
        <span style={{ fontSize: 10, color: "#64748b", fontWeight: 700, marginRight: 4 }}>TIPO DE GASTO:</span>
        {["TODO", "INVERSIÓN", "GASTO CORRIENTE"].map(g => (
          <button key={g} style={btnStyle(gastoFilter === g)} onClick={() => setGastoFilter(g)}>{g}</button>
        ))}
        <span style={{ fontSize: 10, color: "#64748b", fontWeight: 700, marginLeft: 16, marginRight: 4 }}>FUENTE:</span>
        {["TODO", "RO", "ROOC"].map(f => (
          <button key={f} style={btnStyle(ffFilter === f)} onClick={() => setFfFilter(f)}>{f}</button>
        ))}
      </div>
 
      {/* KPI Cards */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))", gap: 10, marginBottom: 18 }}>
        {[
          { label: "PIA", value: totals.PIA, color: "#6366f1" },
          { label: "PIM", value: totals.PIM, color: "#3b82f6" },
          { label: "Certificado", value: totals.CERTIFICADO, color: "#06b6d4" },
          { label: "Compromiso", value: totals.COMPROMISO, color: "#f59e0b" },
          { label: "Devengado", value: totals.DEVENGADO, color: "#10b981" },
          { label: "Programado", value: totals.TOTAL_PROG, color: "#8b5cf6" },
        ].map((kpi) => (
          <div key={kpi.label} style={{ background: "#1e293b", borderRadius: 8, padding: "12px 14px", borderLeft: `3px solid ${kpi.color}` }}>
            <div style={{ fontSize: 9, color: "#94a3b8", fontWeight: 700, textTransform: "uppercase", letterSpacing: 1.2 }}>{kpi.label}</div>
            <div style={{ fontSize: 16, fontWeight: 800, color: kpi.color, marginTop: 4 }}>{fmt(kpi.value)}</div>
            <div style={{ fontSize: 9, color: "#475569", marginTop: 2 }}>{fmtFull(kpi.value)}</div>
          </div>
        ))}
      </div>
 
      {/* Row: Donut + Gauges */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr 1fr 1fr", gap: 12, marginBottom: 18, alignItems: "center" }}>
        <div style={{ background: "#1e293b", borderRadius: 10, padding: 16, gridColumn: "span 1" }}>
          <DonutChart
            data={[{ label: "RO", value: pimByFF.ro }, { label: "ROOC", value: pimByFF.rooc }]}
            colors={["#3b82f6", "#f59e0b"]}
            title="Fuente de Financiamiento"
            size={160}
          />
        </div>
        <div style={{ background: "#1e293b", borderRadius: 10, padding: 16, gridColumn: "span 1" }}>
          <DonutChart
            data={[{ label: "Inversión", value: pimByGasto.inv }, { label: "G. Corriente", value: pimByGasto.gc }]}
            colors={["#8b5cf6", "#06b6d4"]}
            title="Tipo de Gasto"
            size={160}
          />
        </div>
        <div style={{ background: "#1e293b", borderRadius: 10, padding: 14 }}>
          <Gauge value={totals.DEVENGADO} total={totals.PIM} label="Devengado" color="#10b981" size={150} />
        </div>
        <div style={{ background: "#1e293b", borderRadius: 10, padding: 14 }}>
          <Gauge value={totals.CERTIFICADO} total={totals.PIM} label="Certificado" color="#06b6d4" size={150} />
        </div>
        <div style={{ background: "#1e293b", borderRadius: 10, padding: 14 }}>
          <Gauge value={totals.COMPROMISO} total={totals.PIM} label="Compromiso" color="#f59e0b" size={150} />
        </div>
      </div>
 
      {/* Bar Chart: Programación y Ejecución */}
      <div style={{ background: "#1e293b", borderRadius: 10, padding: 16, marginBottom: 18 }}>
        <div style={{ fontSize: 12, fontWeight: 700, color: "#94a3b8", textTransform: "uppercase", letterSpacing: 1.2, marginBottom: 10 }}>
          Programación y Ejecución Mensual 2026
        </div>
        <BarChart progData={monthlyData.prog} devData={monthlyData.dev} maxVal={monthlyData.maxVal} />
      </div>
 
      {/* Table: Ejecución por Línea de Intervención */}
      <div style={{ background: "#1e293b", borderRadius: 10, padding: 16, overflowX: "auto" }}>
        <div style={{ fontSize: 12, fontWeight: 700, color: "#94a3b8", textTransform: "uppercase", letterSpacing: 1.2, marginBottom: 10 }}>
          Ejecución por Línea de Intervención
        </div>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 10 }}>
          <thead>
            <tr style={{ borderBottom: "2px solid #334155" }}>
              <th style={{ textAlign: "left", padding: "8px 6px", color: "#64748b", fontWeight: 700, fontSize: 9 }}>NATURALEZA</th>
              <th style={{ textAlign: "left", padding: "8px 6px", color: "#64748b", fontWeight: 700, fontSize: 9 }}>GASTO</th>
              <th style={{ textAlign: "right", padding: "8px 6px", color: "#64748b", fontWeight: 700, fontSize: 9 }}>PIM</th>
              <th style={{ textAlign: "right", padding: "8px 6px", color: "#64748b", fontWeight: 700, fontSize: 9 }}>CERTIFICADO</th>
              <th style={{ textAlign: "right", padding: "8px 6px", color: "#64748b", fontWeight: 700, fontSize: 9 }}>COMPROMISO</th>
              <th style={{ textAlign: "right", padding: "8px 6px", color: "#64748b", fontWeight: 700, fontSize: 9 }}>DEVENGADO</th>
              <th style={{ textAlign: "right", padding: "8px 6px", color: "#64748b", fontWeight: 700, fontSize: 9 }}>% EJEC.</th>
            </tr>
          </thead>
          <tbody>
            {tableData.map((r, i) => {
              const ejec = r.PIM > 0 ? (r.DEVENGADO / r.PIM * 100) : 0;
              const barColor = ejec > 70 ? "#10b981" : ejec > 40 ? "#f59e0b" : "#ef4444";
              return (
                <tr key={i} style={{ borderBottom: "1px solid #1e293b", background: i % 2 === 0 ? "transparent" : "#0f172a33" }}>
                  <td style={{ padding: "7px 6px", color: "#cbd5e1", maxWidth: 200, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>{r.NATURALEZA}</td>
                  <td style={{ padding: "7px 6px", color: r.GASTO === "Inversión" ? "#8b5cf6" : "#06b6d4", fontSize: 9 }}>{r.GASTO === "Inversión" ? "INV" : "GC"}</td>
                  <td style={{ padding: "7px 6px", textAlign: "right", color: "#e2e8f0", fontWeight: 600 }}>{fmt(r.PIM)}</td>
                  <td style={{ padding: "7px 6px", textAlign: "right", color: "#06b6d4" }}>{fmt(r.CERTIFICADO)}</td>
                  <td style={{ padding: "7px 6px", textAlign: "right", color: "#f59e0b" }}>{fmt(r.COMPROMISO)}</td>
                  <td style={{ padding: "7px 6px", textAlign: "right", color: "#10b981" }}>{fmt(r.DEVENGADO)}</td>
                  <td style={{ padding: "7px 6px", textAlign: "right" }}>
                    <div style={{ display: "flex", alignItems: "center", justifyContent: "flex-end", gap: 6 }}>
                      <div style={{ width: 50, height: 5, background: "#0f172a", borderRadius: 3, overflow: "hidden" }}>
                        <div style={{ width: `${Math.min(ejec, 100)}%`, height: "100%", background: barColor, borderRadius: 3 }} />
                      </div>
                      <span style={{ color: barColor, fontWeight: 700, minWidth: 35, textAlign: "right" }}>{ejec.toFixed(1)}%</span>
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
          <tfoot>
            <tr style={{ borderTop: "2px solid #3b82f6", fontWeight: 800 }}>
              <td style={{ padding: "8px 6px", color: "#e2e8f0" }} colSpan={2}>TOTAL</td>
              <td style={{ padding: "8px 6px", textAlign: "right", color: "#e2e8f0" }}>{fmt(totals.PIM)}</td>
              <td style={{ padding: "8px 6px", textAlign: "right", color: "#06b6d4" }}>{fmt(totals.CERTIFICADO)}</td>
              <td style={{ padding: "8px 6px", textAlign: "right", color: "#f59e0b" }}>{fmt(totals.COMPROMISO)}</td>
              <td style={{ padding: "8px 6px", textAlign: "right", color: "#10b981" }}>{fmt(totals.DEVENGADO)}</td>
              <td style={{ padding: "8px 6px", textAlign: "right", color: "#3b82f6", fontWeight: 800 }}>{totals.PIM > 0 ? (totals.DEVENGADO / totals.PIM * 100).toFixed(1) : 0}%</td>
            </tr>
          </tfoot>
        </table>
      </div>
 
      <div style={{ textAlign: "center", fontSize: 9, color: "#334155", marginTop: 16, paddingBottom: 10 }}>
        Provías Descentralizado — MTC · Datos embebidos desde CONSOLIDADO · Filtros sincronizados
      </div>
    </div>
  );
}
