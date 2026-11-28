/**
 * Formatos de números y fechas que se repiten en las pantallas.
 * DRF envía los DecimalField como texto ("12.50"), por eso todo pasa por Number().
 */
const LOCALE = "es-VE";

const SIMBOLO = { USD: "$", VES: "Bs" };

/** 3855 -> "$ 3.855,00" ; (120, "VES") -> "Bs 120,00" */
export const dinero = (n, moneda = "USD") =>
  `${SIMBOLO[moneda] ?? moneda} ` +
  (Number(n) || 0).toLocaleString(LOCALE, { minimumFractionDigits: 2, maximumFractionDigits: 2 });

/** Cantidades de stock: 12 -> "12" ; "2.5000" -> "2,5" */
export const cantidad = (n) => (Number(n) || 0).toLocaleString(LOCALE, { maximumFractionDigits: 2 });

/** plural(1, "pedido", "pedidos") -> "1 pedido" ; plural(3, ...) -> "3 pedidos" */
export const plural = (n, uno, varios) => `${n} ${n === 1 ? uno : varios}`;

/** "2026-11-14" (DateField) -> Date local, sin el corrimiento de zona horaria. */
export function aFecha(valor) {
  if (!valor) return null;
  const [a, m, d] = String(valor).slice(0, 10).split("-").map(Number);
  return a && m && d ? new Date(a, m - 1, d) : null;
}

/** Días entre hoy y una fecha: 0 = hoy, 1 = mañana, -2 = hace dos días. */
export function diasHasta(valor) {
  const f = aFecha(valor);
  if (!f) return null;
  const hoy = new Date();
  hoy.setHours(0, 0, 0, 0);
  return Math.round((f - hoy) / 86_400_000);
}

/** "14 nov" */
export const fechaCorta = (valor) =>
  aFecha(valor)?.toLocaleDateString(LOCALE, { day: "numeric", month: "short" }).replace(".", "") ?? "—";
