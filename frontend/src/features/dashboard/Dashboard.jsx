import { Link } from "react-router-dom";
import Layout from "../../components/Layout.jsx";
import Panel from "../../components/Panel.jsx";
import EstadoVacio from "../../components/EstadoVacio.jsx";
import ContenidoConsulta from "../../components/ContenidoConsulta.jsx";
import { useConsulta } from "../../hooks/useConsulta.js";
import { obtenerDashboard } from "./api.js";
import TarjetasResumen from "./TarjetasResumen";
import GraficoIngresos from "./GraficoIngresos";
import TablaStock from "./TablaStock";
import "./Dashboard.css";

function Dashboard() {
  // Los datos salen de ./api.js: simulados (VITE_API_MOCK=true) o de
  // GET /reports/dashboard/ cuando el backend esté listo.
  const consulta = useConsulta(obtenerDashboard, []);

  // Mes actual: nombre ("noviembre"), número (11) y cuántos días tiene
  const hoy = new Date();
  const numeroMes = hoy.getMonth() + 1;
  const nombreMes = hoy.toLocaleDateString("es-VE", { month: "long" });
  const diasDelMes = new Date(hoy.getFullYear(), numeroMes, 0).getDate();

  return (
    <Layout
      activa="dashboard"
      titulo="Dashboard"
      acciones={
        <>
          <Link to="/compras/nueva" className="button button--secondary button--inline">Nueva compra</Link>
          <Link to="/ventas/nueva" className="button button--inline">+ Nueva venta</Link>
        </>
      }
    >
      <ContenidoConsulta consulta={consulta} esVacio={() => false}>
        {(d) => {
          const hayIngresos = Object.keys(d.ingresosDiarios).length > 0;
          return (
            <>
              <TarjetasResumen resumen={d.resumen} mes={nombreMes} />

              <section className="fila fila-2">
                <Panel titulo={`Ingresos diarios de ${nombreMes}`} enlace="Ver reporte" a="/reportes">
                  {hayIngresos ? (
                    <div className="panel-cuerpo">
                      <GraficoIngresos porDia={d.ingresosDiarios} dias={diasDelMes} mes={numeroMes} />
                    </div>
                  ) : (
                    <EstadoVacio texto="Todavía no hay ingresos registrados este mes." />
                  )}
                </Panel>

                <Panel titulo="Próximas entregas" enlace="Ver pedidos" a="/ventas">
                  {d.proximasEntregas.length === 0 ? (
                    <EstadoVacio texto="No hay entregas pendientes." />
                  ) : (
                    <ul className="lista">
                      {d.proximasEntregas.map((e) => (
                        <li key={e.id}>
                          <div>
                            <b>{e.codigo ?? `#${e.id}`} {e.cliente}</b>
                            <small>{e.descripcion}</small>
                          </div>
                          <span className={`etiqueta${e.urgente ? " manana" : ""}`}>{e.entrega}</span>
                        </li>
                      ))}
                    </ul>
                  )}
                </Panel>
              </section>

              <section className="fila fila-3">
                <Panel titulo="Menor stock de materia prima" enlace="Ver todo" a="/inventario?tab=materiales">
                  <TablaStock columna="Materia prima" filas={d.stockMateriaPrima}
                    vacio="No hay materia prima registrada." />
                </Panel>

                <Panel titulo="Menor stock de productos" enlace="Ver todo" a="/inventario">
                  <TablaStock columna="Producto" filas={d.stockProductos}
                    vacio="No hay productos registrados." />
                </Panel>

                <Panel titulo="Últimos movimientos de stock" enlace="Ver historial" a="/historial">
                  {d.movimientos.length === 0 ? (
                    <EstadoVacio texto="Todavía no hay movimientos de stock." />
                  ) : (
                    <ul className="lista">
                      {d.movimientos.map((m) => (
                        <li key={m.id}>
                          <div>
                            <b>{m.descripcion}</b>
                            <small>{m.detalle}</small>
                          </div>
                          <b>{m.cantidad > 0 ? "+" : ""}{m.cantidad}</b>
                        </li>
                      ))}
                    </ul>
                  )}
                </Panel>
              </section>
            </>
          );
        }}
      </ContenidoConsulta>
    </Layout>
  );
}

export default Dashboard;
