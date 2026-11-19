import './Etiqueta.css'

/**
 * Píldora de estado. `tono`: neutro | alerta | peligro | exito | marca | info.
 */
export default function Etiqueta({ tono = 'neutro', children }) {
  return <span className={`etiqueta${tono !== 'neutro' ? ` etiqueta--${tono}` : ''}`}>{children}</span>
}

/** Cantidad de stock pintada según lo que queda: 0 rojo, poco ámbar, suficiente gris. */
export function Cantidad({ valor, minimo = 5, children }) {
  const n = Number(valor) || 0
  const clase = n <= 0 ? 'cant cero' : n <= minimo ? 'cant' : 'cant ok'
  return <span className={clase}>{children ?? n}</span>
}
