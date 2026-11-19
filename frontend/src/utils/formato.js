// Formatos de números y fechas que se repiten en todas las pantallas.
// DRF envía los DecimalField como texto ("12.50"), por eso todo pasa por Number().

const LOCALE = "es-VE";

const SIMBOLO = { USD: "$", BS: "Bs" };

// Muestra un número como dinero: 3855 -> "$ 3.855,00" ; (120, "BS") -> "Bs 120,00"
export const dinero = (n, moneda = "USD") =>
  `${SIMBOLO[moneda] ?? moneda} ` +
  (Number(n) || 0).toLocaleString(LOCALE, { minimumFractionDigits: 2, maximumFractionDigits: 2 });

// Cantidades de stock: 12 -> "12" ; "2.5000" -> "2,5"
export const cantidad = (n) => (Number(n) || 0).toLocaleString(LOCALE, { maximumFractionDigits: 2 });

// plural(1, "venta", "ventas") -> "1 venta" ; plural(3, ...) -> "3 ventas"
export const plural = (n, uno, varios) => `${n} ${n === 1 ? uno : varios}`;

// "2026-11-14" o un ISO completo -> Date local (sin el corrimiento de zona horaria)
export function aFecha(valor) {
  if (!valor) return null;
  if (valor instanceof Date) return valor;
  const texto = String(valor);
  if (/^\d{4}-\d{2}-\d{2}$/.test(texto)) {
    const [a, m, d] = texto.split("-").map(Number);
    return new Date(a, m - 1, d);
  }
  const fecha = new Date(texto);
  return Number.isNaN(fecha.getTime()) ? null : fecha;
}

// Date -> "2026-11-14" (formato que espera DRF para DateField)
export function isoDia(fecha = new Date()) {
  const f = aFecha(fecha);
  const dos = (n) => String(n).padStart(2, "0");
  return `${f.getFullYear()}-${dos(f.getMonth() + 1)}-${dos(f.getDate())}`;
}

// "14 nov 2026"
export const fecha = (valor) =>
  aFecha(valor)?.toLocaleDateString(LOCALE, { day: "numeric", month: "short", year: "numeric" }).replace(".", "") ?? "—";

// "14 nov, 16:52"
export const fechaHora = (valor) => {
  const f = aFecha(valor);
  if (!f) return "—";
  const dia = f.toLocaleDateString(LOCALE, { day: "numeric", month: "short" }).replace(".", "");
  const hora = f.toLocaleTimeString(LOCALE, { hour: "2-digit", minute: "2-digit", hour12: false });
  return `${dia}, ${hora}`;
};

// "16:52"
export const hora = (valor) =>
  aFecha(valor)?.toLocaleTimeString(LOCALE, { hour: "2-digit", minute: "2-digit", hour12: false }) ?? "";

// Días entre hoy y una fecha (0 = hoy, 1 = mañana, -2 = hace dos días)
export function diasHasta(valor) {
  const f = aFecha(valor);
  if (!f) return null;
  const hoy = new Date();
  const a = Date.UTC(hoy.getFullYear(), hoy.getMonth(), hoy.getDate());
  const b = Date.UTC(f.getFullYear(), f.getMonth(), f.getDate());
  return Math.round((b - a) / 86400000);
}

// Fecha de entrega legible: "Hoy", "Mañana", "Vencido", "3 nov"
export function entrega(valor) {
  const dias = diasHasta(valor);
  if (dias === null) return "Sin fecha";
  if (dias < 0) return "Vencido";
  if (dias === 0) return "Hoy";
  if (dias === 1) return "Mañana";
  return aFecha(valor).toLocaleDateString(LOCALE, { day: "numeric", month: "short" }).replace(".", "");
}
