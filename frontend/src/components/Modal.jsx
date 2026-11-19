import { useEffect, useId, useRef } from 'react'
import BotonIcono from './BotonIcono.jsx'
import './Modal.css'

/**
 * Ventana modal con <dialog> nativo (bloquea el fondo, Escape la cierra y
 * el foco queda dentro). `pie` son los botones de abajo.
 * `tamano`: "normal" | "ancho" | "angosto".
 * Si `onEnviar` existe, el contenido es un formulario y Enter lo envía.
 */
export default function Modal({ abierto, onCerrar, titulo, pie, tamano = 'normal', onEnviar, children }) {
  const ref = useRef(null)
  const tituloId = useId()

  useEffect(() => {
    const dialogo = ref.current
    if (!dialogo) return
    if (abierto && !dialogo.open) dialogo.showModal()
    if (!abierto && dialogo.open) dialogo.close()
  }, [abierto])

  const clase = `modal${tamano === 'ancho' ? ' modal--ancho' : tamano === 'angosto' ? ' modal--angosto' : ''}`

  const contenido = (
    <>
      <div className="modal-cuerpo">{children}</div>
      {pie && <div className="modal-pie">{pie}</div>}
    </>
  )

  return (
    <dialog
      ref={ref}
      className={clase}
      aria-labelledby={tituloId}
      onCancel={(e) => {
        e.preventDefault()
        onCerrar()
      }}
      onClick={(e) => {
        // Clic en el fondo oscuro (fuera de la caja) cierra la ventana.
        if (e.target === ref.current) onCerrar()
      }}
    >
      {abierto && (
        <>
          <div className="modal-cab">
            <h2 id={tituloId}>{titulo}</h2>
            <BotonIcono icono="cerrar" etiqueta="Cerrar" onClick={onCerrar} />
          </div>
          {onEnviar ? (
            <form
              noValidate
              className="modal-formulario"
              onSubmit={(e) => {
                e.preventDefault()
                onEnviar()
              }}
            >
              {contenido}
            </form>
          ) : (
            contenido
          )}
        </>
      )}
    </dialog>
  )
}
