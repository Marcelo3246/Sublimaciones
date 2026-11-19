import { useLayoutEffect, useRef } from "react";
import { dinero } from "../../utils/formato";
import "./GraficoIngresos.css";

// Gráfico de barras hecho a mano con SVG (sin librerías).
// porDia = { 28: 1800, 29: 1400 } -> ingresos de cada día del mes.
// dias = cuántos días tiene el mes; mes = su número (1 a 12).
function GraficoIngresos({ porDia, dias, mes }) {
  const W = 640, H = 230, izq = 42, der = 8, arriba = 10, abajo = 28;
  const paso = 500;
  // Tope del eje: 2000 como mínimo, y si un día supera eso se redondea hacia arriba
  const max = Math.max(2000, Math.ceil(Math.max(0, ...Object.values(porDia)) / paso) * paso);
  const anchoDia = (W - izq - der) / dias;
  // Convierte un valor de dinero en su posición vertical
  const y = (valor) => arriba + (H - arriba - abajo) * (1 - valor / max);

  const guias = [];
  for (let v = 0; v <= max; v += paso) guias.push(v);

  const listaDias = Array.from({ length: dias }, (_, i) => i + 1);

  // En celular el gráfico tiene un ancho mínimo y se desliza de costado;
  // arranca con el día de hoy cerca del borde derecho, mostrando los días anteriores.
  const contenedor = useRef(null);
  useLayoutEffect(() => {
    const c = contenedor.current;
    if (!c || c.scrollWidth <= c.clientWidth) return;
    const hoy = new Date().getDate();
    const finDeHoy = ((izq + hoy * anchoDia) / W) * c.scrollWidth;
    c.scrollLeft = finDeHoy - c.clientWidth + 16;
  }, [anchoDia]);

  return (
    <div className="grafico-scroll" ref={contenedor}>
      <svg className="grafico" viewBox={`0 0 ${W} ${H}`} role="img" aria-label="Ingresos por día del mes">
        {guias.map((v) => (
          <g key={v}>
            <line className="guia" x1={izq} x2={W - der} y1={y(v)} y2={y(v)} />
            <text className="eje" x={izq - 8} y={y(v) + 4} textAnchor="end">{v}</text>
          </g>
        ))}

        {listaDias.map((dia) => {
          const valor = porDia[dia] || 0;
          const x = izq + (dia - 1) * anchoDia;
          const mostrarEtiqueta = (dia - 1) % 3 === 0 || dia === dias;
          return (
            <g key={dia}>
              {valor > 0 && (
                <rect className="barra" x={x + anchoDia * 0.15} y={y(valor)}
                  width={anchoDia * 0.7} height={y(0) - y(valor)} rx="2">
                  <title>{`${dia}/${mes}: ${dinero(valor)}`}</title>
                </rect>
              )}
              {mostrarEtiqueta && (
                <text className="eje" x={x + anchoDia / 2} y={H - 8} textAnchor="middle">
                  {String(dia).padStart(2, "0")}/{String(mes).padStart(2, "0")}
                </text>
              )}
            </g>
          );
        })}
      </svg>
    </div>
  );
}

export default GraficoIngresos;
