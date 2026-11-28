import { CabeceraPagina } from "../../../app/layout/AppShell";
import { Button } from "../../../components/Button";
import { Panel } from "../../../components/Panel";
import { dinero, plural } from "../../../utils/formato";
import { TablaPedidosProduccion } from "../components/TablaPedidosProduccion";
import { TablaStockCritico } from "../components/TablaStockCritico";
import { TarjetaIndicador } from "../components/TarjetaIndicador";
import { useDashboard } from "../hooks/useDashboard";

/** Ventas de hoy: el monto en USD va grande y el de bolívares, si hay, en la nota. */
function resumenVentas({ pedidos, totales }) {
  const total = (moneda) => totales.find((t) => t.moneda === moneda)?.total;
  const bolivares = total("VES");
  return {
    valor: dinero(total("USD") ?? 0, "USD"),
    nota: [plural(pedidos, "pedido", "pedidos"), bolivares && dinero(bolivares, "VES")].filter(Boolean).join(" · "),
  };
}

function Contenido({ datos }) {
  const { ventas_hoy, pedidos_en_produccion: produccion, stock_critico: stock } = datos;
  const ventas = resumenVentas(ventas_hoy);

  return (
    <>
      <div className="mb-5 grid grid-cols-3 gap-5 max-[1100px]:grid-cols-2 max-[640px]:grid-cols-1">
        <TarjetaIndicador titulo="Ventas de hoy" valor={ventas.valor} nota={ventas.nota} />
        <TarjetaIndicador
          titulo="Pedidos en producción"
          valor={produccion.cantidad}
          nota={produccion.atrasados > 0 ? plural(produccion.atrasados, "atrasado", "atrasados") : "Ninguno atrasado"}
          alerta={produccion.atrasados > 0}
        />
        <TarjetaIndicador
          titulo="Stock crítico"
          valor={stock.cantidad}
          nota={stock.sin_existencia > 0 ? `${stock.sin_existencia} sin existencia` : "Todo con existencia"}
          alerta={stock.cantidad > 0}
        />
      </div>

      <div className="grid grid-cols-2 gap-5 max-[1100px]:grid-cols-1">
        <Panel titulo="Pedidos en producción">
          <TablaPedidosProduccion pedidos={produccion.pedidos} />
        </Panel>
        <Panel titulo="Stock crítico">
          <TablaStockCritico items={stock.items} />
        </Panel>
      </div>
    </>
  );
}

export function DashboardPage() {
  const { data, isPending, isError, refetch, isFetching } = useDashboard();

  return (
    <>
      <CabeceraPagina titulo="Dashboard" />

      {isPending && (
        <p className="flex items-center justify-center gap-2.5 py-16 text-texto-secundario">
          <span
            aria-hidden="true"
            className="size-4 animate-spin rounded-full border-2 border-borde border-t-marca motion-reduce:[animation-duration:2s]"
          />
          Cargando…
        </p>
      )}

      {isError && !data && (
        <div role="alert" className="flex flex-col items-center gap-3 py-16 text-center text-peligro">
          No se pudo cargar el dashboard.
          <Button variant="secondary" inline loading={isFetching} onClick={() => refetch()}>
            Reintentar
          </Button>
        </div>
      )}

      {data && <Contenido datos={data} />}
    </>
  );
}
