import Icono from './Icono.jsx'
import './BotonIcono.css'

/** Botón chico con solo ícono (editar, desactivar…). `etiqueta` se lee en lectores de pantalla y como tooltip. */
export default function BotonIcono({ icono, etiqueta, peligro = false, ...props }) {
  return (
    <button
      type="button"
      className={`boton-icono${peligro ? ' boton-icono--peligro' : ''}`}
      aria-label={etiqueta}
      title={etiqueta}
      {...props}
    >
      <Icono nombre={icono} tamano={18} />
    </button>
  )
}
