// Fechas relativas a hoy para los datos de ejemplo: así el dashboard y los
// reportes siempre muestran movimiento en el mes actual.

/** ISO de hace `dias` días a la hora indicada. */
export function hace(dias, horas = 10, minutos = 0) {
  const d = new Date()
  d.setDate(d.getDate() - dias)
  d.setHours(horas, minutos, 0, 0)
  return d.toISOString()
}

/** "YYYY-MM-DD" dentro de `dias` días (negativo = pasado). */
export function enDias(dias) {
  const d = new Date()
  d.setDate(d.getDate() + dias)
  const dos = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${dos(d.getMonth() + 1)}-${dos(d.getDate())}`
}
