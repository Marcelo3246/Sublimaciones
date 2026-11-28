import { EstadoVacio } from "../../../components/Panel";
import { dinero, diasHasta, fechaCorta } from "../../../utils/formato";

const celda = "px-6 py-3 max-[860px]:px-4";
const cabecera = `${celda} bg-superficie-suave py-2 text-xs font-medium whitespace-nowrap text-texto-secundario`;

/** Etiqueta de la fecha de compromiso: atrasado en rojo, hoy o mañana en ámbar. */
function Compromiso({ fecha }) {
  const dias = diasHasta(fecha);
  if (dias === null) return <span className="text-texto-secundario">Sin fecha</span>;

  const [texto, tono] =
    dias < 0
      ? [`Atrasado · ${fechaCorta(fecha)}`, "bg-peligro-fondo text-peligro"]
      : dias === 0
        ? ["Hoy", "bg-alerta-fondo text-alerta"]
        : dias === 1
          ? ["Mañana", "bg-alerta-fondo text-alerta"]
          : [fechaCorta(fecha), "bg-chip text-texto-secundario"];

  return <span className={`inline-block rounded-full px-2.5 py-0.5 text-xs font-medium whitespace-nowrap ${tono}`}>{texto}</span>;
}

export function TablaPedidosProduccion({ pedidos }) {
  if (pedidos.length === 0) return <EstadoVacio>No hay pedidos en producción.</EstadoVacio>;

  return (
    <div className="overflow-x-auto">
      <table className="w-full border-collapse">
        <thead>
          <tr>
            <th className={`${cabecera} text-left`}>Pedido</th>
            <th className={`${cabecera} text-left`}>Entrega</th>
            <th className={`${cabecera} text-right`}>Total</th>
          </tr>
        </thead>
        <tbody>
          {pedidos.map((p) => (
            <tr key={p.id} className="border-t border-borde">
              <td className={celda}>
                <span className="block font-medium tabular-nums">{p.codigo}</span>
                <span className="block text-[13px] text-texto-secundario">{p.cliente}</span>
              </td>
              <td className={celda}>
                <Compromiso fecha={p.fecha_compromiso} />
              </td>
              <td className={`${celda} text-right whitespace-nowrap tabular-nums`}>{dinero(p.total, p.moneda)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
