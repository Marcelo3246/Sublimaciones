const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

/** Correo opcional: vacío es válido. */
export function correoOpcional(value) {
  const correo = (value || '').trim()
  if (!correo) return null
  return EMAIL_RE.test(correo) ? null : 'El correo no tiene un formato válido.'
}

export const requerido = (value, mensaje = 'Este campo es obligatorio.') =>
  String(value ?? '').trim() ? null : mensaje

/** Número mayor que cero (o mayor o igual si se permite cero). */
export function numeroPositivo(value, { permitirCero = false } = {}) {
  if (value === '' || value === null || value === undefined) return 'Escribe un número.'
  const n = Number(value)
  if (Number.isNaN(n)) return 'Debe ser un número.'
  if (permitirCero ? n < 0 : n <= 0) return permitirCero ? 'No puede ser negativo.' : 'Debe ser mayor que cero.'
  return null
}
