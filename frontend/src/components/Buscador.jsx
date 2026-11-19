import Icono from './Icono.jsx'
import './Buscador.css'

/** Caja de búsqueda para filtrar tablas. */
export default function Buscador({ valor, onCambio, placeholder = 'Buscar', etiqueta = placeholder }) {
  return (
    <label className="buscador">
      <Icono nombre="buscar" tamano={16} />
      <span className="sr-only">{etiqueta}</span>
      <input type="search" value={valor} placeholder={placeholder} onChange={(e) => onCambio(e.target.value)} />
    </label>
  )
}
