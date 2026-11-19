import './Pestanas.css'

/**
 * Pestañas para cambiar de vista dentro de una página.
 *   <Pestanas opciones={[{ id: 'productos', texto: 'Productos' }]} activa={tab} onCambio={setTab} />
 * Flechas izquierda/derecha mueven entre pestañas (patrón ARIA de tabs).
 */
export default function Pestanas({ opciones, activa, onCambio, etiqueta = 'Secciones' }) {
  function alTeclear(e) {
    if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return
    const i = opciones.findIndex((o) => o.id === activa)
    const siguiente = (i + (e.key === 'ArrowRight' ? 1 : -1) + opciones.length) % opciones.length
    onCambio(opciones[siguiente].id)
    e.currentTarget.querySelectorAll('[role="tab"]')[siguiente]?.focus()
  }

  return (
    <div className="pestanas" role="tablist" aria-label={etiqueta} onKeyDown={alTeclear}>
      {opciones.map((o) => (
        <button
          key={o.id}
          type="button"
          role="tab"
          className="pestana"
          aria-selected={o.id === activa}
          tabIndex={o.id === activa ? 0 : -1}
          onClick={() => onCambio(o.id)}
        >
          {o.texto}
        </button>
      ))}
    </div>
  )
}
