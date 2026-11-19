import { useState } from 'react'
import Modal from './Modal.jsx'
import Button from './Button.jsx'

/**
 * Pregunta antes de una acción delicada (desactivar, anular…).
 *   <Confirmar abierto titulo="Desactivar cliente" texto="…" confirmar="Desactivar"
 *     peligro onConfirmar={async () => …} onCerrar={() => …} />
 * Mientras onConfirmar trabaja, el botón muestra el indicador de carga.
 */
export default function Confirmar({ abierto, titulo, texto, confirmar = 'Confirmar', peligro = false, onConfirmar, onCerrar }) {
  const [trabajando, setTrabajando] = useState(false)

  async function aceptar() {
    setTrabajando(true)
    try {
      await onConfirmar()
    } finally {
      setTrabajando(false)
    }
  }

  return (
    <Modal
      abierto={abierto}
      onCerrar={onCerrar}
      titulo={titulo}
      tamano="angosto"
      pie={
        <>
          <Button type="button" variant="secondary" inline onClick={onCerrar} disabled={trabajando}>
            Cancelar
          </Button>
          <Button type="button" inline className={peligro ? 'boton-peligro' : ''} loading={trabajando} onClick={aceptar}>
            {confirmar}
          </Button>
        </>
      }
    >
      <p>{texto}</p>
    </Modal>
  )
}
