import { http } from "../../../services/http";

/**
 * Dashboard (RF-56). El módulo reports no tiene tablas: el backend calcula todo
 * a partir de ventas e inventario, filtrado por el local del usuario (o de
 * todos los locales si es_global).
 *
 *   GET /api/v1/reports/dashboard/  ->
 *   {
 *     ventas_hoy: {
 *       pedidos: 3,                                  // confirmados hoy, sin anulados
 *       totales: [{ moneda: "USD", total: "120.00" }, { moneda: "VES", total: "4500.00" }]
 *     },
 *     pedidos_en_produccion: {
 *       cantidad: 4,                                 // estado EN_PRODUCCION
 *       atrasados: 1,                                // fecha_compromiso anterior a hoy
 *       pedidos: [{ id, codigo, cliente, fecha_compromiso, total, moneda }]  // por fecha_compromiso
 *     },
 *     stock_critico: {
 *       cantidad: 2,                                 // stock.cantidad_disponible <= nivel_minimo
 *       sin_existencia: 1,                           // cantidad_disponible = 0
 *       items: [{ id, tipo: "MATERIAL" | "PRODUCTO", nombre, local,
 *                 cantidad_disponible, cantidad_minima_alerta }]
 *     }
 *   }
 *
 * Comisiones por pagar queda fuera: está diferido con la nómina (fase 4).
 *
 * Con VITE_AUTH_MOCK=true la sesión es simulada y el backend rechazaría el
 * token, así que se devuelve un dashboard vacío sin llamar a la API.
 */
const USA_MOCK = import.meta.env.VITE_AUTH_MOCK === "true";

const DASHBOARD_VACIO = {
  ventas_hoy: { pedidos: 0, totales: [] },
  pedidos_en_produccion: { cantidad: 0, atrasados: 0, pedidos: [] },
  stock_critico: { cantidad: 0, sin_existencia: 0, items: [] },
};

export async function obtenerDashboard() {
  if (USA_MOCK) {
    await new Promise((resolver) => setTimeout(resolver, 400));
    return DASHBOARD_VACIO;
  }
  const { data } = await http.get("/reports/dashboard/");
  return data;
}
