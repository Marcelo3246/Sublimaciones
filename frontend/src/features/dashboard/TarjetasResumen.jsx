import { dinero, plural } from "../../utils/formato";

// "mes" es el nombre del mes actual (por ejemplo "noviembre")
function TarjetasResumen({ resumen: r, mes }) {
  const nota = r.vencenManana === 1 ? "1 vence mañana"
    : r.vencenManana === 0 ? "Ninguno vence mañana"
    : `${r.vencenManana} vencen mañana`;

  const tarjetas = [
    { titulo: "Ingresos de hoy", valor: dinero(r.ingresosHoy), nota: plural(r.ventasHoy, "venta", "ventas") },
    { titulo: `Ingresos de ${mes}`, valor: dinero(r.ingresosMes), nota: plural(r.ventasMes, "venta", "ventas") },
    { titulo: "Pedidos por entregar", valor: r.pedidosPorEntregar, nota, alerta: r.pedidosPorEntregar > 0 },
    {
      titulo: `Compras de ${mes}`,
      valor: dinero(r.comprasMes),
      nota: `${plural(r.cantidadComprasMes, "compra", "compras")} a ${plural(r.proveedoresMes, "proveedor", "proveedores")}`,
    },
  ];

  return (
    <section className="kpis" aria-label="Resumen">
      {tarjetas.map((t) => (
        <article key={t.titulo} className={`kpi${t.alerta ? " alerta" : ""}`}>
          <p>{t.titulo}</p>
          <strong>{t.valor}</strong>
          <small>{t.nota}</small>
        </article>
      ))}
    </section>
  );
}

export default TarjetasResumen;
