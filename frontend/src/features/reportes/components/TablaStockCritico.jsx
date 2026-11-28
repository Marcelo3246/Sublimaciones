import { EstadoVacio } from "../../../components/Panel";
import { cantidad } from "../../../utils/formato";

const celda = "px-6 py-3 max-[860px]:px-4";
const cabecera = `${celda} bg-superficie-suave py-2 text-xs font-medium whitespace-nowrap text-texto-secundario`;

const TIPO = { MATERIAL: "Materia prima", PRODUCTO: "Producto" };

export function TablaStockCritico({ items }) {
  if (items.length === 0) return <EstadoVacio>No hay stock por debajo del mínimo.</EstadoVacio>;

  return (
    <div className="overflow-x-auto">
      <table className="w-full border-collapse">
        <thead>
          <tr>
            <th className={`${cabecera} text-left`}>Ítem</th>
            <th className={`${cabecera} text-right`}>Disponible</th>
            <th className={`${cabecera} text-right`}>Mínimo</th>
          </tr>
        </thead>
        <tbody>
          {items.map((i) => {
            const agotado = Number(i.cantidad_disponible) === 0;
            return (
              <tr key={`${i.tipo}-${i.id}`} className="border-t border-borde">
                <td className={celda}>
                  <span className="block font-medium">{i.nombre}</span>
                  <span className="block text-[13px] text-texto-secundario">
                    {[TIPO[i.tipo], i.local].filter(Boolean).join(" · ")}
                  </span>
                </td>
                <td className={`${celda} text-right font-medium tabular-nums ${agotado ? "text-peligro" : "text-alerta"}`}>
                  {cantidad(i.cantidad_disponible)}
                </td>
                <td className={`${celda} text-right text-texto-secundario tabular-nums`}>
                  {cantidad(i.cantidad_minima_alerta)}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
